"""
Snowbird Financial Assistant - Main Application (Simplified)
"""
import streamlit as st
import sys
import os

# Add the current directory to the Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Streamlit for deployment
st.set_page_config(
    page_title="Snowbird: Your Seasonal Financial Assistant", 
    layout="wide",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function with fallback implementation"""

    # Try to load the main app, fallback to snowbird_app.py if issues
    try:
        from main_app import main as main_app_main
        main_app_main()
    except Exception as e:
        st.warning(f"Loading main app failed ({str(e)}), using fallback...")

        # Import and run the working snowbird_app.py
        try:
            # Import the snowbird app content
            exec(open('snowbird_app.py').read())
        except Exception as fallback_error:
            st.error(f"Fallback also failed: {str(fallback_error)}")

            # Ultimate fallback - basic app
            st.title("❄️ Snowbird Financial Assistant 🏖️")
            st.write("Application is starting up...")
            st.info("If you continue to see this message, please refresh the page.")

if __name__ == "__main__":
    main()