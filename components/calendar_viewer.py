
"""
Google Calendar events viewer for Snowbird app.
"""

import streamlit as st
import datetime
from typing import List, Dict
from utils.google_calendar import calendar_sync

def render_calendar_events_viewer():
    """Render a viewer for Snowbird calendar events"""
    
    if not calendar_sync.is_authenticated():
        st.info("Connect to Google Calendar in Settings to view synced events")
        return
    
    st.subheader("📅 Your Snowbird Calendar Events")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "From Date",
            value=datetime.date.today() - datetime.timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "To Date", 
            value=datetime.date.today() + datetime.timedelta(days=30)
        )
    
    if st.button("🔍 Load Events"):
        try:
            # Get events from calendar
            events = calendar_sync.get_snowbird_events(start_date, end_date)
            
            if events:
                # Group events by type
                residency_events = [e for e in events if e['type'] == 'residency_log']
                reminder_events = [e for e in events if e['type'] == 'reminder']
                
                # Display residency logs
                if residency_events:
                    st.write("**🏠 Residency Day Logs:**")
                    for event in sorted(residency_events, key=lambda x: x['date'], reverse=True):
                        state_emoji = "🌵" if event.get('state') == 'Arizona' else "❄️"
                        st.write(f"{state_emoji} {event['title']} - {event['date']}")
                
                # Display reminders
                if reminder_events:
                    st.write("**🔔 Reminders:**")
                    for event in sorted(reminder_events, key=lambda x: x['date']):
                        reminder_type = event.get('reminder_type', 'general')
                        emoji = "💰" if reminder_type == 'bill' else "⚠️" if reminder_type == 'threshold' else "📋"
                        st.write(f"{emoji} {event['title']} - {event['date']}")
                
                st.success(f"Found {len(events)} Snowbird events in your calendar")
                
            else:
                st.info("No Snowbird events found in the selected date range")
                
        except Exception as e:
            st.error(f"Error loading calendar events: {e}")

def render_sync_status():
    """Render calendar sync status widget"""
    
    if calendar_sync.is_authenticated():
        st.success("📅 Google Calendar Connected")
        
        # Show sync preferences
        auto_sync = st.session_state.get('auto_calendar_sync', False)
        sync_reminders = st.session_state.get('sync_bill_reminders', False)
        
        status_text = []
        if auto_sync:
            status_text.append("✅ Auto-sync residency logs")
        if sync_reminders:
            status_text.append("✅ Sync bill reminders")
        
        if status_text:
            st.write("**Active sync settings:**")
            for setting in status_text:
                st.write(f"• {setting}")
        else:
            st.write("• Sync settings: Manual only")
            
    else:
        st.warning("📅 Google Calendar not connected")
        st.write("Connect in Settings to enable automatic syncing")
