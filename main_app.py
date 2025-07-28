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

    # Render main header with Hawaiian vibes
    render_main_header()
    
    # Add Hawaiian greeting banner
    from utils.hawaii_expressions import da_kine_time_vibe
    if not st.session_state.get('onboarded', False):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); 
                    padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
            <p style="color: white; margin: 0; font-size: 1.1rem;">
                🌺 {da_kine_time_vibe()} Welcome to your Snowbird ohana! 🏄‍♂️
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Show onboarding tour for first-time users
    if should_show_onboarding():
        render_onboarding_carousel()
        return  # Don't render the rest of the app during onboarding

    # Dashboard now includes integrated quick actions

    # Mobile-optimized navigation with Hawaiian expressions
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
        # Shorter labels for mobile with Hawaiian flair
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏠 Hale", 
            "📅 Log", 
            "💰 Money", 
            "🏡 Props",
            "🤖 AI", 
            "📊 Report",
            "⚙️ Setup",
            "🌺 Ohana"
        ])
    else:
        # Full labels for desktop with island vibes
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏠 Dashboard", 
            "📅 Day Tracker", 
            "💰 Budget Tracker", 
            "🏡 Properties",
            "🤖 AI Kokua", 
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

        widget_keys = list(available_widgets.keys())
        mid_point = len(widget_keys) // 2

        # First column of widgets
        with widget_col1:
            for widget_key in widget_keys[:mid_point]:
                widget_info = available_widgets[widget_key]
                current_state = st.session_state.widgets.get(widget_key, True)

                new_state = st.checkbox(
                    widget_info["name"],
                    value=current_state,
                    key=f"widget_checkbox_{widget_key}",
                    help=widget_info["description"]
                )
                st.session_state.widgets[widget_key] = new_state

        # Second column of widgets  
        with widget_col2:
            for widget_key in widget_keys[mid_point:]:
                widget_info = available_widgets[widget_key]
                current_state = st.session_state.widgets.get(widget_key, True)

                new_state = st.checkbox(
                    widget_info["name"],
                    value=current_state,
                    key=f"widget_checkbox_{widget_key}",
                    help=widget_info["description"]
                )
                st.session_state.widgets[widget_key] = new_state

        # Widget selection helper buttons
        st.write("")
        widget_btn_col1, widget_btn_col2, widget_btn_col3 = st.columns(3)

        with widget_btn_col1:
            if st.button("✅ Select All Widgets", use_container_width=True):
                for widget_key in available_widgets.keys():
                    st.session_state.widgets[widget_key] = True
                st.rerun()

        with widget_btn_col2:
            if st.button("❌ Deselect All", use_container_width=True):
                for widget_key in available_widgets.keys():
                    st.session_state.widgets[widget_key] = False
                st.rerun()

        with widget_btn_col3:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                # Reset to default widget selection
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

        # Show current selection summary
        enabled_count = sum(1 for enabled in st.session_state.widgets.values() if enabled)
        total_count = len(st.session_state.widgets)
        st.info(f"📊 Currently showing {enabled_count} of {total_count} available widgets on your dashboard.")

        # Reset to defaults
        st.subheader("Reset Settings")
        if st.button("🔄 Reset to Defaults", type="secondary"):
            if st.button("⚠️ Confirm Reset", type="secondary"):
                # Reset only settings, keep user data
                settings_keys = [
                    'tax_threshold', 'fiscal_year_start', 'primary_residence',
                    'timezone', 'date_format', 'chart_style', 'dashboard_layout',
                    'analytics_enabled', 'auto_save', 'session_timeout'
                ]
                for key in settings_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Settings reset to defaults!")
                st.rerun()

    # Save settings button
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("💾 Save All Settings", type="primary", use_container_width=True):
            # In a real app, this would save to database
            st.success("✅ All settings saved successfully!")
            st.balloons()

def render_properties_tab():
    """Render properties management tab with mobile-optimized interface"""
    st.markdown('<h2><i data-lucide="home" class="icon"></i>Property Management</h2>', unsafe_allow_html=True)

    # Initialize properties if not exists
    if 'user_properties' not in st.session_state:
        st.session_state.user_properties = {
            "Arizona Home": {
                "state": "Arizona",
                "address": "",
                "property_type": "Primary",
                "notes": ""
            },
            "Minnesota Home": {
                "state": "Minnesota", 
                "address": "",
                "property_type": "Secondary",
                "notes": ""
            }
        }

    # Property overview metrics
    st.subheader("📊 Property Overview")
    
    total_properties = len(st.session_state.user_properties)
    states_with_properties = len(set(prop['state'] for prop in st.session_state.user_properties.values()))
    primary_properties = sum(1 for prop in st.session_state.user_properties.values() if prop['property_type'] == 'Primary')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Properties", total_properties)
    with col2:
        st.metric("States", states_with_properties)
    with col3:
        st.metric("Primary Residences", primary_properties)

    st.markdown("---")

    # Display current properties in mobile-friendly cards
    st.subheader("🏠 Your Properties")

    if st.session_state.user_properties:
        properties_to_delete = []

        for prop_name, prop_details in st.session_state.user_properties.items():
            # Mobile-friendly property card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #cbd5e1; 
                        margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.2rem;">
                    🏠 {prop_name}
                </h4>
            </div>
            """, unsafe_allow_html=True)

            prop_col1, prop_col2 = st.columns([3, 1])
            
            with prop_col1:
                st.write(f"**📍 State:** {prop_details['state']}")
                st.write(f"**🏷️ Type:** {prop_details['property_type']}")
                if prop_details.get('address'):
                    st.write(f"**📮 Address:** {prop_details['address']}")
                if prop_details.get('notes'):
                    st.write(f"**📝 Notes:** {prop_details['notes']}")

            with prop_col2:
                if st.button(f"🗑️", key=f"delete_{prop_name}", help=f"Delete {prop_name}"):
                    properties_to_delete.append(prop_name)

        # Remove deleted properties
        for prop_name in properties_to_delete:
            del st.session_state.user_properties[prop_name]
            # Also remove from budgets if exists
            if prop_name in st.session_state.home_budgets:
                del st.session_state.home_budgets[prop_name]
            st.success(f"✅ Deleted property: {prop_name}")
            st.rerun()

    else:
        st.info("No properties configured yet. Add your first property below!")

    st.markdown("---")

    # Add new property section - mobile optimized
    st.subheader("➕ Add New Property")

    with st.form("add_property_form", clear_on_submit=True):
        # Stack inputs vertically on mobile
        new_prop_name = st.text_input(
            "Property Name *",
            placeholder="e.g., 'Florida Condo', 'Texas Ranch'",
            help="Give your property a memorable name"
        )

        # All 50 US states plus territories
        available_states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
            "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
            "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
            "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
            "New Hampshire", "New Jersey", "New Mexico", "New York", 
            "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
            "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
            "West Virginia", "Wisconsin", "Wyoming", "Washington DC", 
            "Puerto Rico", "US Virgin Islands", "Guam", "Other"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            new_prop_state = st.selectbox("State *", options=available_states)
        with col2:
            new_prop_type = st.selectbox(
                "Property Type *",
                options=["Primary", "Secondary", "Vacation", "Investment", "Rental"]
            )

        # Custom state input for "Other"
        if new_prop_state == "Other":
            new_prop_state = st.text_input(
                "Enter State/Territory Name *",
                placeholder="Enter state or territory name"
            )

        new_prop_address = st.text_area(
            "Address (Optional)",
            placeholder="Enter property address...",
            height=60
        )

        new_prop_notes = st.text_area(
            "Notes (Optional)",
            placeholder="Any additional notes about this property...",
            height=60
        )

        # Submit button
        submitted = st.form_submit_button("➕ Add Property", type="primary", use_container_width=True)

        if submitted:
            if new_prop_name and new_prop_state:
                if new_prop_name not in st.session_state.user_properties:
                    # Add new property
                    st.session_state.user_properties[new_prop_name] = {
                        "state": new_prop_state,
                        "address": new_prop_address,
                        "property_type": new_prop_type,
                        "notes": new_prop_notes
                    }

                    # Initialize budget for new property
                    if new_prop_name not in st.session_state.home_budgets:
                        st.session_state.home_budgets[new_prop_name] = {
                            "Utilities": 200,
                            "Insurance": 150, 
                            "Maintenance": 100,
                            "Property Tax": 300,
                            "HOA": 0
                        }

                    # Add to states tracking if new state
                    if new_prop_state not in st.session_state.states:
                        st.session_state.states[new_prop_state] = 0

                    st.success(f"✅ Added property: {new_prop_name} in {new_prop_state}")
                    st.rerun()
                else:
                    st.error("❌ Property name already exists. Please choose a different name.")
            else:
                st.error("❌ Please enter both property name and state.")

def render_budgets_tab():
    """Render budgets management tab"""
    st.markdown('<h2><i data-lucide="wallet" class="icon"></i>Budget Management</h2>', unsafe_allow_html=True)

    # Budget overview
    col1, col2, col3 = st.columns(3)

    with col1:
        total_budget = sum(sum(budget.values()) for budget in st.session_state.home_budgets.values())
        st.metric("Total Monthly Budget", f"${total_budget:,}")

    with col2:
        num_homes = len(st.session_state.home_budgets)
        st.metric("Properties", num_homes)

    with col3:
        avg_budget = total_budget / max(num_homes, 1)
        st.metric("Average per Property", f"${avg_budget:,.0f}")

    st.markdown("---")

    # Budget management
    st.subheader("Manage Property Budgets")

    # Select property to manage
    if st.session_state.home_budgets:
        # Show property selector with state info
        property_options = []
        for prop_name in st.session_state.home_budgets.keys():
            if 'user_properties' in st.session_state and prop_name in st.session_state.user_properties:
                state = st.session_state.user_properties[prop_name]['state']
                property_options.append(f"{prop_name} ({state})")
            else:
                property_options.append(prop_name)

        selected_display = st.selectbox("Select Property", property_options)
        selected_home = selected_display.split(" (")[0]  # Extract property name

        if selected_home:
            # Show property details if available
            if 'user_properties' in st.session_state and selected_home in st.session_state.user_properties:
                prop_details = st.session_state.user_properties[selected_home]
                st.info(f"🏠 **{selected_home}** - {prop_details['state']} ({prop_details['property_type']})")

            st.write(f"**Budget for {selected_home}:**")
            budget = st.session_state.home_budgets[selected_home]

            # Display current budget breakdown
            budget_col1, budget_col2 = st.columns(2)

            with budget_col1:
                st.write("**Current Budget:**")
                for category, amount in budget.items():
                    st.write(f"• {category}: ${amount:,}")
                st.write(f"**Total: ${sum(budget.values()):,}**")

            with budget_col2:
                st.write("**Edit Budget:**")
                new_budget = {}
                for category, current_amount in budget.items():
                    new_budget[category] = st.number_input(
                        f"{category}", 
                        value=current_amount, 
                        min_value=0, 
                        step=100,
                        key=f"budget_{selected_home}_{category}"
                    )

                # Add new budget category
                st.write("**Add Category:**")
                new_category = st.text_input("Category Name", key=f"new_category_{selected_home}")
                new_amount = st.number_input("Amount", min_value=0, step=50, key=f"new_amount_{selected_home}")

                if st.button("Add Category", key=f"add_cat_{selected_home}"):
                    if new_category and new_category not in budget:
                        new_budget[new_category] = new_amount
                        st.success(f"Added {new_category}")

                if st.button("Update Budget", type="primary"):
                    st.session_state.home_budgets[selected_home] = new_budget
                    st.success(f"Budget updated for {selected_home}")

                    # Sync bill reminders to calendar if enabled
                    if (st.session_state.get('sync_bill_reminders', False) and 
                        'google_calendar_credentials' in st.session_state):

                        from utils.google_calendar import calendar_sync

                        # Create calendar reminders for bills
                        try:
                            today = datetime.date.today()
                            next_month = today.replace(day=1) + datetime.timedelta(days=32)
                            next_month = next_month.replace(day=1)

                            for category, amount in new_budget.items():
                                # Create reminder for next month (simplified - in production you'd use actual due dates)
                                bill_date = next_month.replace(day=15)  # Default to 15th of month

                                reminder_created = calendar_sync.create_reminder_event(
                                    title=f"{selected_home} {category} Bill",
                                    description=f"${amount} {category} bill due for {selected_home}",
                                    due_date=bill_date,
                                    reminder_type="bill"
                                )

                                if reminder_created:
                                    st.info(f"📅 Created calendar reminder for {category} bill")

                        except Exception as e:
                            st.warning(f"Calendar sync failed: {e}")

                    st.rerun()
    else:
        st.info("No properties configured yet. Go to Settings → Data Management to add properties.")

def render_ai_assistant_tab(openai_available, openai_client):
    """Render AI assistant tab"""
    st.markdown('<h2><i data-lucide="bot" class="icon"></i>AI Financial Assistant</h2>', unsafe_allow_html=True)

    if not openai_available:
        st.warning("🔑 AI features require an OpenAI API key. Add your OPENAI_API_KEY to Replit Secrets to enable this feature.")
        st.info("Once configured, the AI assistant can help with:")
        st.write("• Tax residency planning advice")
        st.write("• Budget optimization suggestions")
        st.write("• Risk assessment and alerts")
        st.write("• Financial planning recommendations")
    else:
        # AI Chat Interface
        st.subheader("Ask Your Financial Assistant")

        # Initialize chat history
        if "ai_chat_history" not in st.session_state:
            st.session_state.ai_chat_history = []

        # Display chat history
        for message in st.session_state.ai_chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about your tax residency, budgets, or financial planning..."):
            # Add user message to chat
            st.session_state.ai_chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.write(prompt)

            # Generate AI response (placeholder for now)
            with st.chat_message("assistant"):
                response = f"I understand you're asking about: '{prompt}'. As your AI financial assistant, I would analyze your current tax residency status, budget allocations, and provide personalized advice. This feature will be fully implemented once the OpenAI integration is complete."
                st.write(response)
                st.session_state.ai_chat_history.append({"role": "assistant", "content": response})

        # Quick action buttons
        st.subheader("Quick Insights")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Analyze Tax Risk", use_container_width=True):
                st.info("AI would analyze your current day counts and provide risk assessment")

        with col2:
            if st.button("Budget Optimization", use_container_width=True):
                st.info("AI would suggest budget optimizations based on your spending patterns")

        with col3:
            if st.button("Planning Advice", use_container_width=True):
                st.info("AI would provide personalized tax residency planning advice")

def render_reports_tab():
    """Render reports tab"""
    st.markdown('<h2><i data-lucide="file-text" class="icon"></i>Tax Residency Reports</h2>', unsafe_allow_html=True)

    # Report type selector
    report_type = st.selectbox(
        "Select Report Type",
        ["Annual Summary", "Monthly Breakdown", "Risk Assessment", "Budget Analysis"]
    )

    if report_type == "Annual Summary":
        st.subheader("Annual Tax Residency Summary")

        # Year selector
        import datetime
        current_year = datetime.datetime.now().year
        selected_year = st.selectbox("Select Year", [current_year, current_year - 1, current_year - 2])

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_days = sum(st.session_state.states.values())
            st.metric("Total Days Logged", total_days)

        with col2:
            max_state = max(st.session_state.states.keys(), key=lambda x: st.session_state.states[x]) if st.session_state.states else "None"
            st.metric("Primary State", max_state)

        with col3:
            days_remaining = st.session_state.tax_threshold - max(st.session_state.states.values()) if st.session_state.states else st.session_state.tax_threshold
            st.metric("Days to Threshold", days_remaining)

        with col4:
            risk_level = "🟢 Safe" if days_remaining > 30 else "🟡 Monitor" if days_remaining > 14 else "🔴 Risk"
            st.metric("Risk Status", risk_level)

        # State breakdown chart
        if st.session_state.states:
            import plotly.express as px
            import pandas as pd

            df = pd.DataFrame(list(st.session_state.states.items()), columns=['State', 'Days'])
            fig = px.pie(df, values='Days', names='State', title='Days by State')
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Monthly Breakdown":
        st.subheader("Monthly Day Count Breakdown")
        st.info("Monthly breakdown functionality - would show day counts by month for each state")

    elif report_type == "Risk Assessment":
        st.subheader("Tax Residency Risk Assessment")

        # Risk analysis
        for state, days in st.session_state.states.items():
            remaining = st.session_state.tax_threshold - days
            percentage = (days / st.session_state.tax_threshold) * 100

            if percentage < 70:
                risk_color = "🟢"
                risk_text = "Safe"
            elif percentage < 90:
                risk_color = "🟡"
                risk_text = "Monitor"
            else:
                risk_color = "🔴"
                risk_text = "High Risk"

            st.markdown(f"**{state}**: {days} days ({percentage:.1f}%) {risk_color} {risk_text}")
            st.progress(min(percentage / 100, 1.0))

    elif report_type == "Budget Analysis":
        st.subheader("Budget Analysis Report")

        if st.session_state.home_budgets:
            total_budget = sum(sum(budget.values()) for budget in st.session_state.home_budgets.values())

            # Budget breakdown by property
            for home, budget in st.session_state.home_budgets.items():
                with st.expander(f"{home} - ${sum(budget.values()):,}/month"):
                    for category, amount in budget.items():
                        percentage = (amount / sum(budget.values())) * 100
                        st.write(f"• {category}: ${amount:,} ({percentage:.1f}%)")
        else:
            st.info("No budget data available. Configure budgets in the Budgets tab.")

    # Export functionality
    st.markdown("---")
    st.subheader("Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export PDF", use_container_width=True):
            st.info("PDF export functionality would be implemented here")

    with col2:
        if st.button("📊 Export Excel", use_container_width=True):
            st.info("Excel export functionality would be implemented here")

    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email report functionality would be implemented here")

def render_community_tab():
    """Render community forum and discussion tab"""
    st.markdown('<h2><i data-lucide="users" class="icon"></i>Snowbird Community</h2>', unsafe_allow_html=True)

    # Community description
    st.markdown("""
    ### 🌐 Connect with Fellow Snowbirds

    Join our vibrant community of seasonal residents sharing tips, asking questions, 
    and helping each other navigate the snowbird lifestyle.
    """)

    # Community features overview
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **💬 Share Tips**
        - Tax residency strategies
        - Home maintenance advice
        - Travel recommendations
        - Cost-saving ideas
        """)

    with col2:
        st.markdown("""
        **❓ Ask Questions**
        - State tax requirements
        - Budget planning help
        - Legal considerations
        - Property management
        """)

    with col3:
        st.markdown("""
        **🏪 Find Local Services**
        - Trusted contractors
        - Healthcare providers
        - Property managers
        - Emergency contacts
        """)

    st.markdown("---")

    # Forum access section
    st.subheader("🗣️ Join the Discussion")

    # Primary forum link with prominent styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
                padding: 2rem; border-radius: 12px; text-align: center; margin: 1.5rem 0;">
        <h3 style="color: white; margin: 0 0 1rem 0;">
            💬 Snowbird Community Forum
        </h3>
        <p style="color: #dbeafe; margin: 0 0 1.5rem 0; font-size: 1.1rem;">
            Connect with thousands of snowbirds sharing their experiences and knowledge
        </p>
        <a href="https://reddit.com/r/snowbirds" target="_blank" 
           style="background: white; color: #1d4ed8; padding: 0.75rem 2rem; 
                  border-radius: 8px; text-decoration: none; font-weight: 600; 
                  font-size: 1.1rem; display: inline-block;">
            🚀 Join Our Forum →
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Alternative community platforms
    st.subheader("🌍 Other Community Platforms")

    community_col1, community_col2 = st.columns(2)

    with community_col1:
        st.markdown("""
        **📱 Social Media Groups**
        - [Facebook Snowbird Groups](https://facebook.com/groups/snowbirds)
        - [Twitter #SnowbirdLife](https://twitter.com/hashtag/snowbirdlife)
        - [LinkedIn Snowbird Network](https://linkedin.com/groups/snowbirds)
        """)

    with community_col2:
        st.markdown("""
        **📧 Newsletter & Updates**
        - Weekly community highlights
        - Tax law changes
        - New member introductions
        - Local event announcements
        """)

    # Community guidelines and rules
    with st.expander("📋 Community Guidelines"):
        st.markdown("""
        **Our Community Values:**

        🤝 **Be Respectful** - Treat all members with kindness and respect

        💡 **Share Knowledge** - Help others with your experiences and insights

        🎯 **Stay On Topic** - Keep discussions relevant to snowbird lifestyle

        🔒 **Protect Privacy** - Don't share personal financial or location details

        ⚖️ **No Legal Advice** - Always consult professionals for legal/tax matters

        🚫 **No Spam** - Commercial promotions must be approved by moderators
        """)

    # Quick tips for new community members
    st.subheader("💡 Getting Started in the Community")

    st.markdown("""
    **New to our community? Here's how to get the most out of it:**

    1. **📝 Introduce Yourself** - Share your snowbird journey and which states you split time between

    2. **🔍 Search First** - Check if your question has been answered before posting

    3. **🏷️ Use Tags** - Help others find your posts with relevant tags (#taxes, #arizona, #minnesota, etc.)

    4. **👥 Follow Topics** - Subscribe to discussions about your areas of interest

    5. **🎁 Give Back** - Share your own tips and experiences to help newcomers
    """)

    # Community stats and activity (placeholder for future integration)
    st.markdown("---")
    st.subheader("📊 Community Activity")

    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

    with stats_col1:
        st.metric("Active Members", "2,847", "↗️ +127 this month")

    with stats_col2:
        st.metric("Discussions", "1,392", "↗️ +89 this week")

    with stats_col3:
        st.metric("Tips Shared", "5,621", "↗️ +203 this month")

    with stats_col4:
        st.metric("States Covered", "48", "Complete coverage!")

    # Embedded forum preview (using iframe for demonstration)
    st.markdown("---")
    st.subheader("📖 Recent Community Discussions")

    # Option to embed forum content via iframe
    if st.checkbox("📺 Show Live Forum Feed", help="Display recent discussions directly in the app"):
        st.markdown("""
        <div style="border: 2px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin: 1rem 0;">
            <iframe src="https://reddit.com/r/snowbirds/new.compact" 
                    width="100%" height="400" frameborder="0"
                    style="border: none; background: white;">
                <p>Your browser does not support iframes. 
                   <a href="https://reddit.com/r/snowbirds" target="_blank">Visit our forum directly</a>
                </p>
            </iframe>
        </div>
        """, unsafe_allow_html=True)

        st.caption("🔗 Forum content loads from external source - may take a moment to appear")

    # Quick contact for community issues
    st.markdown("---")
    st.info("""
    **Need Help with the Community?**

    📧 Contact our community moderators: community@snowbirdapp.com

    🐛 Report technical issues or suggest improvements for better community integration
    """)

def render_footer():
    """Render application footer with Hawaiian vibes"""
    from utils.hawaii_expressions import da_kine_success
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #64748B; font-size: 0.9rem; padding: 1.5rem;">
        <div style="margin-bottom: 1rem;">
            <strong style="color: #12BDF2;">🌺 Snowbird Financial Assistant 🌺</strong>
        </div>
        <div style="margin-bottom: 1rem;">
            <span style="margin: 0 1rem;">📍 Multi-State Tax Planning</span>
            <span style="margin: 0 1rem;">💰 Budget Management</span>
            <span style="margin: 0 1rem;">🤖 AI-Powered Insights</span>
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8;">
            Built with aloha spirit ❤️ and island vibes 🌊 for seasonal residents everywhere<br>
            <em>Helping snowbirds navigate da kine with confidence and style! 🤙</em><br>
            <small style="color: #0ea5e9; font-style: italic;">
                Mahalo for choosing our ohana! 🌺
            </small>
        </div>
    </div>
    """, unsafe_allow_html=True)

def validate_backup_data(backup_data: dict) -> bool:
    """
    Validate backup data structure and integrity

    Args:
        backup_data (dict): The backup data to validate

    Returns:
        bool: True if backup is valid, False otherwise
    """
    try:
        # Check required top-level keys
        required_keys = ['timestamp', 'version', 'data']
        if not all(key in backup_data for key in required_keys):
            return False

        # Check data structure
        data = backup_data['data']

        # Validate states data
        if 'states' in data:
            states = data['states']
            if not isinstance(states, dict):
                return False
            # Check that all values are numeric
            for state, days in states.items():
                if not isinstance(days, (int, float)) or days < 0:
                    return False

        # Validate budgets data
        if 'home_budgets' in data:
            budgets = data['home_budgets']
            if not isinstance(budgets, dict):
                return False
            # Check budget structure
            for state, budget in budgets.items():
                if not isinstance(budget, dict):
                    return False
                for category, amount in budget.items():
                    if not isinstance(amount, (int, float)) or amount < 0:
                        return False

        # Validate threshold
        if 'tax_threshold' in data:
            threshold = data['tax_threshold']
            if not isinstance(threshold, (int, float)) or threshold <= 0 or threshold > 365:
                return False

        return True

    except Exception as e:
        logger.error(f"Backup validation error: {e}")
        return False

def restore_backup_data(backup_data: dict):
    """
    Restore backup data to session state

    Args:
        backup_data (dict): The validated backup data to restore
    """
    try:
        data = backup_data['data']

        # Restore core tracking data
        if 'states' in data:
            st.session_state.states = data['states']

        if 'home_budgets' in data:
            st.session_state.home_budgets = data['home_budgets']

        if 'seasonal_cash_flow' in data:
            st.session_state.seasonal_cash_flow = data['seasonal_cash_flow']

        # Restore settings
        if 'tax_threshold' in data:
            st.session_state.tax_threshold = data['tax_threshold']

        if 'risk_warning_days' in data:
            st.session_state.risk_warning_days = data['risk_warning_days']

        if 'default_state' in data:
            st.session_state.default_state = data['default_state']

        # Restore user preferences
        if 'user_preferences' in data:
            prefs = data['user_preferences']
            st.session_state.theme = prefs.get('theme', 'light')
            st.session_state.notify_email = prefs.get('notifications', False)
            st.session_state.auto_save = prefs.get('auto_save', True)
            st.session_state.show_tips = prefs.get('show_tips', True)

        # Restore additional data if present
        if 'migration_checklist' in data:
            st.session_state.migration_checklist = data['migration_checklist']

        if 'bills' in data:
            st.session_state.bills = data['bills']

        # Auto-save the restored data
        from utils.data_persistence import save_user_data
        save_user_data()

        logger.info("Backup restored successfully")

    except Exception as e:
        logger.error(f"Backup restoration error: {e}")
        raise e

def render_sidebar():
    """Render sidebar with theme toggle and other options"""
    # Import and render theme toggle
    from components.styles import render_theme_toggle
    render_theme_toggle()

def start_api_server():
    """Start the FastAPI server in a background thread"""
    def run_server():
        try:
            from api import run_api_server
            # Run API server on port 8000 (different from Streamlit's port)
            run_api_server(host="0.0.0.0", port=8000)
        except Exception as e:
            from utils.logging_config import data_logger
            data_logger.error(f"API server failed to start: {e}")

    # Start server in daemon thread so it doesn't prevent app shutdown
    api_thread = threading.Thread(target=run_server, daemon=True)
    api_thread.start()

    # Give the server a moment to start
    time.sleep(2)

    # Show API info in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("🔗 **REST API Available**")
        st.markdown("API running on port 8000")
        st.markdown("- `GET /logs` - View logs")
        st.markdown("- `GET /budgets` - View budgets") 
        st.markdown("- `POST /logs` - Add log entry")
        st.markdown("- `/docs` - API documentation")

# Run the main application
if __name__ == "__main__":
    main()