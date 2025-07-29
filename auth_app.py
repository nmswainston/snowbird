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
            'theme': 'light',
            'notifications': True,
            'auto_tracking': False
        })
        st.session_state.trip_plans = profile.get('trip_plans', [])
        st.session_state.financial_notes = profile.get('financial_notes', [])
        st.session_state.saved_destinations = profile.get('saved_destinations', [])
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
        'trip_plans': st.session_state.get('trip_plans', []),
        'financial_notes': st.session_state.get('financial_notes', []),
        'saved_destinations': st.session_state.get('saved_destinations', []),
        'last_activity': datetime.now()
    }

    return db.update_user_profile(user['uid'], sync_data)

def apply_user_theme():
    """Apply user's theme preference"""
    theme = st.session_state.user_preferences.get('theme', 'light')

    if theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #f1f5f9;
        }
        .theme-card {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1e293b;
        }
        .theme-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        </style>
        """, unsafe_allow_html=True)

def render_trip_dashboard():
    """Render trip planning dashboard"""
    st.markdown("### 🏖️ Trip Dashboard")

    # Real-time sync indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**Upcoming Trips & Location Tracking**")
    with col2:
        if st.button("🔄 Sync Trips"):
            if sync_data_to_firebase():
                show_success("✅ Trips synced!")
                st.rerun()
    with col3:
        sync_status = "🟢 Live" if 'last_sync' in st.session_state else "🔴 Offline"
        st.markdown(f"**Status:** {sync_status}")

    # Quick location logger
    st.markdown("#### 📍 Log Today's Location")
    location_col1, location_col2 = st.columns([2, 1])

    with location_col1:
        location = st.selectbox("Where are you today?", ("Arizona", "Minnesota", "Other"))

    with location_col2:
        if st.button("Log Day", use_container_width=True):
            if location in st.session_state.states:
                st.session_state.states[location] += 1
            else:
                st.session_state.states[location] = 1

            if sync_data_to_firebase():
                show_success(f"✅ Logged day in {location}!")
                st.rerun()

    # Current residency status
    st.markdown("#### 📊 Tax Residency Status")

    for state, days in st.session_state.states.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            progress = min(days / 183, 1.0)
            st.progress(progress, text=f"{state}: {days} days (Goal: < 183)")
        with col2:
            if days >= 183:
                st.error("⚠️ Risk")
            elif days >= 150:
                st.warning("🟡 Caution")
            else:
                st.success("✅ Safe")

    # Trip planning
    st.markdown("#### ✈️ Planned Trips")

    # Add new trip
    with st.expander("➕ Add New Trip"):
        trip_col1, trip_col2, trip_col3 = st.columns(3)

        with trip_col1:
            destination = st.text_input("Destination")
            start_date = st.date_input("Start Date")
        with trip_col2:
            end_date = st.date_input("End Date")
            trip_type = st.selectbox("Type", ["Business", "Personal", "Medical"])
        with trip_col3:
            st.write("")  # Spacing
            st.write("")
            if st.button("Add Trip", use_container_width=True):
                if destination and start_date and end_date:
                    new_trip = {
                        'id': len(st.session_state.trip_plans) + 1,
                        'destination': destination,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'type': trip_type,
                        'created_at': datetime.now().isoformat()
                    }
                    st.session_state.trip_plans.append(new_trip)

                    if sync_data_to_firebase():
                        show_success("✅ Trip added!")
                        st.rerun()

    # Display existing trips
    if st.session_state.trip_plans:
        for i, trip in enumerate(st.session_state.trip_plans):
            with st.container():
                st.markdown(f"""
                <div style="background: var(--overlay-light); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <strong>🏝️ {trip['destination']}</strong><br>
                    📅 {trip['start_date']} to {trip['end_date']}<br>
                    🏷️ Type: {trip['type']}
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Remove Trip {i+1}", key=f"remove_trip_{i}"):
                    st.session_state.trip_plans.pop(i)
                    sync_data_to_firebase()
                    st.rerun()
    else:
        st.info("📝 No trips planned yet. Add your first trip above!")

def render_budget_tracker():
    """Render budget tracking interface"""
    st.markdown("### 💰 Budget Tracker")

    # Real-time sync for budgets
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Multi-Home Budget Management**")
    with col2:
        if st.button("💾 Save Budgets"):
            if sync_data_to_firebase():
                show_success("✅ Budgets saved!")
                st.rerun()

    # Home budgets with inline editing
    st.markdown("#### 🏠 Home Maintenance Budgets")

    for home, budget in st.session_state.home_budgets.items():
        with st.expander(f"🏡 {home} Budget", expanded=True):
            st.markdown(f"**Monthly Budget for {home}**")

            # Create editable budget categories
            total_budget = 0
            for category, amount in budget.items():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"• {category}")
                with col2:
                    new_amount = st.number_input(
                        f"Amount", 
                        value=amount, 
                        min_value=0, 
                        key=f"budget_{home}_{category}",
                        label_visibility="collapsed"
                    )
                    if new_amount != amount:
                        st.session_state.home_budgets[home][category] = new_amount
                with col3:
                    st.write(f"${new_amount:,}")

                total_budget += new_amount

            # Add new category
            with st.container():
                add_col1, add_col2, add_col3 = st.columns([2, 1, 1])
                with add_col1:
                    new_category = st.text_input(f"New category for {home}", key=f"new_cat_{home}")
                with add_col2:
                    new_amount = st.number_input(f"Amount for new category", min_value=0, key=f"new_amt_{home}")
                with add_col3:
                    if st.button(f"Add", key=f"add_cat_{home}"):
                        if new_category and new_amount > 0:
                            st.session_state.home_budgets[home][new_category] = new_amount
                            sync_data_to_firebase()
                            st.rerun()

            st.markdown(f"**Total Monthly: ${total_budget:,}**")
            st.markdown(f"**Annual Projection: ${total_budget * 12:,}**")

    # Seasonal expenses
    st.markdown("#### 🌊 Seasonal Cash Flow")

    total_seasonal = 0
    for category, amount in st.session_state.seasonal_cash_flow.items():
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            icon = "✈️" if "Travel" in category else "🏥" if "Healthcare" in category else "🛡️"
            st.write(f"{icon} {category}")
        with col2:
            new_amount = st.number_input(
                f"Monthly amount", 
                value=amount, 
                min_value=0, 
                key=f"seasonal_{category}",
                label_visibility="collapsed"
            )
            if new_amount != amount:
                st.session_state.seasonal_cash_flow[category] = new_amount
        with col3:
            st.write(f"${new_amount:,}")

        total_seasonal += new_amount

    st.markdown(f"**Total Seasonal Monthly: ${total_seasonal:,}**")
    st.markdown(f"**Total Seasonal Annual: ${total_seasonal * 12:,}**")

def render_notes_section():
    """Render financial notes and documents"""
    st.markdown("### 📝 Financial Notes")

    # Sync controls
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Personal Financial Notes & Reminders**")
    with col2:
        if st.button("💾 Save Notes"):
            if sync_data_to_firebase():
                show_success("✅ Notes saved!")
                st.rerun()

    # Add new note
    with st.expander("➕ Add New Note", expanded=False):
        note_col1, note_col2 = st.columns([3, 1])

        with note_col1:
            note_title = st.text_input("Note Title")
            note_content = st.text_area("Note Content", height=100)
            note_category = st.selectbox("Category", ["Tax", "Budget", "Travel", "Insurance", "General"])

        with note_col2:
            st.write("")  # Spacing
            st.write("")
            if st.button("Add Note", use_container_width=True):
                if note_title and note_content:
                    new_note = {
                        'id': len(st.session_state.financial_notes) + 1,
                        'title': note_title,
                        'content': note_content,
                        'category': note_category,
                        'created_at': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat()
                    }
                    st.session_state.financial_notes.append(new_note)

                    if sync_data_to_firebase():
                        show_success("✅ Note added!")
                        st.rerun()

    # Display existing notes
    if st.session_state.financial_notes:
        # Filter by category
        categories = list(set([note['category'] for note in st.session_state.financial_notes]))
        selected_category = st.selectbox("Filter by category:", ["All"] + categories)

        filtered_notes = st.session_state.financial_notes
        if selected_category != "All":
            filtered_notes = [note for note in st.session_state.financial_notes if note['category'] == selected_category]

        for i, note in enumerate(filtered_notes):
            with st.expander(f"📋 {note['title']} ({note['category']})"):
                # Inline editing
                col1, col2 = st.columns([3, 1])

                with col1:
                    updated_content = st.text_area(
                        "Content", 
                        value=note['content'], 
                        key=f"note_content_{note['id']}",
                        height=80
                    )

                    if updated_content != note['content']:
                        # Find and update the note
                        for original_note in st.session_state.financial_notes:
                            if original_note['id'] == note['id']:
                                original_note['content'] = updated_content
                                original_note['last_updated'] = datetime.now().isoformat()
                                break

                with col2:
                    st.caption(f"Created: {note['created_at'][:10]}")
                    if 'last_updated' in note:
                        st.caption(f"Updated: {note['last_updated'][:10]}")

                    if st.button(f"🗑️ Delete", key=f"delete_note_{note['id']}"):
                        st.session_state.financial_notes = [n for n in st.session_state.financial_notes if n['id'] != note['id']]
                        sync_data_to_firebase()
                        st.rerun()
    else:
        st.info("📝 No notes yet. Add your first financial note above!")

    # Saved destinations (stretch goal)
    st.markdown("#### 🌟 Saved Destinations")

    with st.expander("➕ Add Destination"):
        dest_col1, dest_col2, dest_col3 = st.columns(3)

        with dest_col1:
            dest_name = st.text_input("Destination Name")
        with dest_col2:
            dest_url = st.text_input("Website/Link (optional)")
        with dest_col3:
            st.write("")
            if st.button("Save Destination"):
                if dest_name:
                    new_dest = {
                        'name': dest_name,
                        'url': dest_url,
                        'added_at': datetime.now().isoformat()
                    }
                    st.session_state.saved_destinations.append(new_dest)
                    sync_data_to_firebase()
                    st.rerun()

    # Display saved destinations
    if st.session_state.saved_destinations:
        for i, dest in enumerate(st.session_state.saved_destinations):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if dest.get('url'):
                    st.markdown(f"🌴 [{dest['name']}]({dest['url']})")
                else:
                    st.markdown(f"🌴 {dest['name']}")
            with col2:
                st.caption(f"Added: {dest['added_at'][:10]}")
            with col3:
                if st.button(f"Remove", key=f"remove_dest_{i}"):
                    st.session_state.saved_destinations.pop(i)
                    sync_data_to_firebase()
                    st.rerun()

def render_dashboard():
    """Render the main Snowbird dashboard for authenticated users"""

    # Apply user theme
    apply_user_theme()

    # Sync data on load
    if 'data_loaded' not in st.session_state:
        with st.spinner("Loading your personalized dashboard..."):
            if initialize_user_session():
                st.session_state.data_loaded = True
                show_success("✅ Dashboard loaded successfully!")
            else:
                show_error("⚠️ Could not load user data")

    # Header with user info and controls
    auth = get_firebase_auth()
    user = auth.get_current_user()

    # Main header
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: var(--overlay-light); border-radius: 12px; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: var(--primary);">❄️ Snowbird Financial Dashboard 🏖️</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Your personalized seasonal lifestyle assistant</p>
    </div>
    """, unsafe_allow_html=True)

    # User controls bar
    control_col1, control_col2, control_col3, control_col4 = st.columns([2, 1, 1, 1])

    with control_col1:
        st.markdown(f"**Welcome back, {user.get('email', 'User').split('@')[0]}!** 👋")

    with control_col2:
        # Theme toggle
        current_theme = st.session_state.user_preferences.get('theme', 'light')
        theme_icon = "🌙" if current_theme == 'light' else "☀️"
        if st.button(f"{theme_icon} Theme"):
            new_theme = 'dark' if current_theme == 'light' else 'light'
            st.session_state.user_preferences['theme'] = new_theme
            sync_data_to_firebase()
            st.rerun()

    with control_col3:
        # Auto-sync toggle
        if st.button("🔄 Auto-Sync"):
            if sync_data_to_firebase():
                show_success("✅ Synced!")
                st.session_state.last_sync = datetime.now()

    with control_col4:
        # Logout button
        if st.button("🚪 Logout", type="secondary"):
            auth.logout_user()
            # Clear all session data
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Sync status indicator
    if 'last_sync' in st.session_state:
        st.caption(f"🔄 Last synced: {st.session_state.last_sync.strftime('%I:%M %p')}")

    st.markdown("---")

    # Main tabbed interface
    tab1, tab2, tab3 = st.tabs(["🏖️ Trip Dashboard", "💰 Budget Tracker", "📝 Notes & Planning"])

    with tab1:
        render_trip_dashboard()

    with tab2:
        render_budget_tracker()

    with tab3:
        render_notes_section()

    # Auto-sync footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: var(--overlay-light); border-radius: 8px; margin-top: 2rem;">
        <small>🔄 Your data automatically syncs across all your devices • 🔐 Secured with Firebase Authentication</small>
    </div>
    """, unsafe_allow_html=True)

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
            'theme': 'light',
            'notifications': True,
            'auto_tracking': False
        }
        st.session_state.trip_plans = []
        st.session_state.financial_notes = []
        st.session_state.saved_destinations = []

    # Check authentication
    try:
        user = check_authentication()

        # User is authenticated, show personalized dashboard
        render_dashboard()

        # Background auto-sync every 30 seconds
        if 'last_auto_sync' not in st.session_state:
            st.session_state.last_auto_sync = datetime.now()

        current_time = datetime.now()
        if (current_time - st.session_state.last_auto_sync).seconds > 30:
            sync_data_to_firebase()
            st.session_state.last_auto_sync = current_time

    # Note: st.stop() will halt execution here if user is not authenticated
    # No need to catch it as an exception
    except BaseException as e:
        st.error(f"❌ Dashboard Error: {e}")
        st.write("Please refresh the page or contact support.")

        # Debug information
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug Details"):
                st.code(f"Error Type: {type(e).__name__}")
                st.code(f"Error Message: {str(e)}")

        # Fallback logout option
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()