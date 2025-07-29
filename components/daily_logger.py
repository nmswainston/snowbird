
import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_daily_state_logger():
    """Render a simple daily state logging interface with Firebase integration"""
    
    # Initialize data manager and Firebase
    data_manager = SnowbirdData()
    
    # Import Firebase database
    try:
        from utils.firebase_database import get_firebase_database
        firebase_db = get_firebase_database()
        has_firebase = True
    except ImportError:
        has_firebase = False
    
    st.markdown("### 📍 Daily Location Logger")
    st.markdown("*Track where you are today for tax residency tracking*")
    
    # Create the logging form
    with st.form("daily_location_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Get available states
            available_states = ["Arizona", "Minnesota", "Florida", "Texas", "California", "Nevada", "North Carolina", "Other"]
            
            # Add any states from session state
            if 'states' in st.session_state:
                for state in st.session_state.states.keys():
                    if state not in available_states:
                        available_states.append(state)
            
            available_states = sorted(available_states)
            
            selected_state = st.selectbox(
                "Where are you today?",
                options=available_states,
                key="daily_logger_state",
                help="Select your current state/location"
            )
            
            # Optional date picker (defaults to today)
            log_date = st.date_input(
                "Date",
                value=datetime.date.today(),
                max_value=datetime.date.today(),
                key="daily_logger_date",
                help="Defaults to today"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # More spacing
            
            # Submit button
            submitted = st.form_submit_button(
                "📅 Log Location",
                type="primary",
                use_container_width=True
            )
    
    # Handle form submission
    if submitted and selected_state:
        # Save to local session state
        success, message = data_manager.add_day_log(selected_state, log_date.isoformat())
        
        if success:
            # Save to Firebase if available and user is authenticated
            if has_firebase and 'user' in st.session_state and st.session_state.user:
                try:
                    # Save location data to Firebase
                    firebase_db.save_location_data(
                        st.session_state.user['uid'], 
                        st.session_state.states
                    )
                    
                    # Log activity for analytics
                    firebase_db.log_activity(
                        st.session_state.user['uid'],
                        'daily_location_logged',
                        {
                            'state': selected_state,
                            'date': log_date.isoformat(),
                            'method': 'daily_logger'
                        }
                    )
                    
                    st.success(f"✅ {message} - Synced to cloud!")
                    
                except Exception as e:
                    st.success(f"✅ {message} - Saved locally")
                    st.caption("⚠️ Cloud sync temporarily unavailable")
            else:
                st.success(f"✅ {message}")
                if not has_firebase:
                    st.caption("💡 Sign in to sync data across devices")
        else:
            st.warning(message)
    
    # Show quick stats
    if 'states' in st.session_state and st.session_state.states:
        st.markdown("---")
        st.markdown("**Current Year Totals:**")
        
        cols = st.columns(len(st.session_state.states))
        for idx, (state, days) in enumerate(st.session_state.states.items()):
            with cols[idx]:
                threshold = st.session_state.get('tax_threshold', 183)
                percentage = (days / threshold) * 100
                
                if percentage < 50:
                    color = "🟢"
                elif percentage < 80:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.metric(
                    f"{color} {state}",
                    f"{days} days",
                    f"{percentage:.1f}% of threshold"
                )

def render_quick_state_logger():
    """Render a minimal quick logging interface"""
    
    data_manager = SnowbirdData()
    
    # Single row quick logger
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        available_states = ["Arizona", "Minnesota", "Florida", "Texas", "California", "Other"]
        if 'states' in st.session_state:
            for state in st.session_state.states.keys():
                if state not in available_states:
                    available_states.append(state)
        
        selected_state = st.selectbox(
            "Where are you today?",
            options=sorted(available_states),
            key="quick_logger_state"
        )
    
    with col2:
        if st.button("📍 Log Today", type="primary", use_container_width=True):
            success, message = data_manager.add_day_log(selected_state)
            
            if success:
                # Firebase sync
                try:
                    from utils.firebase_database import get_firebase_database
                    firebase_db = get_firebase_database()
                    
                    if 'user' in st.session_state and st.session_state.user:
                        firebase_db.save_location_data(
                            st.session_state.user['uid'], 
                            st.session_state.states
                        )
                        st.success(f"✅ {message} - Synced!")
                    else:
                        st.success(f"✅ {message}")
                except:
                    st.success(f"✅ {message}")
            else:
                st.warning(message)
    
    with col3:
        # Show today's total
        total_days = sum(st.session_state.get('states', {}).values())
        st.metric("Total Days", total_days)
