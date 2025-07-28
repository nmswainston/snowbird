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

    # Add privacy notice in sidebar
    with st.sidebar:
        with st.expander("🔒 Privacy & Security"):
            st.markdown(get_privacy_notice())

            if st.button("Clear Session Data"):
                SessionSecurity.clear_sensitive_data()
                st.success("Session data cleared!")
                st.rerun()

    # Create main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard", 
        "📅 Day Tracker", 
        "🗺️ Auto-Track",
        "💰 Budgets", 
        "🤖 AI Assistant", 
        "📋 Reports",
        "🎨 Themes"
    ])

    with tab1:
        # Dashboard - Overview of all key metrics
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
        st.markdown('**<i data-lucide="map-pin" class="icon"></i>Log Your Location**', unsafe_allow_html=True)

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        location = st.radio("Where are you today?", ("Arizona", "Minnesota"))
        if st.button(f"Log a day in {location}"):
            st.session_state.states[location] += 1
            st.success(f"Logged a day in {location}!")
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
        st.markdown('**<i data-lucide="search" class="icon"></i>Intelligent Location Detection**', unsafe_allow_html=True)
        st.markdown("""
        <div class="winter-card">
        <p>✈️ <strong>Gmail Travel Analysis:</strong> Automatically detect travel from your email confirmations</p>
        <p>📍 <strong>GPS Location:</strong> Get your current location for manual verification</p>
        <p>📊 <strong>Audit Trail:</strong> Comprehensive logging for tax compliance</p>
        </div>
        """, unsafe_allow_html=True)

        from components.auto_tracker import render_auto_tracker
        render_auto_tracker()

    with tab4:
        # Budgets
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
        st.markdown('**<i data-lucide="brain" class="icon"></i>Ask Snowbird AI**', unsafe_allow_html=True)

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        if not openai.api_key or openai.api_key.strip() == "":
            st.info("💡 To enable AI features, add your OPENAI_API_KEY to Replit Secrets in the Tools panel.")
            st.text_area("Ask a financial question:", disabled=True, placeholder="Add OpenAI API key to enable this feature")
        else:
            question = st.text_input("Ask a financial question:")
            if st.button("Get AI Advice"):
                if question.strip():
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a friendly AI financial assistant for seasonal residents (snowbirds)."},
                                {"role": "user", "content": question}
                            ]
                        )
                        st.session_state.chat_response = response['choices'][0]['message']['content']
                    except Exception as e:
                        st.session_state.chat_response = f"Error: {e}"
                else:
                    st.warning("Please enter a question first.")

        if st.session_state.chat_response:
            st.markdown("**AI Response:**")
            st.write(st.session_state.chat_response)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        # Reports
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

    with tab7:
        # Themes
        st.markdown('**<i data-lucide="palette" class="icon"></i>Theme Customization**', unsafe_allow_html=True)

        from components.theme_selector import render_advanced_theme_selector, render_theme_customizer

        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        render_advanced_theme_selector()
        st.markdown('</div>', unsafe_allow_html=True)

        render_theme_customizer()

if __name__ == "__main__":
    main()