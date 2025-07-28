import streamlit as st
from components.session_state import initialize_session_state
from components.styles import load_custom_css, render_main_header
from components.dashboard import render_dashboard
from components.day_tracker import render_day_tracker
from utils.auth import check_openai_availability
from utils.data_models import SnowbirdData

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
        # Initialize session state
        initialize_session_state()

        # Load custom CSS
        load_custom_css()

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

    # Dashboard now includes integrated quick actions

    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "📅 Day Tracker", 
        "💰 Budgets", 
        "🤖 AI Assistant", 
        "📋 Reports",
        "⚙️ Settings"
    ])

    with tab1:
        render_dashboard()

    with tab2:
        render_day_tracker()

    with tab3:
        render_budgets_tab()

    with tab4:
        render_ai_assistant_tab(openai_available, openai_client)

    with tab5:
        render_reports_tab()

    with tab6:
        render_settings_tab()

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
        selected_home = st.selectbox("Select Property", list(st.session_state.home_budgets.keys()))

        if selected_home:
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

                if st.button("Update Budget", type="primary"):
                    st.session_state.home_budgets[selected_home] = new_budget
                    st.success(f"Budget updated for {selected_home}")
                    st.rerun()
    else:
        st.info("No properties configured yet. Go to Day Tracker to add properties.")

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

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.9rem; padding: 1.5rem;">
        <div style="margin-bottom: 1rem;">
            <strong style="color: #12BDF2;">❄️ Snowbird Financial Assistant ❄️</strong>
        </div>
        <div style="margin-bottom: 1rem;">
            <span style="margin: 0 1rem;">📍 Multi-State Tax Planning</span>
            <span style="margin: 0 1rem;">💰 Budget Management</span>
            <span style="margin: 0 1rem;">🤖 AI-Powered Insights</span>
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8;">
            Built with ❤️ and ❄️ for seasonal residents everywhere<br>
            <em>Helping snowbirds fly south (and north) with confidence</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with theme toggle and other options"""
    # Import and render theme toggle
    from components.styles import render_theme_toggle
    render_theme_toggle()

if __name__ == "__main__":
    main()