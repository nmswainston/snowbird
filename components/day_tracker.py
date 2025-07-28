import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_day_tracker():
    """Render the day tracker tab"""
    snowbird_data = SnowbirdData()

    st.markdown('<h2><i data-lucide="calendar-days" class="icon"></i>Residency Day Tracker</h2>', unsafe_allow_html=True)

    # Horizontal divider after header for visual separation
    st.markdown("---")

    # Add spacing before residency section
    st.write("")

    # Current location logging
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="map-pin" class="icon"></i>Log Your Current Location**', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Updated selectbox label for clearer microcopy - asking where user is today
        current_location = st.selectbox("Where are you today?", list(st.session_state.states.keys()))
        custom_date = st.date_input("Select date:", value=datetime.date.today())
        # Added helpful caption explaining date picker default behavior
        st.caption("Defaults to today—change if needed")

    with col2:
        # Changed button label to "Log Today" for clearer microcopy
        if st.button("Log Today", type="primary"):
            success, message = snowbird_data.add_day_log(current_location, custom_date.isoformat())
            if success:
                # Enhanced feedback confirmation with clear, specific messaging
                formatted_date = custom_date.strftime("%Y-%m-%d")
                st.success(f"✅ Logged {current_location} for {formatted_date}")
                st.rerun()
            else:
                st.warning(message)

    st.markdown('</div>', unsafe_allow_html=True)

    # Add spacing before activity section
    st.write("")

    # Recent activity
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="activity" class="icon"></i>Recent Activity**', unsafe_allow_html=True)

    if st.session_state.day_log:
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.markdown(f'<i data-lucide="calendar" class="icon"></i>{date_obj.strftime("%b %d, %Y")} - **{log["state"]}**', unsafe_allow_html=True)
    else:
        # Enhanced empty state with visual snowflake illustration
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Center-aligned snowflake visual with styling
            st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <div style="font-size: 4rem; color: #AEDFF7; margin-bottom: 1rem;">❄️</div>
                <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 0.5rem;">No activity yet—log your first day!</p>
                <p style="color: #94a3b8; font-size: 0.9rem;">Start tracking your snowbird journey above ↑</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Add spacing before bulk operations section
    st.write("")

    # Bulk operations - wrapped in expander to reduce visual noise
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)

    with st.expander("⚙️ Bulk Operations"):
        st.caption("Advanced: adjust multiple days at once.")

        col1, col2 = st.columns(2)

        with col1:
            # Updated selectbox label to match main interface microcopy
            bulk_state = st.selectbox("Which location for bulk operation?", list(st.session_state.states.keys()), key="bulk_state")
            bulk_days = st.number_input("Set total days:", min_value=0, max_value=365, value=st.session_state.states[bulk_state])

            if st.button("Update Total Days"):
                st.session_state.states[bulk_state] = bulk_days
                # Enhanced feedback confirmation for bulk operations
                st.success(f"✅ Updated {bulk_state} total to {bulk_days} days")
                st.rerun()

        with col2:
            if st.button("Clear All Logs", type="secondary"):
                st.session_state.day_log = []
                st.session_state.states = {state: 0 for state in st.session_state.states.keys()}
                # Enhanced feedback confirmation for data clearing
                st.success("✅ All logs and counts have been cleared")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)