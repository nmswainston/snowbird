"""
Snowbird Financial Assistant - Main Application
"""
import streamlit as st
from components.styles import load_custom_css
from utils.accessibility import AccessibilityManager
from utils.performance import PerformanceOptimizer, monitor_memory_usage
from components.feedback_system import render_feedback_form, render_help_section
from utils.i18n import render_language_selector, t
from utils.version_manager import render_version_info
from utils.error_handling import initialize_error_monitoring, render_error_banner

# Configure Streamlit page first
st.set_page_config(
    page_title="Snowbird Financial Assistant",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def safe_main():
    """Safely run the main application with error handling"""
    try:
        # Try to import and run main app
        from main_app import main
        main()
    except ImportError as e:
        st.error("❌ **Import Error**")
        st.write(f"Could not import required modules: {e}")
        st.info("💡 **Solutions:**")
        st.write("1. Restart the application")
        st.write("2. Check that all dependencies are installed")
        st.write("3. Verify the file structure is correct")

        if st.button("🔄 Restart Application"):
            st.rerun()

    except Exception as e:
        st.error("🚨 **Application Error**")
        st.write("The Snowbird app encountered an unexpected error.")

        with st.expander("🔍 Error Details"):
            st.code(f"Error Type: {type(e).__name__}")
            st.code(f"Error Message: {str(e)}")
            st.code(f"Traceback:\n{traceback.format_exc()}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart"):
                st.rerun()
        with col2:
            if st.button("🏠 Reset Session"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    safe_main()