import streamlit as st
import datetime
from utils.data_models import SnowbirdData
import pandas as pd

def render_day_tracker():
    """Render the day tracking interface with property-based state selection and Firebase integration"""
    st.markdown('<h2><i data-lucide="calendar" class="icon"></i>Daily Location Tracker</h2>', unsafe_allow_html=True)

    # Initialize data manager and Firebase
    data_manager = SnowbirdData()
    
    # Import Firebase database
    from utils.firebase_database import get_firebase_database
    firebase_db = get_firebase_database()

    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)

    total_days = sum(st.session_state.states.values())

    with col1:
        st.metric("Total Days Logged", total_days)

    with col2:
        max_state = max(st.session_state.states.keys(), key=lambda x: st.session_state.states[x]) if st.session_state.states else "None"
        st.metric("Primary State", max_state)

    with col3:
        if st.session_state.states:
            max_days = max(st.session_state.states.values())
            days_to_threshold = st.session_state.tax_threshold - max_days
            st.metric("Days to Tax Threshold", days_to_threshold)
        else:
            st.metric("Days to Tax Threshold", st.session_state.tax_threshold)

    with col4:
        year_days = datetime.datetime.now().timetuple().tm_yday
        days_remaining = 365 - year_days
        st.metric("Days Left in Year", days_remaining)

    st.markdown("---")

    # Enhanced Quick Location Logger with Firebase
    st.subheader("📍 Where are you today?")
    
    # Create a prominent daily logging section
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #f8f9ff 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border: 2px solid #e1f5fe;">
        """, unsafe_allow_html=True)
        
        quick_col1, quick_col2, quick_col3 = st.columns([3, 2, 2])

        with quick_col1:
            # Get available states from properties and existing states
            available_states = set(st.session_state.states.keys())

            # Add states from user properties if they exist
            if 'user_properties' in st.session_state:
                for prop_name, prop_details in st.session_state.user_properties.items():
                    available_states.add(prop_details['state'])

            # Ensure we have at least the default states
            if not available_states:
                available_states = {"Arizona", "Minnesota", "Florida", "Texas", "California", "Other"}

            available_states = sorted(list(available_states))

            selected_state = st.selectbox(
                "Where are you today?",
                options=available_states,
                key="daily_state_selector",
                help="Select your current state for today's log entry"
            )

        with quick_col2:
            # Show properties in selected state
            properties_in_state = []
            if 'user_properties' in st.session_state:
                properties_in_state = [
                    prop_name for prop_name, prop_details in st.session_state.user_properties.items()
                    if prop_details['state'] == selected_state
                ]

            if properties_in_state:
                selected_property = st.selectbox(
                    "Property (Optional)",
                    options=["Not Specified"] + properties_in_state,
                    key="daily_property_selector"
                )
            else:
                selected_property = "Not Specified"
                if selected_state in ["Arizona", "Minnesota"]:
                    st.caption(f"No properties configured in {selected_state}")

        with quick_col3:
            st.write("")  # Add some spacing
            if st.button("📅 Log Today's Location", type="primary", use_container_width=True):
                # Save to local session state
                success, message = data_manager.add_day_log(selected_state)
                
                if success:
                    # Save to Firebase if user is authenticated
                    if 'user' in st.session_state and st.session_state.user:
                        try:
                            # Save location data to Firebase
                            firebase_db.save_location_data(
                                st.session_state.user['uid'], 
                                st.session_state.states
                            )
                            
                            # Log activity for analytics
                            firebase_db.log_activity(
                                st.session_state.user['uid'],
                                'location_logged',
                                {
                                    'state': selected_state,
                                    'property': selected_property if selected_property != "Not Specified" else None,
                                    'date': datetime.date.today().isoformat()
                                }
                            )
                            
                            st.success(f"✅ {message} - Saved to cloud!")
                        except Exception as e:
                            st.success(f"✅ {message} - Local save only")
                            st.warning("⚠️ Cloud sync failed, but data saved locally")
                    else:
                        st.success(f"✅ {message}")
                    
                    if selected_property != "Not Specified":
                        st.info(f"🏠 Logged at: {selected_property}")
                else:
                    st.warning(message)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Property Quick Actions
    if 'user_properties' in st.session_state and st.session_state.user_properties:
        st.markdown("**🏠 Quick Log by Property:**")

        # Create columns for each property (max 4 per row)
        properties = list(st.session_state.user_properties.items())
        rows = [properties[i:i+4] for i in range(0, len(properties), 4)]

        for row in rows:
            cols = st.columns(len(row))
            for idx, (prop_name, prop_details) in enumerate(row):
                with cols[idx]:
                    if st.button(
                        f"📍 {prop_name}\n({prop_details['state']})",
                        key=f"quick_log_{prop_name}",
                        use_container_width=True
                    ):
                        success, message = data_manager.add_day_log(prop_details['state'])
                        if success:
                            st.success(f"✅ Logged day in {prop_details['state']} at {prop_name}")
                        else:
                            st.warning(message)
                        st.rerun()

    st.markdown("---")

    # Manual Date Entry
    st.subheader("📝 Log Specific Date")

    manual_col1, manual_col2, manual_col3, manual_col4 = st.columns([2, 2, 2, 1])

    with manual_col1:
        manual_date = st.date_input(
            "Select Date",
            value=datetime.date.today(),
            max_value=datetime.date.today(),
            key="manual_date_input"
        )

    with manual_col2:
        manual_state = st.selectbox(
            "Select State",
            options=available_states,
            key="manual_state_selector"
        )

    with manual_col3:
        # Show properties in selected state for manual entry
        manual_properties_in_state = []
        if 'user_properties' in st.session_state:
            manual_properties_in_state = [
                prop_name for prop_name, prop_details in st.session_state.user_properties.items()
                if prop_details['state'] == manual_state
            ]

        if manual_properties_in_state:
            manual_property = st.selectbox(
                "Property (Optional)",
                options=["Not Specified"] + manual_properties_in_state,
                key="manual_property_selector"
            )
        else:
            manual_property = "Not Specified"

    with manual_col4:
        if st.button("➕ Add Entry", type="secondary", use_container_width=True):
            success, message = data_manager.add_day_log(manual_state, manual_date.isoformat())
            if success:
                st.success(message)
                if manual_property != "Not Specified":
                    st.info(f"🏠 Logged at: {manual_property}")
            else:
                st.warning(message)
            st.rerun()

    # Recent Activity & Calendar View
    st.markdown("---")

    activity_col1, activity_col2 = st.columns([2, 1])

    with activity_col1:
        st.subheader("📊 Recent Activity")

        if st.session_state.day_log:
            # Show last 10 entries
            recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]

            for log in recent_logs:
                log_date = datetime.datetime.fromisoformat(log['date']).strftime("%m/%d/%Y")
                auto_text = " (Auto)" if log.get('auto_logged', False) else ""

                # Show property if available
                property_text = ""
                if 'user_properties' in st.session_state:
                    for prop_name, prop_details in st.session_state.user_properties.items():
                        if prop_details['state'] == log['state']:
                            property_text = f" @ {prop_name}"
                            break

                st.write(f"• {log_date}: {log['state']}{property_text}{auto_text}")
        else:
            st.info("No activity logged yet. Start by logging today's location!")

    with activity_col2:
        st.subheader("🎯 Current Status")

        for state, days in st.session_state.states.items():
            status, severity = data_manager.get_tax_status(days, state=state)
            # Get state-specific threshold
            state_threshold = data_manager.state_tax_thresholds.get(state, data_manager.tax_threshold)
            percentage = (days / state_threshold) * 100

            st.write(f"**{state}**: {days} days")
            st.write(f"Status: {status}")

            # Progress bar
            if severity == "status-safe":
                st.progress(min(percentage / 100, 1.0))
            elif severity == "status-warning":
                st.warning(f"⚠️ {percentage:.1f}% of threshold")
                st.progress(min(percentage / 100, 1.0))
            else:
                st.error(f"🚨 {percentage:.1f}% of threshold")
                st.progress(min(percentage / 100, 1.0))

            st.write("")  # Add spacing

    # Bulk Operations
    if st.session_state.day_log:
        st.markdown("---")
        st.subheader("🔧 Bulk Operations")

        bulk_col1, bulk_col2, bulk_col3 = st.columns(3)

        with bulk_col1:
            if st.button("📄 Export Log", use_container_width=True):
                # Create CSV export
                log_data = []
                for log in st.session_state.day_log:
                    log_data.append({
                        'Date': log['date'],
                        'State': log['state'],
                        'Auto Logged': log.get('auto_logged', False),
                        'Timestamp': log['timestamp']
                    })

                df = pd.DataFrame(log_data)
                csv = df.to_csv(index=False)

                st.download_button(
                    "⬇️ Download CSV",
                    data=csv,
                    file_name=f"snowbird_log_{datetime.date.today()}.csv",
                    mime="text/csv"
                )

        with bulk_col2:
            if st.button("🗑️ Clear All Logs", use_container_width=True):
                if st.button("⚠️ Confirm Delete All", key="confirm_delete_all"):
                    st.session_state.day_log = []
                    # Reset state counts
                    for state in st.session_state.states:
                        st.session_state.states[state] = 0
                    st.success("✅ All logs cleared!")
                    st.rerun()

        with bulk_col3:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation - navigate to Reports tab for detailed analysis")

    # State Management
    st.markdown("---")
    st.subheader("🗺️ State Management") 

    state_mgmt_col1, state_mgmt_col2 = st.columns(2)

    with state_mgmt_col1:
        st.write("**Add New State:**")
        new_state = st.text_input("State Name", placeholder="e.g., Florida, Texas", key="new_state_input")

        if st.button("➕ Add State") and new_state:
            if new_state not in st.session_state.states:
                st.session_state.states[new_state] = 0
                st.success(f"✅ Added {new_state} to tracking")
                st.rerun()
            else:
                st.warning(f"⚠️ {new_state} is already being tracked")

    with state_mgmt_col2:
        st.write("**Current States:**")
        for state, days in st.session_state.states.items():
            status, severity = data_manager.get_tax_status(days)
            color = "🟢" if severity == "status-safe" else "🟡" if severity == "status-warning" else "🔴"
            st.write(f"{color} {state}: {days} days ({status})")

    # Tips and Help
    if st.session_state.get('show_tips', True):
        st.markdown("---")
        with st.expander("💡 Tracking Tips"):
            st.markdown("""
            **Best Practices for Location Tracking:**

            🎯 **Daily Logging**: Log your location daily for accurate tax compliance

            📍 **Property Association**: Link your logs to specific properties for better organization

            ⚖️ **Tax Thresholds**: Monitor your progress toward the 183-day tax residency threshold

            📱 **Mobile Friendly**: Bookmark this page on your phone for easy daily logging

            🔄 **Backup Regularly**: Export your logs periodically as backup

            📊 **Review Reports**: Check the Reports tab monthly for detailed analysis
            """)

    # Auto-logging status
    if st.session_state.get('gmail_integration', False):
        st.info("📧 Gmail travel detection is enabled - some entries may be logged automatically")

    # Show recent changes notification
    if 'recent_property_changes' in st.session_state and st.session_state.recent_property_changes:
        st.success("✨ New properties detected! Your state options have been updated.")
        # Clear the notification
        st.session_state.recent_property_changes = False

def render_day_tracker():
    """Render the day tracking interface"""
    st.markdown('<h2><i data-lucide="calendar-days" class="icon"></i>Residency Day Tracker</h2>', unsafe_allow_html=True)
    st.markdown("*Track your daily locations for accurate tax residency management.* 📊")

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