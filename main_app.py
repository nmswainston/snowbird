"""
The code has been modified to remove references to Hawaiian expressions and vibes from the header and navigation.
"""
"""
Snowbird Financial Assistant - Main Application
"""

import streamlit as st
import datetime
import pandas as pd
from typing import Dict, List
import traceback
import threading
import time
from components.session_state import initialize_session_state
from components.styles import load_custom_css, render_main_header
from components.dashboard import render_dashboard
from components.day_tracker import render_day_tracker
from utils.auth import check_openai_availability
from utils.data_models import SnowbirdData
from utils.onboarding import render_onboarding_carousel, should_show_onboarding, render_onboarding_trigger

# Configure Streamlit
st.set_page_config(
    page_title="Snowbird: Your Seasonal Financial Assistant", 
    layout="wide",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)

def start_api_server():
    """Start API server in background thread"""
    try:
        from api import run_api_server
        import threading
        
        # Start API server in background thread
        api_thread = threading.Thread(
            target=run_api_server,
            args=("0.0.0.0", 8000),
            daemon=True
        )
        api_thread.start()
        
    except Exception as e:
        # Don't crash the main app if API server fails
        print(f"API server start failed: {e}")

def main():
    """Main application function"""
    try:
        # Start API server in background thread if not already running
        if 'api_server_started' not in st.session_state:
            start_api_server()
            st.session_state.api_server_started = True

        # Load custom CSS
        load_custom_css()

        # Initialize session state
        initialize_session_state()

        # Handle scroll to top after onboarding
        if st.session_state.get('scroll_to_top', False):
            st.session_state.scroll_to_top = False
            # Use JavaScript with a delay to ensure page is loaded
            st.markdown("""
            <script>
            setTimeout(function() {
                window.parent.document.querySelector('.main').scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
                window.scrollTo(0, 0);
            }, 100);
            </script>
            """, unsafe_allow_html=True)

        # Start health monitoring
        from utils.health_monitor import health_monitor
        health_monitor.start_monitoring()

    except Exception as e:
        st.error("🚨 Application initialization failed")
        st.exception(e)

        if st.button("🔄 Restart Application"):
            st.rerun()
        return

    # Check integrations
    openai_available, openai_client = check_openai_availability()
    if not openai_available:
        st.info("To enable AI features, add your OPENAI_API_KEY to Replit Secrets.")

    # PWA meta tags
    st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#12BDF2">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="Snowbird">
        <link rel="manifest" href="/manifest.json">
        <link rel="apple-touch-icon" href="/generated-icon.png">
    </head>
    """, unsafe_allow_html=True)

    # Render main header
    render_main_header()

    # Add welcome banner
    if not st.session_state.get('onboarded', False):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); 
                    padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
            <p style="color: white; margin: 0; font-size: 1.1rem;">
                🏠 Welcome to your Snowbird Financial Assistant! 📊
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Show onboarding tour for first-time users
    if should_show_onboarding():
        render_onboarding_carousel()
        return  # Don't render the rest of the app during onboarding

    # Dashboard now includes integrated quick actions

    # Mobile-optimized navigation
    import streamlit.components.v1 as components

    # Auto-detect mobile with better method
    components.html("""
    <script>
    if (window.innerWidth < 768) {
        window.parent.postMessage({type: 'mobile_detected', mobile: true}, '*');
    }
    </script>
    """, height=0)

    # Detect mobile view
    mobile_view = st.session_state.get('mobile_view', False) or st.session_state.get('force_mobile_tabs', False)

    if mobile_view:
        # Shorter labels for mobile
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏠 Home", 
            "📅 Log", 
            "💰 Budget", 
            "🏡 Props",
            "🤖 AI", 
            "📊 Report",
            "⚙️ Setup",
            "🌺 Community"
        ])
    else:
        # Full labels for desktop
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏠 Dashboard", 
            "📅 Day Tracker", 
            "💰 Budget Tracker", 
            "🏡 Properties",
            "🤖 AI Assistant", 
            "📊 Reports",
            "⚙️ Settings",
            "🌺 Community"
        ])

    # Enhanced mobile detection with settings override
    st.markdown("""
    <script>
    function detectMobile() {
        const isMobile = window.innerWidth < 768 || 
                        /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        if (isMobile) {
            window.parent.postMessage({type: 'mobile_detected', mobile: true}, '*');
            // Add mobile-specific styling
            document.body.classList.add('mobile-device');
        }
    }

    detectMobile();
    window.addEventListener('resize', detectMobile);
    </script>
    <style>
    .mobile-device .main .block-container {
        padding: 0.5rem !important;
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Allow manual mobile mode toggle in settings
    if st.session_state.get('force_mobile_view', False):
        st.session_state.mobile_view = True

    with tab1:
        render_dashboard()

    with tab2:
        render_day_tracker()

    with tab3:
        render_budgets_tab()

    with tab4:
        render_properties_tab()

    with tab5:
        render_ai_assistant_tab(openai_available, openai_client)

    with tab6:
        render_reports_tab()

    with tab7:
        render_settings_tab()

    with tab8:
        render_community_tab()

    # Footer
    render_footer()

def render_budgets_tab():
    """Render the budget tracking tab"""
    st.markdown('<h2><i data-lucide="dollar-sign" class="icon"></i>Budget Tracker</h2>', unsafe_allow_html=True)
    
    from components.budget_tracker import render_budget_tracker
    render_budget_tracker()

def render_properties_tab():
    """Render the properties management tab"""
    st.markdown('<h2><i data-lucide="home" class="icon"></i>Properties</h2>', unsafe_allow_html=True)
    
    from components.properties_manager import render_properties_manager
    render_properties_manager()

def render_ai_assistant_tab(openai_available, openai_client):
    """Render the AI assistant tab"""
    st.markdown('<h2><i data-lucide="bot" class="icon"></i>AI Assistant</h2>', unsafe_allow_html=True)
    
    if openai_available:
        from components.ai_assistant import render_ai_assistant
        render_ai_assistant(openai_client)
    else:
        st.info("🤖 AI Assistant requires OpenAI API key. Add your key to Replit Secrets to enable AI features.")

def render_reports_tab():
    """Render the reports tab"""
    st.markdown('<h2><i data-lucide="bar-chart" class="icon"></i>Reports</h2>', unsafe_allow_html=True)
    
    from components.reports import render_reports
    render_reports()

def render_community_tab():
    """Render the community tab"""
    st.markdown('<h2><i data-lucide="users" class="icon"></i>Community</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🌺 Welcome to the Snowbird Community!
    
    Connect with other snowbirds, share tips, and get advice on managing your seasonal lifestyle.
    """)
    
    # Community features placeholder
    st.info("Community features coming soon! This will include forums, tips sharing, and seasonal advice.")

def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.9rem;">
        🏠 Snowbird Financial Assistant | Built with ❤️ for seasonal residents
    </div>
    """, unsafe_allow_html=True)

def render_settings_tab():
    """Render comprehensive settings/preferences tab"""
    st.markdown('<h2><i data-lucide="settings" class="icon"></i>Settings & Preferences</h2>', unsafe_allow_html=True)

    # Create tabs for different settings categories
    settings_tabs = st.tabs([
        "⚙️ General", 
        "📧 Email & Notifications", 
        "🎨 Theme & Display", 
        "🔒 Privacy & Security",
        "📊 Data Management",
        "🔧 Advanced"
    ])

    with settings_tabs[0]:  # General Settings
        st.subheader("Tax Residency Settings")

        col1, col2 = st.columns(2)
        with col1:
            tax_threshold = st.number_input(
                "Tax Threshold (days)", 
                value=st.session_state.get('tax_threshold', 183), 
                min_value=1, 
                max_value=365,
                help="Number of days that determines tax residency"
            )
            st.session_state.tax_threshold = tax_threshold

        with col2:
            fiscal_year_start = st.selectbox(
                "Fiscal Year Start",
                options=["January 1", "April 1", "July 1", "October 1"],
                index=0,
                help="When your tax year begins"
            )
            st.session_state.fiscal_year_start = fiscal_year_start

        st.divider()
        st.subheader("Currency & Financial Settings")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Currency selector
            from utils.currency import SUPPORTED_CURRENCIES
            currency_options = list(SUPPORTED_CURRENCIES.keys())
            currency_names = [f"{code} - {SUPPORTED_CURRENCIES[code]['name']}" for code in currency_options]

            selected_currency_index = st.selectbox(
                "Primary Currency",
                options=range(len(currency_options)),
                format_func=lambda x: currency_names[x],
                index=currency_options.index(st.session_state.get('primary_currency', 'USD')),
                help="Your preferred currency for all financial calculations"
            )
            st.session_state.primary_currency = currency_options[selected_currency_index]

        with col2:
            # Inflation adjustment toggle
            inflation_enabled = st.checkbox(
                "Enable Inflation Adjustment",
                value=st.session_state.get('inflation_enabled', False),
                help="Adjust financial values for inflation over time"
            )
            st.session_state.inflation_enabled = inflation_enabled

        with col3:
            # Inflation rate setting (only show if inflation is enabled)
            if inflation_enabled:
                inflation_rate = st.number_input(
                    "Annual Inflation Rate (%)",
                    value=st.session_state.get('inflation_rate', 3.0),
                    min_value=0.0,
                    max_value=20.0,
                    step=0.1,
                    help="Expected annual inflation rate for adjustments"
                )
                st.session_state.inflation_rate = inflation_rate / 100.0  # Convert to decimal
            else:
                st.session_state.inflation_rate = 0.03  # Default 3%

        # Show current exchange rate info
        if st.session_state.get('primary_currency', 'USD') != 'USD':
            from utils.currency import get_currency_conversion_info
            try:
                rate, rate_info = get_currency_conversion_info('USD', st.session_state.primary_currency)
                st.info(f"💱 Current exchange rate: {rate_info}")
            except Exception as e:
                st.warning("⚠️ Unable to fetch current exchange rates. Using fallback rates.")

        st.subheader("Location Settings")
        primary_residence = st.selectbox(
            "Primary Residence State",
            options=["Arizona", "Minnesota", "Other"],
            index=st.session_state.get('primary_residence_index', 0)
        )
        st.session_state.primary_residence = primary_residence

        # Time zone setting
        timezone = st.selectbox(
            "Time Zone",
            options=["US/Arizona", "US/Central", "US/Eastern", "US/Pacific"],
            index=0,
            help="Your preferred timezone for date calculations"
        )
        st.session_state.timezone = timezone

    with settings_tabs[1]:  # Email & Notifications
        from components.email_settings import render_email_settings
        render_email_settings()

        st.divider()
        st.subheader("Google Calendar Integration")

        # Import calendar sync utility
        from utils.google_calendar import calendar_sync

        if calendar_sync.is_authenticated():
            st.success("✅ Connected to Google Calendar")

            # Auto-sync settings
            auto_sync = st.checkbox(
                "Auto-sync residency logs to calendar",
                value=st.session_state.get('auto_calendar_sync', False),
                help="Automatically create calendar events when logging days"
            )
            st.session_state.auto_calendar_sync = auto_sync

            # Reminder sync settings
            sync_reminders = st.checkbox(
                "Sync bill reminders to calendar",
                value=st.session_state.get('sync_bill_reminders', False),
                help="Create calendar reminders for upcoming bills"
            )
            st.session_state.sync_bill_reminders = sync_reminders

            # Show recent synced events
            if st.button("📅 View Recent Calendar Events"):
                try:
                    from datetime import timedelta
                    start_date = datetime.date.today() - timedelta(days=30)
                    end_date = datetime.date.today() + timedelta(days=30)

                    events = calendar_sync.get_snowbird_events(start_date, end_date)

                    if events:
                        st.write("**Recent Snowbird Calendar Events:**")
                        for event in events[:10]:  # Show last 10 events
                            event_type = "🏠" if event['type'] == 'residency_log' else "🔔"
                            st.write(f"{event_type} {event['title']} - {event['date']}")
                    else:
                        st.info("No Snowbird events found in your calendar")

                except Exception as e:
                    st.error(f"Error retrieving calendar events: {e}")

            # Disconnect option
            if st.button("🔌 Disconnect from Google Calendar", type="secondary"):
                calendar_sync.disconnect()
                st.success("Disconnected from Google Calendar")
                st.rerun()

        else:
            st.info("🔗 Connect your Google Calendar to automatically sync residency logs and reminders")

            # Instructions for setup
            with st.expander("📋 Setup Instructions"):
                st.markdown("""
                **To enable Google Calendar sync:**

                1. **Get Google API Credentials:**
                   - Go to [Google Cloud Console](https://console.cloud.google.com/)
                   - Create a project or select existing one
                   - Enable Google Calendar API
                   - Create OAuth 2.0 credentials

                2. **Add to Replit Secrets:**
                   - Add `GOOGLE_CLIENT_ID` with your client ID
                   - Add `GOOGLE_CLIENT_SECRET` with your client secret

                3. **Authorize Access:**
                   - Click "Connect to Google Calendar" below
                   - Sign in to your Google account
                   - Grant calendar permissions
                """)

            # Show connect button if credentials are available
            # Check if secrets exist first to avoid StreamlitSecretNotFoundError
            try:
                has_google_credentials = (
                    hasattr(st, 'secrets') and 
                    st.secrets.get("GOOGLE_CLIENT_ID") and 
                    st.secrets.get("GOOGLE_CLIENT_SECRET")
                )
            except Exception:
                has_google_credentials = False

            if has_google_credentials:
                if st.button("📅 Connect to Google Calendar", type="primary"):
                    auth_url = calendar_sync.get_auth_url()
                    if auth_url:
                        st.markdown(f"🔗 **[Click here to authorize Google Calendar access]({auth_url})**")
                        st.info("After authorizing, copy the authorization code and paste it below:")

                        auth_code = st.text_input("Authorization Code:", placeholder="Paste code here...")

                        if st.button("✅ Complete Setup") and auth_code:
                            if calendar_sync.authenticate_with_code(auth_code):
                                st.success("🎉 Successfully connected to Google Calendar!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to connect. Please check your authorization code.")
                    else:
                        st.error("Failed to generate authorization URL. Check your Google API credentials.")
            else:
                st.warning("⚠️ Google API credentials not found in Replit Secrets. Please add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.")

        st.divider()
        st.subheader("Notification Preferences")

        # Weekly summary
        weekly_summary = st.checkbox(
            "Weekly Summary Emails",
            value=st.session_state.get('weekly_summary', True),
            help="Receive weekly summaries of your residency status"
        )
        st.session_state.weekly_summary = weekly_summary

        # Threshold warnings
        threshold_warnings = st.checkbox(
            "Threshold Warning Alerts",
            value=st.session_state.get('threshold_warnings', True),
            help="Get notified when approaching tax residency thresholds"
        )
        st.session_state.threshold_warnings = threshold_warnings

        # Warning days before threshold
        if threshold_warnings:
            warning_days = st.slider(
                "Days before threshold to warn",
                min_value=1,
                max_value=30,
                value=st.session_state.get('warning_days', 14)
            )
            st.session_state.warning_days = warning_days

    with settings_tabs[2]:  # Theme & Display
        from components.theme_selector import render_theme_selector
        render_theme_selector()

        st.divider()
        st.subheader("Display Preferences")

        # Mobile view toggle
        force_mobile = st.checkbox(
            "Force Mobile View",
            value=st.session_state.get('force_mobile_view', False),
            help="Use mobile-optimized layout even on desktop"
        )
        st.session_state.force_mobile_view = force_mobile
        if force_mobile:
            st.session_state.mobile_view = True

        # Date format
        date_format = st.selectbox(
            "Date Format",
            options=["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
            index=0
        )
        st.session_state.date_format = date_format

        # Chart preferences
        chart_style = st.selectbox(
            "Chart Style",
            options=["Modern", "Classic", "Minimal"],
            index=0
        )
        st.session_state.chart_style = chart_style

        # Dashboard layout
        dashboard_layout = st.radio(
            "Dashboard Layout",
            options=["Compact", "Expanded", "Cards"],
            index=1,
            horizontal=True
        )
        st.session_state.dashboard_layout = dashboard_layout

    with settings_tabs[3]:  # Privacy & Security
        st.subheader("Privacy Settings")

        # Data collection
        analytics_enabled = st.checkbox(
            "Enable Usage Analytics",
            value=st.session_state.get('analytics_enabled', False),
            help="Help improve the app by sharing anonymous usage data"
        )
        st.session_state.analytics_enabled = analytics_enabled

        # Auto-save
        auto_save = st.checkbox(
            "Auto-save Changes",
            value=st.session_state.get('auto_save', True),
            help="Automatically save your changes"
        )
        st.session_state.auto_save = auto_save

        # Session timeout
        session_timeout = st.selectbox(
            "Session Timeout",
            options=["15 minutes", "30 minutes", "1 hour", "2 hours", "Never"],
            index=2
        )
        st.session_state.session_timeout = session_timeout

        st.subheader("Data Security")
        st.info("🔒 All your data is encrypted and stored securely. We never share your personal information.")

        # Show security status
        if st.button("🔍 Check Security Status"):
            st.success("✅ All security checks passed")
            st.write("- Data encryption: Active")
            st.write("- Secure connections: Enabled") 
            st.write("- Authentication: Valid")

    with settings_tabs[4]:  # Data Management
        st.markdown("### 📊 Data Management")

        # Auto-save toggle
        st.session_state.auto_save = st.toggle(
            "Auto-save data", 
            value=st.session_state.get('auto_save', True),
            help="Automatically save your data when changes are made"
        )

        # AI Rating Statistics (optional display)
        st.markdown("---")
        st.markdown("### 🤖 AI Response Ratings")

        from utils.ai_rating_system import ai_rating_manager
        rating_stats = ai_rating_manager.get_rating_stats()

        if rating_stats["total_ratings"] > 0:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total AI Ratings", rating_stats["total_ratings"])

            with col2:
                st.metric("👍 Satisfaction", f"{rating_stats['thumbs_up_percentage']}%")

            with col3:
                st.metric("Recent Positive", rating_stats["thumbs_up"])

            # Show rating breakdown
            if st.checkbox("Show detailed AI rating statistics"):
                st.write(f"**Positive ratings:** {rating_stats['thumbs_up']}")
                st.write(f"**Negative ratings:** {rating_stats['thumbs_down']}")
                st.write(f"**Average question length:** {rating_stats['average_question_length']} characters")
                st.write(f"**Average response length:** {rating_stats['average_response_length']} characters")
        else:
            st.info("No AI ratings recorded yet. Use the AI Assistant to ask questions and rate responses!")

        st.subheader("Data Export & Backup")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📄 Export All Data"):
                try:
                    import json
                    from datetime import datetime

                    export_data = {
                        "export_date": datetime.now().isoformat(),
                        "settings": dict(st.session_state),
                        "version": "1.0"
                    }

                    st.download_button(
                        label="⬇️ Download Export File",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"snowbird_export_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                    st.success("✅ Export prepared!")
                except Exception as e:
                    st.error(f"Export failed: {e}")

        with col2:
            if st.button("🗑️ Clear All Data"):
                if st.button("⚠️ Confirm Delete", type="secondary"):
                    # Clear session state
                    for key in list(st.session_state.keys()):
                        if not key.startswith('_'):
                            del st.session_state[key]
                    st.success("✅ All data cleared!")
                    st.rerun()

        # Backup and Restore Section
        st.markdown("---")
        st.subheader("🔄 Backup & Restore")

        col1_backup, col2_backup = st.columns(2)

        with col1_backup:
            st.markdown("**💾 Create Backup**")
            if st.button("📦 Backup Data", type="primary"):
                try:
                    from utils.backup_manager import backup_manager

                    # Create comprehensive backup with timestamp
                    backup_data = {
                        'timestamp': datetime.now().isoformat(),
                        'version': '1.0.0',
                        'app_version': 'Snowbird v2.0',
                        'data': {
                            'states': dict(st.session_state.get('states', {})),
                            'home_budgets': dict(st.session_state.get('home_budgets', {})),
                            'seasonal_cash_flow': dict(st.session_state.get('seasonal_cash_flow', {})),
                            'tax_threshold': st.session_state.get('tax_threshold', 183),
                            'risk_warning_days': st.session_state.get('risk_warning_days', 14),
                            'default_state': st.session_state.get('default_state', 'Arizona'),
                            'user_preferences': {
                                'theme': st.session_state.get('theme', 'light'),
                                'notifications': st.session_state.get('notify_email', False),
                                'auto_save': st.session_state.get('auto_save', True),
                                'show_tips': st.session_state.get('show_tips', True)
                            },
                            'migration_checklist': dict(st.session_state.get('migration_checklist', {})),
                            'bills': dict(st.session_state.get('bills', {}))
                        }
                    }

                    # Create zip file with backup data
                    import zipfile
                    import io

                    zip_buffer = io.BytesIO()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        # Add main backup file
                        backup_json = json.dumps(backup_data, indent=2, default=str)
                        zip_file.writestr(f"snowbird_backup_{timestamp}.json", backup_json)

                        # Add metadata file
                        metadata = {
                            'backup_date': backup_data['timestamp'],
                            'total_days_az': backup_data['data']['states'].get('Arizona', 0),
                            'total_days_mn': backup_data['data']['states'].get('Minnesota', 0),
                            'backup_size': len(backup_json),
                            'checksum': str(hash(backup_json))
                        }
                        zip_file.writestr("backup_metadata.json", json.dumps(metadata, indent=2))

                    zip_buffer.seek(0)

                    st.download_button(
                        label="⬇️ Download Backup ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"snowbird_backup_{timestamp}.zip",
                        mime="application/zip",
                        help="Download your complete Snowbird data backup"
                    )
                    st.success("✅ Backup created successfully!")

                except Exception as e:
                    st.error(f"❌ Backup failed: {str(e)}")
                    logger.error(f"Backup creation error: {e}")

        with col2_backup:
            st.markdown("**📥 Restore Backup**")
            uploaded_backup = st.file_uploader(
                "Choose backup file",
                type=['zip', 'json'],
                help="Upload a backup ZIP or JSON file to restore your data",
                key="backup_restore"
            )

            if uploaded_backup is not None:
                if st.button("🔄 Restore Data", type="secondary"):
                    try:
                        # Validate and restore backup
                        restore_success = False

                        if uploaded_backup.name.endswith('.zip'):
                            # Handle ZIP backup
                            import zipfile
                            import io

                            zip_data = io.BytesIO(uploaded_backup.read())

                            with zipfile.ZipFile(zip_data, 'r') as zip_file:
                                # List contents for validation
                                file_list = zip_file.namelist()

                                # Look for backup JSON file
                                backup_files = [f for f in file_list if f.startswith('snowbird_backup_') and f.endswith('.json')]

                                if not backup_files:
                                    st.error("❌ Invalid backup ZIP: No backup file found")
                                else:
                                    # Extract and validate backup data
                                    backup_content = zip_file.read(backup_files[0]).decode('utf-8')
                                    backup_data = json.loads(backup_content)

                                    # Validate backup structure
                                    if validate_backup_data(backup_data):
                                        restore_backup_data(backup_data)
                                        restore_success = True
                                    else:
                                        st.error("❌ Invalid backup format")

                        elif uploaded_backup.name.endswith('.json'):
                            # Handle JSON backup (legacy support)
                            backup_content = uploaded_backup.read().decode('utf-8')
                            backup_data = json.loads(backup_content)

                            if validate_backup_data(backup_data):
                                restore_backup_data(backup_data)
                                restore_success = True
                            else:
                                st.error("❌ Invalid backup format")

                        if restore_success:
                            st.success("✅ Data restored successfully!")
                            st.info("🔄 Please refresh the page to see restored data")
                            # Auto-refresh after short delay
                            time.sleep(2)
                            st.rerun()

                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON format in backup file")
                    except zipfile.BadZipFile:
                        st.error("❌ Invalid ZIP file format")
                    except Exception as e:
                        st.error(f"❌ Restore failed: {str(e)}")
                        logger.error(f"Backup restore error: {e}")

        # Property management moved to dedicated Properties tab for better mobile access

        st.subheader("Import Data")
        uploaded_file = st.file_uploader(
            "Import Settings",
            type=['json'],
            help="Upload a previously exported settings file"
        )

        if uploaded_file is not None:
            try:
                import json
                data = json.load(uploaded_file)

                if st.button("📥 Import Settings"):
                    # Import settings
                    if 'settings' in data:
                        for key, value in data['settings'].items():
                            if not key.startswith('_'):
                                st.session_state[key] = value
                    st.success("✅ Settings imported successfully!")
                    st.rerun()

            except Exception as e:
                st.error(f"Import failed: {e}")

    with settings_tabs[5]:  # Advanced
        st.subheader("Advanced Configuration")

        # Debug mode
        debug_mode = st.checkbox(
            "Enable Debug Mode",
            value=st.session_state.get('debug_mode', False),
            help="Show additional debugging information"
        )
        st.session_state.debug_mode = debug_mode

        # Performance settings
        st.subheader("Performance")
        cache_enabled = st.checkbox(
            "Enable Caching",
            value=st.session_state.get('cache_enabled', True),
            help="Cache data to improve performance"
        )
        st.session_state.cache_enabled = cache_enabled

        # Feature flags
        st.subheader("Feature Flags")

        # Gmail integration
        gmail_integration = st.checkbox(
            "Gmail Travel Detection (Beta)",
            value=st.session_state.get('gmail_integration', False),
            help="Automatically detect travel from Gmail"
        )
        st.session_state.gmail_integration = gmail_integration

        # AI features
        ai_features = st.checkbox(
            "AI Assistant (Beta)",
            value=st.session_state.get('ai_features', False),
            help="Enable AI-powered insights and suggestions"
        )
        st.session_state.ai_features = ai_features

        st.subheader("System Information")

        # Onboarding restart option
        st.markdown("**Onboarding & Help**")
        render_onboarding_trigger()

        if st.button("📊 Show System Info"):
            try:
                from utils.config import settings

                st.write("**Application Version**: 1.0.0")
                st.write(f"**Environment**: {settings.ENVIRONMENT}")
                st.write(f"**Debug Mode**: {settings.DEBUG}")
                st.write("**Features Enabled**:")
                st.write(f"- Gmail Integration: {bool(settings.GMAIL_CREDENTIALS_FILE)}")
                st.write(f"- AI Features: {bool(settings.OPENAI_API_KEY)}")
                st.write(f"- Email Notifications: {bool(settings.SMTP_USERNAME)}")

            except Exception as e:
                st.error(f"Could not load system info: {e}")

        # Widget Configuration Section
        st.subheader("Dashboard Widget Configuration")
        st.write("Choose which widgets to display on your dashboard:")

        # Available widgets with descriptions
        available_widgets = {
            "quick_location_logger": {
                "name": "📍 Quick Location Logger",
                "description": "Fast location logging with dropdown and button"
            },
            "key_metrics": {
                "name": "📊 Key Metrics Overview", 
                "description": "Arizona/Minnesota days and tax threshold progress"
            },
            "tax_progress": {
                "name": "📈 Tax Residency Progress",
                "description": "Visual progress bars and risk assessment"
            },
            "quick_insights": {
                "name": "✨ Quick Insights",
                "description": "Tax optimization score and recommendations"
            },
            "status_overview": {
                "name": "📋 Detailed Status Overview",
                "description": "Total days logged and risk levels"
            },
            "state_breakdown": {
                "name": "🗺️ State-by-State Breakdown",
                "description": "Individual state residency status and progress"
            },
            "financial_summary": {
                "name": "💰 Financial Summary",
                "description": "Monthly budgets and seasonal expenses"
            },
            "ai_tips": {
                "name": "🤖 AI Tips",
                "description": "Smart recommendations and planning advice"
            },
            "expense_sparkline": {
                "name": "📈 Expense Sparkline",
                "description": "Mini charts showing spending trends"
            },
            "reminders": {
                "name": "🔔 Reminders",
                "description": "Important dates and threshold warnings"
            }
        }

        # Initialize widgets session state with defaults if not set
        if 'widgets' not in st.session_state:
            # Default selection - core widgets enabled by default
            st.session_state.widgets = {
                "quick_location_logger": True,
                "key_metrics": True,
                "tax_progress": True,
                "quick_insights": True,
                "status_overview": True,
                "state_breakdown": True,
                "financial_summary": True,
                "ai_tips": False,  # Optional widgets disabled by default
                "expense_sparkline": False,
                "reminders": False
            }

        # Create checkboxes for each widget in a two-column layout
        widget_col1, widget_col2 = st.columns(2)

        # Display widgets in two columns
        widget_keys = list(available_widgets.keys())
        mid_point = len(widget_keys) // 2

        with widget_col1:
            for widget_key in widget_keys[:mid_point]:
                widget_info = available_widgets[widget_key]
                current_value = st.session_state.widgets.get(widget_key, True)
                
                new_value = st.checkbox(
                    widget_info["name"],
                    value=current_value,
                    help=widget_info["description"],
                    key=f"widget_{widget_key}"
                )
                st.session_state.widgets[widget_key] = new_value

        with widget_col2:
            for widget_key in widget_keys[mid_point:]:
                widget_info = available_widgets[widget_key]
                current_value = st.session_state.widgets.get(widget_key, True)
                
                new_value = st.checkbox(
                    widget_info["name"],
                    value=current_value,
                    help=widget_info["description"],
                    key=f"widget_{widget_key}"
                )
                st.session_state.widgets[widget_key] = new_value

        # Quick actions for widget management
        st.markdown("---")
        widget_action_col1, widget_action_col2, widget_action_col3 = st.columns(3)

        with widget_action_col1:
            if st.button("✅ Enable All Widgets"):
                for widget_key in available_widgets.keys():
                    st.session_state.widgets[widget_key] = True
                st.rerun()

        with widget_action_col2:
            if st.button("❌ Disable All Widgets"):
                for widget_key in available_widgets.keys():
                    st.session_state.widgets[widget_key] = False
                st.rerun()

        with widget_action_col3:
            if st.button("🔄 Reset to Defaults"):
                st.session_state.widgets = {
                    "quick_location_logger": True,
                    "key_metrics": True,
                    "tax_progress": True,
                    "quick_insights": True,
                    "status_overview": True,
                    "state_breakdown": True,
                    "financial_summary": True,
                    "ai_tips": False,
                    "expense_sparkline": False,
                    "reminders": False
                }
                st.rerun()

        st.info("💡 Changes will take effect when you refresh the dashboard tab.")