"""
Admin Dashboard for monitoring the Snowbird application.
Provides system health, analytics, and user activity monitoring.
"""

import streamlit as st
import datetime
import json
import psutil
import os
from pathlib import Path
from typing import Dict, Any, List

from components.analytics import get_analytics_summary
from utils.logging_config import logger
from config import config

def render_admin_dashboard():
    """Render the admin monitoring dashboard"""

    # Admin authentication check
    if not check_admin_access():
        render_admin_login()
        return

    st.markdown('<h1><i data-lucide="shield" class="icon"></i>Admin Dashboard</h1>', unsafe_allow_html=True)

    # Create admin tabs
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "📊 Analytics", 
        "⚡ System Health", 
        "👥 User Activity",
        "⚙️ Configuration"
    ])

    with admin_tab1:
        render_analytics_overview()

    with admin_tab2:
        render_system_health()

    with admin_tab3:
        render_user_activity()

    with admin_tab4:
        render_configuration_status()

def check_admin_access() -> bool:
    """Check if user has admin access"""
    # Simple password-based admin access
    if 'admin_authenticated' in st.session_state:
        return st.session_state.admin_authenticated

    # Check for admin password in environment
    admin_password = os.getenv('ADMIN_PASSWORD', 'snowbird_admin_2024')
    return False

def render_admin_login():
    """Render admin login form"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="lock" class="icon"></i>Admin Access Required**', unsafe_allow_html=True)

    password = st.text_input("Enter admin password:", type="password")

    if st.button("Login"):
        admin_password = os.getenv('ADMIN_PASSWORD', 'snowbird_admin_2024')
        if password == admin_password:
            st.session_state.admin_authenticated = True
            st.success("Admin access granted!")
            st.rerun()
        else:
            st.error("Invalid password!")

    st.info("💡 Set ADMIN_PASSWORD in your environment variables to change the default password.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics_overview():
    """Render analytics overview"""
    st.markdown('<h2><i data-lucide="bar-chart" class="icon"></i>Analytics Overview</h2>', unsafe_allow_html=True)

    # Get analytics summary
    try:
        analytics_summary = get_analytics_summary()

        if 'error' in analytics_summary:
            st.error(f"Analytics Error: {analytics_summary['error']}")
            return

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Events", analytics_summary.get('total_events', 0))

        with col2:
            st.metric("Unique Sessions", analytics_summary.get('unique_sessions', 0))

        with col3:
            avg_events = analytics_summary.get('total_events', 0) / max(analytics_summary.get('unique_sessions', 1), 1)
            st.metric("Avg Events/Session", f"{avg_events:.1f}")

        with col4:
            days_with_activity = len(analytics_summary.get('daily_activity', {}))
            st.metric("Active Days", days_with_activity)

        # Event types breakdown
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Event Types**', unsafe_allow_html=True)

        event_types = analytics_summary.get('event_types', {})
        if event_types:
            import pandas as pd
            df = pd.DataFrame(list(event_types.items()), columns=['Event Type', 'Count'])
            st.bar_chart(df.set_index('Event Type'))
        else:
            st.info("No event data available")

        st.markdown('</div>', unsafe_allow_html=True)

        # Daily activity
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Daily Activity (Last 7 Days)**', unsafe_allow_html=True)

        daily_activity = analytics_summary.get('daily_activity', {})
        if daily_activity:
            import pandas as pd
            df = pd.DataFrame(list(daily_activity.items()), columns=['Date', 'Events'])
            df['Date'] = pd.to_datetime(df['Date'])
            st.line_chart(df.set_index('Date'))
        else:
            st.info("No daily activity data available")

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to load analytics: {e}")

def render_system_health():
    """Render system health monitoring"""
    st.markdown('<h2><i data-lucide="activity" class="icon"></i>System Health</h2>', unsafe_allow_html=True)

    # System metrics
    try:
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("CPU Usage", f"{cpu_percent:.1f}%")
            if cpu_percent > 80:
                st.error("⚠️ High CPU usage!")

        with col2:
            memory_percent = memory.percent
            st.metric("Memory Usage", f"{memory_percent:.1f}%")
            if memory_percent > 80:
                st.error("⚠️ High memory usage!")

        with col3:
            disk_percent = (disk.used / disk.total) * 100
            st.metric("Disk Usage", f"{disk_percent:.1f}%")
            if disk_percent > 80:
                st.warning("⚠️ High disk usage!")

        # Process information
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Process Information**', unsafe_allow_html=True)

        process = psutil.Process()
        st.write(f"**Process ID**: {process.pid}")
        st.write(f"**Memory**: {process.memory_info().rss / 1024 / 1024:.1f} MB")
        st.write(f"**CPU Time**: {process.cpu_times().user + process.cpu_times().system:.2f}s")
        st.write(f"**Open Files**: {len(process.open_files())}")
        st.write(f"**Threads**: {process.num_threads()}")

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Application health checks
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Application Health**', unsafe_allow_html=True)

        health_checks = run_health_checks()

        for check_name, result in health_checks.items():
            if result['status'] == 'healthy':
                st.success(f"✅ {check_name}: {result['message']}")
            elif result['status'] == 'warning':
                st.warning(f"⚠️ {check_name}: {result['message']}")
            else:
                st.error(f"❌ {check_name}: {result['message']}")

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to get system metrics: {e}")

def render_user_activity():
    """Render user activity monitoring"""
    st.markdown('<h2><i data-lucide="users" class="icon"></i>User Activity</h2>', unsafe_allow_html=True)

    # Session information
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**Current Session**', unsafe_allow_html=True)

    session_info = {
        'Session Items': len(st.session_state.keys()),
        'Session ID': st.session_state.get('analytics_session_id', 'Not set'),
        'Admin Authenticated': st.session_state.get('admin_authenticated', False)
    }

    for key, value in session_info.items():
        st.write(f"**{key}**: {value}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent log entries
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**Recent Log Entries**', unsafe_allow_html=True)

    try:
        log_file = Path("logs/snowbird_app.log")
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-20:] if len(lines) > 20 else lines
                
            for line in reversed(recent_lines):
                if line.strip():
                    st.text(line.strip())
        else:
            st.info("No log file found")
    except Exception as e:
        st.error(f"Failed to read logs: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

def render_configuration_status():
    """Render configuration status"""
    st.markdown('<h2><i data-lucide="settings" class="icon"></i>Configuration Status</h2>', unsafe_allow_html=True)

    # Configuration summary
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**Configuration Summary**', unsafe_allow_html=True)

    config_summary = get_config_summary()

    for key, value in config_summary.items():
        if isinstance(value, bool):
            icon = "✅" if value else "❌"
            st.write(f"{icon} **{key.replace('_', ' ').title()}**: {value}")
        else:
            st.write(f"**{key.replace('_', ' ').title()}**: {value}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Configuration validation
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**Configuration Validation**', unsafe_allow_html=True)
    
    validation_results = validate_required_config()
    
    for component, is_valid in validation_results.items():
        if is_valid:
            st.success(f"✅ {component.replace('_', ' ').title()}: Valid")
        else:
            st.error(f"❌ {component.replace('_', ' ').title()}: Invalid")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Environment variables
    if st.checkbox("Show Environment Variables (Sensitive)"):
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Environment Variables**', unsafe_allow_html=True)
        
        sensitive_vars = ['OPENAI_API_KEY', 'ADMIN_PASSWORD', 'SMTP_PASSWORD']
        
        for key, value in os.environ.items():
            if key.startswith(('SNOWBIRD_', 'OPENAI_', 'GMAIL_', 'SMTP_', 'ADMIN_')):
                if key in sensitive_vars and value:
                    display_value = f"{'*' * (len(value) - 4)}{value[-4:]}" if len(value) > 4 else "***"
                else:
                    display_value = value or "(not set)"
                st.write(f"**{key}**: {display_value}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def run_health_checks() -> Dict[str, Dict[str, str]]:
    """Run application health checks"""
    checks = {}

    # Check logging
    try:
        logger.info("Health check - logging test")
        checks['Logging'] = {'status': 'healthy', 'message': 'Logging system operational'}
    except Exception as e:
        checks['Logging'] = {'status': 'error', 'message': f'Logging failed: {e}'}

    # Check configuration
    try:
        validation = validate_required_config()
        if all(validation.values()):
            checks['Configuration'] = {'status': 'healthy', 'message': 'All configurations valid'}
        else:
            invalid_configs = [k for k, v in validation.items() if not v]
            checks['Configuration'] = {'status': 'warning', 'message': f'Invalid configs: {", ".join(invalid_configs)}'}
    except Exception as e:
        checks['Configuration'] = {'status': 'error', 'message': f'Config check failed: {e}'}

    # Check disk space
    try:
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent < 80:
            checks['Disk Space'] = {'status': 'healthy', 'message': f'{disk_percent:.1f}% used'}
        elif disk_percent < 90:
            checks['Disk Space'] = {'status': 'warning', 'message': f'{disk_percent:.1f}% used'}
        else:
            checks['Disk Space'] = {'status': 'error', 'message': f'{disk_percent:.1f}% used - Critical!'}
    except Exception as e:
        checks['Disk Space'] = {'status': 'error', 'message': f'Disk check failed: {e}'}

    # Check analytics
    try:
        analytics_summary = get_analytics_summary()
        if 'error' not in analytics_summary:
            checks['Analytics'] = {'status': 'healthy', 'message': 'Analytics system operational'}
        else:
            checks['Analytics'] = {'status': 'warning', 'message': 'Analytics data unavailable'}
    except Exception as e:
        checks['Analytics'] = {'status': 'error', 'message': f'Analytics check failed: {e}'}

    return checks