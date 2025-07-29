
import streamlit as st
import time
from datetime import datetime
from components.auth_components import (
    render_auth_page, 
    render_user_profile, 
    render_logout_button,
    check_authentication
)
from utils.firebase_database import get_firebase_database
from utils.firebase_auth import get_firebase_auth
from components.loading_states import show_loading, show_success, show_error
from utils.profile_sync import sync_user_data, watch_user_data_changes
import threading

# Configure page
st.set_page_config(
    page_title="Snowbird Financial Assistant",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_user_session():
    """Initialize user session with Firebase data"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if not user:
        return False
    
    # Get user profile from Firebase
    db = get_firebase_database()
    profile = db.get_user_profile(user['uid'])
    
    if profile:
        # Sync Firebase data to session state
        st.session_state.states = profile.get('states', {'Arizona': 0, 'Minnesota': 0})
        st.session_state.home_budgets = profile.get('home_budgets', {
            'Arizona': {'Utilities': 200, 'Insurance': 150, 'HOA': 100},
            'Minnesota': {'Utilities': 250, 'Insurance': 170, 'HOA': 90}
        })
        st.session_state.seasonal_cash_flow = profile.get('seasonal_cash_flow', {
            'Travel': 300, 'Healthcare': 400, 'Supplemental Insurance': 200
        })
        st.session_state.user_preferences = profile.get('preferences', {
            'theme': 'default',
            'notifications': True,
            'auto_tracking': False
        })
        st.session_state.last_sync = datetime.now()
        return True
    
    return False

def sync_data_to_firebase():
    """Sync session state data to Firebase"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if not user:
        return False
    
    db = get_firebase_database()
    
    # Prepare data for sync
    sync_data = {
        'states': st.session_state.get('states', {}),
        'home_budgets': st.session_state.get('home_budgets', {}),
        'seasonal_cash_flow': st.session_state.get('seasonal_cash_flow', {}),
        'preferences': st.session_state.get('user_preferences', {}),
        'last_activity': datetime.now()
    }
    
    return db.update_user_profile(user['uid'], sync_data)

def render_dashboard():
    """Render the main Snowbird dashboard for authenticated users"""
    
    # Sync data on load
    if 'data_loaded' not in st.session_state:
        with st.spinner("Loading your data..."):
            if initialize_user_session():
                st.session_state.data_loaded = True
                show_success("✅ Data loaded successfully!")
            else:
                show_error("⚠️ Could not load user data")
    
    # Header with user info
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("❄️ Snowbird Financial Assistant 🏖️")
    with col2:
        st.markdown(f"**Welcome, {user.get('email', 'User')}!**")
    with col3:
        if st.button("🔄 Sync Data"):
            with st.spinner("Syncing..."):
                if sync_data_to_firebase():
                    show_success("✅ Data synced!")
                    st.rerun()
                else:
                    show_error("❌ Sync failed")
    
    # Real-time sync indicator
    if 'last_sync' in st.session_state:
        st.caption(f"Last synced: {st.session_state.last_sync.strftime('%I:%M %p')}")
    
    # Location Logging
    st.header("🏡 Log Your Location")
    location = st.radio("Where are you today?", ("Arizona", "Minnesota"))
    
    if st.button(f"Log a day in {location}"):
        st.session_state.states[location] += 1
        
        # Auto-sync to Firebase
        with st.spinner("Saving..."):
            if sync_data_to_firebase():
                show_success(f"Logged a day in {location}! ✅")
                
                # Log activity
                db = get_firebase_database()
                db.log_activity(user['uid'], 'location_logged', {
                    'location': location,
                    'total_days': st.session_state.states[location]
                })
            else:
                show_error("❌ Failed to save. Please try again.")
    
    # Budget Management
    st.header("📊 Home Maintenance Budget")
    budget_home = st.selectbox("Select a home to view budget:", ["Arizona", "Minnesota"])
    
    budget = st.session_state.home_budgets.get(budget_home, {})
    
    st.subheader(f"{budget_home} Budget")
    
    # Editable budget
    with st.expander("Edit Budget", expanded=False):
        for category, amount in budget.items():
            new_amount = st.number_input(
                f"{category} (monthly)", 
                value=amount, 
                min_value=0, 
                key=f"budget_{budget_home}_{category}"
            )
            if new_amount != amount:
                st.session_state.home_budgets[budget_home][category] = new_amount
        
        if st.button("Save Budget Changes"):
            with st.spinner("Saving budget..."):
                if sync_data_to_firebase():
                    show_success("✅ Budget updated!")
                    st.rerun()
                else:
                    show_error("❌ Failed to save budget")
    
    # Display current budget
    for category, amount in budget.items():
        st.write(f"- {category}: ${amount}/month")
    
    # Seasonal Cash Flow
    st.header("💸 Seasonal Cash Flow Plan")
    seasonal_flow = st.session_state.get('seasonal_cash_flow', {})
    
    for category, amount in seasonal_flow.items():
        st.write(f"- {category}: ${amount}/month")
    
    # Tax Residency Tracker
    st.header("📅 Tax Residency Tracker")
    TAX_THRESHOLD_DAYS = 183
    
    for state, days in st.session_state.states.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{state}: {days} days")
            if days >= TAX_THRESHOLD_DAYS:
                st.warning(f"⚠️ You may be considered a tax resident of {state}!")
        with col2:
            # Progress bar
            progress = min(days / TAX_THRESHOLD_DAYS, 1.0)
            st.progress(progress)
    
    # User Profile Management
    with st.sidebar:
        render_logout_button()
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Theme preference
        current_theme = st.session_state.user_preferences.get('theme', 'default')
        new_theme = st.selectbox(
            "Theme", 
            ['default', 'dark', 'light'], 
            index=['default', 'dark', 'light'].index(current_theme)
        )
        
        # Notifications
        notifications = st.checkbox(
            "Enable Notifications", 
            value=st.session_state.user_preferences.get('notifications', True)
        )
        
        # Auto tracking
        auto_tracking = st.checkbox(
            "Auto Location Tracking", 
            value=st.session_state.user_preferences.get('auto_tracking', False)
        )
        
        # Save preferences
        if st.button("Save Preferences"):
            st.session_state.user_preferences.update({
                'theme': new_theme,
                'notifications': notifications,
                'auto_tracking': auto_tracking
            })
            
            with st.spinner("Saving preferences..."):
                if sync_data_to_firebase():
                    show_success("✅ Preferences saved!")
                    st.rerun()
                else:
                    show_error("❌ Failed to save preferences")

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.states = {'Arizona': 0, 'Minnesota': 0}
        st.session_state.home_budgets = {
            'Arizona': {'Utilities': 200, 'Insurance': 150, 'HOA': 100},
            'Minnesota': {'Utilities': 250, 'Insurance': 170, 'HOA': 90}
        }
        st.session_state.seasonal_cash_flow = {
            'Travel': 300, 'Healthcare': 400, 'Supplemental Insurance': 200
        }
        st.session_state.user_preferences = {
            'theme': 'default',
            'notifications': True,
            'auto_tracking': False
        }
    
    # Check authentication
    try:
        user = check_authentication()
        
        # User is authenticated, show dashboard
        render_dashboard()
        
        # Auto-sync data periodically (every 30 seconds)
        if 'last_auto_sync' not in st.session_state:
            st.session_state.last_auto_sync = datetime.now()
        
        current_time = datetime.now()
        if (current_time - st.session_state.last_auto_sync).seconds > 30:
            sync_data_to_firebase()
            st.session_state.last_auto_sync = current_time
            
    except st.stop:
        # User not authenticated, auth page is already rendered
        pass
    except Exception as e:
        st.error(f"❌ Application Error: {e}")
        st.write("Please refresh the page or contact support.")

if __name__ == "__main__":
    main()
