"""
Error monitoring and health dashboard for the Snowbird application.
"""

import streamlit as st
import datetime
import json
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

from utils.logging_config import logger
from utils.error_handling import get_error_context
from config import config

def render_error_monitoring_tab():
    """Render the error monitoring and application health tab"""

    if not config.debug and not config.is_development():
        st.warning("Error monitoring is only available in development mode.")
        return

    st.markdown('<h2><i data-lucide="activity" class="icon"></i>Application Health & Error Monitoring</h2>', unsafe_allow_html=True)

    # Application Health Status
    render_health_status()

    # Error Logs
    render_error_logs()

    # Performance Metrics
    render_performance_metrics()

    # Configuration Status
    render_configuration_status()

def render_health_status():
    """Render application health status"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="heart" class="icon"></i>Application Health**', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Check if logging is working
        try:
            logger.info("Health check - logging test")
            logging_status = "🟢 Healthy"
        except Exception:
            logging_status = "🔴 Failed"
        st.metric("Logging", logging_status)

    with col2:
        # Check configuration
        try:
            from utils.config_manager import validate_required_config
            validation = validate_required_config()
            config_status = "🟢 Valid" if all(validation.values()) else "🟡 Issues"
        except Exception:
            config_status = "🔴 Failed"
        st.metric("Configuration", config_status)

    with col3:
        # Check session state
        session_items = len(st.session_state.keys()) if hasattr(st, 'session_state') else 0
        session_status = "🟢 Active" if session_items > 0 else "🟡 Empty"
        st.metric("Session State", session_status, delta=f"{session_items} items")

    with col4:
        # Check external services
        external_status = check_external_services()
        st.metric("External Services", external_status)

    st.markdown('</div>', unsafe_allow_html=True)

def check_external_services() -> str:
    """Check status of external services"""
    services_ok = 0
    total_services = 0

    # Check OpenAI
    if config.enable_ai_features and config.openai_api_key:
        total_services += 1
        try:
            from openai import OpenAI
            client = OpenAI(api_key=config.openai_api_key)
            # Quick test call would go here
            services_ok += 1
        except Exception:
            pass

    # Check email configuration
    if config.enable_notifications:
        total_services += 1
        if config.smtp_username and config.smtp_password:
            services_ok += 1

    if total_services == 0:
        return "🟡 None"
    elif services_ok == total_services:
        return "🟢 All OK"
    elif services_ok > 0:
        return f"🟡 {services_ok}/{total_services}"
    else:
        return "🔴 Failed"

def render_error_logs():
    """Render recent error logs"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="alert-triangle" class="icon"></i>Recent Errors**', unsafe_allow_html=True)

    log_file = Path("logs") / f"snowbird_errors_{datetime.date.today().isoformat()}.log"

    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()

            if lines:
                # Show last 10 error entries
                recent_errors = lines[-10:]

                for line in reversed(recent_errors):
                    if line.strip():
                        # Parse log line
                        try:
                            parts = line.split(' | ', 4)
                            if len(parts) >= 4:
                                timestamp = parts[0]
                                level = parts[1].strip()
                                location = parts[2]
                                message = parts[3] if len(parts) > 3 else "No message"

                                # Color code by level
                                if "ERROR" in level:
                                    st.error(f"🔴 {timestamp} - {message}")
                                elif "WARNING" in level:
                                    st.warning(f"🟡 {timestamp} - {message}")
                                else:
                                    st.info(f"ℹ️ {timestamp} - {message}")

                                with st.expander(f"Details: {location}"):
                                    st.code(line)
                        except Exception:
                            st.text(line.strip())
            else:
                st.success("🎉 No errors found today!")

        except Exception as e:
            st.error(f"Could not read error log: {e}")
    else:
        st.info("No error log file found for today.")

    # Clear logs button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Error Logs", help="Clear today's error logs"):
            try:
                if log_file.exists():
                    log_file.unlink()
                st.success("Error logs cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear logs: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

def render_performance_metrics():
    """Render performance metrics if available"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="zap" class="icon"></i>Performance Metrics**', unsafe_allow_html=True)

    # Read performance data from logs
    log_file = Path("logs") / f"snowbird_{datetime.date.today().isoformat()}.log"

    performance_data = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "Performance:" in line:
                        # Parse performance log entries
                        try:
                            # Extract operation and duration
                            if "took" in line and "s" in line:
                                parts = line.split("Performance:")
                                if len(parts) > 1:
                                    perf_info = parts[1].strip()
                                    # Extract operation name and duration
                                    import re
                                    match = re.search(r'(\w+) took ([\d.]+)s', perf_info)
                                    if match:
                                        operation = match.group(1)
                                        duration = float(match.group(2))
                                        timestamp = line.split(' | ')[0]
                                        performance_data.append({
                                            'timestamp': timestamp,
                                            'operation': operation,
                                            'duration': duration
                                        })
                        except Exception:
                            continue
        except Exception as e:
            st.error(f"Could not read performance data: {e}")

    if performance_data:
        # Create DataFrame and show metrics
        df = pd.DataFrame(performance_data)

        col1, col2, col3 = st.columns(3)

        with col1:
            avg_duration = df['duration'].mean()
            st.metric("Average Duration", f"{avg_duration:.3f}s")

        with col2:
            slow_operations = len(df[df['duration'] > 2.0])
            st.metric("Slow Operations", slow_operations, help="Operations taking >2 seconds")

        with col3:
            total_operations = len(df)
            st.metric("Total Operations", total_operations)

        # Show performance chart
        if len(df) > 1:
            st.subheader("Performance Over Time")
            chart_data = df.set_index('timestamp')['duration']
            st.line_chart(chart_data)

        # Show slowest operations
        if len(df) > 0:
            st.subheader("Recent Operations")
            display_df = df[['operation', 'duration']].tail(10)
            display_df['duration'] = display_df['duration'].apply(lambda x: f"{x:.3f}s")
            st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No performance data available for today.")

    st.markdown('</div>', unsafe_allow_html=True)

def render_configuration_status():
    """Render configuration validation status"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="settings" class="icon"></i>Configuration Status**', unsafe_allow_html=True)

    try:
        from utils.config_manager import validate_required_config, get_config_summary

        # Get validation results
        validation = validate_required_config()
        config_summary = get_config_summary()

        # Display validation results
        st.subheader("Validation Results")
        for component, is_valid in validation.items():
            status = "✅ Valid" if is_valid else "❌ Invalid"
            color = "green" if is_valid else "red"
            st.markdown(f'<span style="color: {color}">**{component}**: {status}</span>', unsafe_allow_html=True)

        # Display configuration summary
        st.subheader("Configuration Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Application Settings:**")
            st.write(f"• Environment: {config_summary['environment']}")
            st.write(f"• Debug Mode: {config_summary['debug']}")
            st.write(f"• Tax Threshold: {config_summary['tax_threshold']} days")
            st.write(f"• Server: {config_summary['server_host']}:{config_summary['server_port']}")

        with col2:
            st.write("**Feature Status:**")
            features = config_summary['features_enabled']
            for feature, enabled in features.items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                st.write(f"• {feature.replace('_', ' ').title()}: {status}")

        # API Keys status
        st.subheader("API Keys & Credentials")
        st.write(f"• OpenAI API Key: {'✅ Configured' if config_summary['has_openai_key'] else '❌ Missing'}")
        st.write(f"• Email Config: {'✅ Configured' if config_summary['has_email_config'] else '❌ Missing'}")
        st.write(f"• Gmail Config: {'✅ Configured' if config_summary['has_gmail_config'] else '❌ Missing'}")

    except Exception as e:
        st.error(f"Could not load configuration status: {e}")
        logger.error(f"Configuration status error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

def render_system_info():
    """Render system information"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="info" class="icon"></i>System Information**', unsafe_allow_html=True)

    import sys
    import platform
    import os

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Python Environment:**")
        st.write(f"• Python Version: {sys.version.split()[0]}")
        st.write(f"• Platform: {platform.platform()}")
        st.write(f"• Architecture: {platform.architecture()[0]}")

    with col2:
        st.write("**Application Info:**")
        st.write(f"• App Version: {config.app_version}")
        st.write(f"• Streamlit Version: {st.__version__}")
        st.write(f"• Process ID: {os.getpid()}")

    # Memory usage (if psutil is available)
    try:
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()

        st.write("**Resource Usage:**")
        st.write(f"• Memory: {memory_mb:.1f} MB")
        st.write(f"• CPU: {cpu_percent:.1f}%")
    except ImportError:
        st.write("**Resource Usage:** psutil not available")

    st.markdown('</div>', unsafe_allow_html=True)

def export_error_report():
    """Export comprehensive error report"""
    try:
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'config_summary': get_config_summary(),
            'error_context': get_error_context(),
            'recent_errors': [],
            'performance_data': []
        }

        # Add recent errors
        log_file = Path("logs") / f"snowbird_errors_{datetime.date.today().isoformat()}.log"
        if log_file.exists():
            with open(log_file, 'r') as f:
                report_data['recent_errors'] = f.readlines()[-50:]  # Last 50 errors

        # Convert to JSON
        report_json = json.dumps(report_data, indent=2, default=str)

        return report_json

    except Exception as e:
        logger.error(f"Failed to generate error report: {e}")
        return None

st.markdown('</div>', unsafe_allow_html=True)

def check_external_services():
    """Check the status of external services"""
    try:
        # Check if OpenAI key is available
        from utils.config import settings
        if settings.OPENAI_API_KEY:
            return "🟢 Available"
        else:
            return "🟡 No API Key"
    except Exception:
        return "🔴 Error"

def get_config_summary():
    """Get configuration summary for monitoring"""
    from config import config
    return {
        'environment': config.environment,
        'debug': config.debug,
        'tax_threshold': config.tax_threshold,
        'server_host': config.server_host,
        'server_port': config.server_port,
        'enable_gmail_integration': config.enable_gmail_integration,
        'enable_ai_features': config.enable_ai_features,
        'enable_notifications': config.enable_notifications,
        'openai_api_key_set': bool(config.openai_api_key)
    }