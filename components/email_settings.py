
import streamlit as st
from utils.email_notifications import send_test_email
from utils.logging_config import logger

def render_email_settings():
    """Render email notification settings in the app"""
    
    st.subheader("📧 Email Notifications")
    
    with st.container():
        # Email address input
        user_email = st.text_input(
            "Your Email Address",
            value=st.session_state.get('user_email', ''),
            placeholder="Enter your email for daily summaries",
            help="We'll send you daily residency status updates"
        )
        
        if user_email:
            st.session_state.user_email = user_email
        
        # Email notifications toggle
        email_enabled = st.checkbox(
            "Enable Daily Email Summaries",
            value=st.session_state.get('email_notifications', False),
            help="Receive daily emails with your residency status and days remaining"
        )
        st.session_state.email_notifications = email_enabled
        
        # Daily email time selector
        if email_enabled:
            daily_time = st.time_input(
                "Daily Email Time",
                value=st.session_state.get('daily_email_time', '09:00'),
                help="What time would you like to receive your daily summary?"
            )
            st.session_state.daily_email_time = daily_time.strftime('%H:%M')
            
            # Test email button
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("📮 Send Test Email", type="secondary"):
                    if user_email:
                        with st.spinner("Sending test email..."):
                            success = send_test_email(user_email)
                            if success:
                                st.success("✅ Test email sent successfully!")
                            else:
                                st.error("❌ Failed to send test email. Check your email settings.")
                    else:
                        st.warning("Please enter your email address first.")
            
            with col2:
                if st.button("💾 Save Settings", type="primary"):
                    # Save settings to session state or database
                    st.success("✅ Email settings saved!")
                    st.rerun()
        
        # Email preview section
        if email_enabled and user_email:
            with st.expander("📋 Email Preview", expanded=False):
                st.markdown("**Daily email will include:**")
                st.markdown("- 🌵 Arizona: Days spent and percentage of threshold")
                st.markdown("- ❄️ Minnesota: Days spent and percentage of threshold") 
                st.markdown("- 🚨 Tax residency status for each state")
                st.markdown("- 📊 Days remaining before reaching thresholds")
                st.markdown("- 💡 Helpful tips and reminders")
        
        # SMTP Configuration (for admin users)
        with st.expander("🔧 SMTP Configuration (Advanced)", expanded=False):
            st.markdown("**Note:** These settings are configured via environment variables:")
            st.code("""
# Required environment variables:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587  
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
DAILY_REMINDER_TIME=09:00
            """)
            
            st.info("💡 For Gmail, use an App Password instead of your regular password. Enable 2-factor authentication first.")
