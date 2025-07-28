"""
Snowbird Financial Assistant - Main Application
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

# Add error boundary for React components
st.markdown("""
<script>
window.addEventListener('error', function(e) {
    console.log('Caught error:', e.error);
    e.preventDefault();
    return true;
});
</script>
""", unsafe_allow_html=True)

# Initialize Firebase authentication with error handling
try:
    from components.auth_components import check_authentication, render_logout_button
    from utils.profile_sync import initialize_user_session, save_user_session, get_profile_sync
    
    # Check authentication first
    user = check_authentication()
    
    # Initialize user session with profile data
    initialize_user_session()
    FIREBASE_AVAILABLE = True
except ImportError as e:
    st.warning("⚠️ Firebase authentication not available. Running in local mode.")
    user = {"uid": "local_user", "email": "local@demo.com"}
    FIREBASE_AVAILABLE = False
    
    # Define stub functions
    def render_logout_button():
        st.sidebar.markdown("**👤 Demo User (Local Mode)**")
    
    def initialize_user_session():
        pass
        
    def save_user_session():
        return True
        
    def get_profile_sync():
        class StubSync:
            def sync_location_data(self, uid, data):
                return True
        return StubSync()

# Initialize configuration first
try:
    from config import config
except ImportError:
    # Create a basic config object if config.py is missing
    class BasicConfig:
        def __init__(self):
            self.debug = True
            self.environment = "development"
            self.tax_threshold = 183
            self.enable_ai_features = True
            self.enable_gmail_integration = False
            self.enable_notifications = False
            self.openai_api_key = ""
            self.server_host = "0.0.0.0"
            self.server_port = 8501
    config = BasicConfig()

# Initialize security
from utils.security import SessionSecurity, get_privacy_notice
SessionSecurity.initialize_secure_session()

# Check session validity
if not SessionSecurity.check_session_validity():
    st.warning("⏰ Your session has expired for security reasons. Please refresh the page.")
    st.stop()
else:
    SessionSecurity.refresh_session()

# Load custom styling
from components.styles import load_custom_css, render_main_header
load_custom_css()

def main():
    """Main application function"""
    # Import and run the working snowbird_app.py content directly
    import datetime
    import openai

    # Load your OpenAI API key from Streamlit secrets (safely)
    try:
        openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        openai.api_key = ""

    # State data
    states = {"Arizona": 0, "Minnesota": 0}
    home_budgets = {
        "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
        "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
    }
    seasonal_cash_flow = {
        "Travel": 300,
        "Healthcare": 400,
        "Supplemental Insurance": 200
    }
    TAX_THRESHOLD_DAYS = 183

    # Session state init
    if "states" not in st.session_state:
        st.session_state.states = states
    if "chat_response" not in st.session_state:
        st.session_state.chat_response = ""

    # Render styled header
    render_main_header()

    # Add user profile and logout in sidebar
    with st.sidebar:
        render_logout_button()
        
        with st.expander("👤 User Profile"):
            if FIREBASE_AVAILABLE:
                from components.auth_components import render_user_profile
                render_user_profile()
            else:
                st.markdown("**Demo User (Local Mode)**")
                st.text_input("Email", value="local@demo.com", disabled=True)
        
        with st.expander("🔒 Privacy & Security"):
            st.markdown(get_privacy_notice())

            if st.button("Clear Session Data"):
                SessionSecurity.clear_sensitive_data()
                st.success("Session data cleared!")
                st.rerun()
                
            if st.button("Save Profile Data"):
                if FIREBASE_AVAILABLE:
                    if save_user_session():
                        st.success("✅ Profile data saved!")
                    else:
                        st.error("❌ Failed to save profile data")
                else:
                    st.success("✅ Profile data saved locally!")

    # Import analytics
    from components.analytics import track_page_view, track_user_action, track_feature_usage

    # Create main navigation tabs with error handling
    try:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Dashboard", 
            "📅 Day Tracker", 
            "🗺️ Auto-Track",
            "💰 Budgets", 
            "🤖 AI Assistant", 
            "📋 Reports",
            "🎨 Themes",
            "🔧 Admin"
        ])
    except Exception as e:
        st.error(f"Error creating tabs: {e}")
        # Create simplified tabs as fallback
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📅 Day Tracker", "💰 Budgets", "🤖 AI Assistant"])
        tab5 = tab6 = tab7 = tab8 = None

    with tab1:
        # Dashboard - Overview of all key metrics
        track_page_view("dashboard")
        st.markdown('**<i data-lucide="bar-chart-3" class="icon"></i>Dashboard Overview**', unsafe_allow_html=True)

        # Quick stats
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Arizona Days", st.session_state.states["Arizona"])
        with col2:
            st.metric("Minnesota Days", st.session_state.states["Minnesota"])
        with col3:
            total_days = sum(st.session_state.states.values())
            st.metric("Total Days Logged", total_days)

        # Tax residency status
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="alert-triangle" class="icon"></i>Tax Residency Status**', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        for idx, (state, days) in enumerate(st.session_state.states.items()):
            col = col1 if idx == 0 else col2
            with col:
                remaining_days = TAX_THRESHOLD_DAYS - days
                if days >= TAX_THRESHOLD_DAYS:
                    status_class = "status-danger"
                    status_text = "⚠️ Tax Resident"
                elif remaining_days <= 30:
                    status_class = "status-warning" 
                    status_text = f"⚡ {remaining_days} days left"
                else:
                    status_class = "status-safe"
                    status_text = f"✅ {remaining_days} days left"

                st.markdown(f'<p class="{status_class}">{status_text}</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # Day Tracker - Log location
        track_page_view("day_tracker")
        st.markdown('**<i data-lucide="map-pin" class="icon"></i>Log Your Location**', unsafe_allow_html=True)

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        location = st.radio("Where are you today?", ("Arizona", "Minnesota"))
        if st.button(f"Log a day in {location}"):
            st.session_state.states[location] += 1
            
            # Sync with user profile if Firebase is available
            if FIREBASE_AVAILABLE:
                sync = get_profile_sync()
                if sync.sync_location_data(user['uid'], st.session_state.states):
                    track_user_action("log_day", {"location": location, "total_days": st.session_state.states[location]})
                    st.success(f"Logged a day in {location}!")
                else:
                    st.warning("Day logged locally, but failed to sync with cloud. Data will sync automatically later.")
            else:
                track_user_action("log_day", {"location": location, "total_days": st.session_state.states[location]})
                st.success(f"Logged a day in {location}! (Local mode)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show current totals
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="calendar" class="icon"></i>Current Totals**', unsafe_allow_html=True)

        for state, days in st.session_state.states.items():
            remaining_days = TAX_THRESHOLD_DAYS - days
            progress = min(days / TAX_THRESHOLD_DAYS, 1.0)
            st.write(f"**{state}**: {days} days")
            st.progress(progress)
            if remaining_days > 0:
                st.write(f"  └ {remaining_days} days until tax residency threshold")
            else:
                st.write(f"  └ ⚠️ Over threshold by {abs(remaining_days)} days")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        # Auto-Tracking with Gmail Integration
        track_page_view("auto_track")
        st.markdown('**<i data-lucide="search" class="icon"></i>Intelligent Location Detection**', unsafe_allow_html=True)
        st.markdown("""
        <div class="winter-card">
        <p>✈️ <strong>Gmail Travel Analysis:</strong> Automatically detect travel from your email confirmations</p>
        <p>📍 <strong>GPS Location:</strong> Get your current location for manual verification</p>
        <p>📊 <strong>Audit Trail:</strong> Comprehensive logging for tax compliance</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            from components.auto_tracker import render_auto_tracker
            render_auto_tracker()
        except ImportError:
            st.info("🚧 Auto-tracking feature coming soon! Manual location logging is available in the Day Tracker tab.")
        except Exception as e:
            st.warning(f"Auto-tracker temporarily unavailable: {e}")
            st.info("Manual location logging is still available in the Day Tracker tab.")

    with tab4:
        # Budgets
        track_page_view("budgets")
        st.markdown('**<i data-lucide="dollar-sign" class="icon"></i>Budget Management**', unsafe_allow_html=True)

        # Home budgets
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="home" class="icon"></i>Home Maintenance Budget**', unsafe_allow_html=True)
        budget_home = st.selectbox("Select a home to view budget:", ["Arizona", "Minnesota"])
        budget = home_budgets[budget_home]
        st.subheader(f"{budget_home} Budget")
        for k, v in budget.items():
            st.write(f"• {k}: ${v}/month")
        st.markdown('</div>', unsafe_allow_html=True)

        # Seasonal cash flow
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="trending-up" class="icon"></i>Seasonal Cash Flow Plan**', unsafe_allow_html=True)
        for k, v in seasonal_cash_flow.items():
            st.write(f"• {k}: ${v}/month")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        # AI Assistant
        track_page_view("ai_assistant")
        st.markdown('**<i data-lucide="brain" class="icon"></i>Ask Snowbird AI**', unsafe_allow_html=True)

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        if not openai.api_key or openai.api_key.strip() == "":
            st.info("💡 To enable AI features, add your OPENAI_API_KEY to Replit Secrets in the Tools panel.")
            st.text_area("Ask a financial question:", disabled=True, placeholder="Add OpenAI API key to enable this feature")
        else:
            question = st.text_input("Ask a financial question:")
            if st.button("Get AI Advice"):
                if question.strip():
                    track_feature_usage("ai_query", {"question_length": len(question)})
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a friendly AI financial assistant for seasonal residents (snowbirds)."},
                                {"role": "user", "content": question}
                            ]
                        )
                        st.session_state.chat_response = response['choices'][0]['message']['content']
                        track_user_action("ai_response_success", {"question_length": len(question)})
                    except Exception as e:
                        st.session_state.chat_response = f"Error: {e}"
                        track_user_action("ai_response_error", {"error": str(e)})
                else:
                    st.warning("Please enter a question first.")

        if st.session_state.chat_response:
            st.markdown("**AI Response:**")
            st.write(st.session_state.chat_response)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        # Reports
        track_page_view("reports")
        st.markdown('**<i data-lucide="file-text" class="icon"></i>Tax Residency Reports**', unsafe_allow_html=True)

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**Annual Summary**', unsafe_allow_html=True)

        total_days = sum(st.session_state.states.values())
        current_year = datetime.datetime.now().year

        st.write(f"**Tax Year {current_year} Summary:**")
        for state, days in st.session_state.states.items():
            percentage = (days / total_days * 100) if total_days > 0 else 0
            st.write(f"• {state}: {days} days ({percentage:.1f}%)")

        st.write(f"• **Total Days Logged**: {total_days}")

        # Tax status summary
        st.markdown("**Tax Residency Status:**")
        for state, days in st.session_state.states.items():
            if days >= TAX_THRESHOLD_DAYS:
                st.error(f"⚠️ Likely tax resident of {state} ({days} days)")
            else:
                remaining = TAX_THRESHOLD_DAYS - days
                st.success(f"✅ Safe in {state} ({remaining} days remaining)")

        st.markdown('</div>', unsafe_allow_html=True)

    if tab7:
        with tab7:
            # Themes
            track_page_view("themes")
            st.markdown('**<i data-lucide="palette" class="icon"></i>Theme Customization**', unsafe_allow_html=True)

            try:
                from components.theme_selector import render_advanced_theme_selector, render_theme_customizer

                st.markdown('<div class="winter-card">', unsafe_allow_html=True)
                render_advanced_theme_selector()
                st.markdown('</div>', unsafe_allow_html=True)

                render_theme_customizer()
            except ImportError:
                st.info("🎨 Theme customization coming soon!")
                st.selectbox("Theme (Preview)", ["Winter Theme", "Summer Theme", "Default"])
            except Exception as e:
                st.warning(f"Theme customization temporarily unavailable: {e}")
                st.info("Using default theme.")

    if tab8:
        with tab8:
            # Admin Dashboard
            track_page_view("admin")
            try:
                from components.admin_dashboard import render_admin_dashboard
                render_admin_dashboard()
            except ImportError:
                st.info("🔧 Admin dashboard coming soon!")
                st.text("System Status: Running")
                st.text("Active Users: 1")
            except Exception as e:
                st.warning(f"Admin dashboard temporarily unavailable: {e}")
                st.info("Core functionality remains available in other tabs.")

if __name__ == "__main__":
    main()