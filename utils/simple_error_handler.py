
"""
Simple error handler for startup issues
"""
import streamlit as st
import traceback
import logging

def safe_import(module_name, package=None):
    """Safely import a module with error handling"""
    try:
        if package:
            return __import__(module_name, fromlist=[package])
        else:
            return __import__(module_name)
    except ImportError as e:
        st.error(f"❌ Could not import {module_name}: {e}")
        st.info("💡 Try restarting the application or check if all dependencies are installed.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error importing {module_name}: {e}")
        st.code(traceback.format_exc())
        return None

def handle_startup_error(error):
    """Handle startup errors gracefully"""
    st.error("🚨 Application Startup Error")
    st.write("The Snowbird app encountered an error during startup.")
    
    with st.expander("Error Details"):
        st.code(str(error))
        st.code(traceback.format_exc())
    
    st.info("💡 **Troubleshooting Steps:**")
    st.write("1. Restart the application")
    st.write("2. Check that all environment variables are set")
    st.write("3. Verify all dependencies are installed")
    
    # Simple restart button
    if st.button("🔄 Try Restart"):
        st.rerun()
