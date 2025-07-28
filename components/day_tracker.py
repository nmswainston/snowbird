
import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_day_tracker():
    """Render the day tracker tab"""
    snowbird_data = SnowbirdData()
    
    st.markdown('<h2><i data-lucide="calendar-days" class="icon"></i>Residency Day Tracker</h2>', unsafe_allow_html=True)

    # Current location logging
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="map-pin" class="icon"></i>Log Your Current Location**', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        current_location = st.selectbox("Where are you today?", list(st.session_state.states.keys()))
        custom_date = st.date_input("Select date:", value=datetime.date.today())

    with col2:
        if st.button("Log Day", type="primary"):
            success, message = snowbird_data.add_day_log(current_location, custom_date.isoformat())
            if success:
                st.success(message)
                st.rerun()
            else:
                st.warning(message)

    st.markdown('</div>', unsafe_allow_html=True)

    # Recent activity
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="activity" class="icon"></i>Recent Activity**', unsafe_allow_html=True)

    if st.session_state.day_log:
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.markdown(f'<i data-lucide="calendar" class="icon"></i>{date_obj.strftime("%b %d, %Y")} - **{log["state"]}**', unsafe_allow_html=True)
    else:
        st.write("No activity logged yet. Start by logging your current location!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Bulk operations
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="settings" class="icon"></i>Bulk Operations**', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        bulk_state = st.selectbox("State for bulk operation:", list(st.session_state.states.keys()), key="bulk_state")
        bulk_days = st.number_input("Set total days:", min_value=0, max_value=365, value=st.session_state.states[bulk_state])

        if st.button("Update Total Days"):
            st.session_state.states[bulk_state] = bulk_days
            st.success(f"Updated {bulk_state} to {bulk_days} days")
            st.rerun()

    with col2:
        if st.button("Clear All Logs", type="secondary"):
            st.session_state.day_log = []
            st.session_state.states = {state: 0 for state in st.session_state.states.keys()}
            st.success("All logs cleared!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
