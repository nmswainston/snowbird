
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
    
    # Initialize session state
    initialize_session_state()
    
    # Load custom CSS
    load_custom_css()
    
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
    
    # Quick actions section
    render_quick_actions()
    
    # Main navigation tabs
    render_main_tabs(openai_available, openai_client)
    
    # Footer
    render_footer()

def render_quick_actions():
    """Render quick action buttons"""
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="zap" class="icon"></i>Quick Actions**', unsafe_allow_html=True)

    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

    with quick_col1:
        if st.button("📍 Log Today", type="primary", use_container_width=True):
            st.session_state.quick_log = True

    with quick_col2:
        remaining_days = {}
        for state, days in st.session_state.states.items():
            remaining_days[state] = max(0, st.session_state.tax_threshold - days)
        safest_state = min(remaining_days.keys(), key=lambda x: remaining_days[x])
        st.metric("Safest Location", safest_state, f"{remaining_days[safest_state]} days left")

    with quick_col3:
        total_monthly_budget = sum(sum(budget.values()) for budget in st.session_state.home_budgets.values())
        st.metric("Monthly Budget", f"${total_monthly_budget:,}")

    with quick_col4:
        days_until_risk = min(remaining_days.values())
        risk_color = "🟢" if days_until_risk > 30 else "🟡" if days_until_risk > 14 else "🔴"
        st.metric("Risk Level", f"{risk_color} {days_until_risk} days")

    st.markdown('</div>', unsafe_allow_html=True)

def render_main_tabs(openai_available, openai_client):
    """Render main application tabs"""
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "📅 Day Tracker", 
        "💰 Budgets", 
        "🤖 AI Assistant", 
        "📋 Reports"
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

def render_budgets_tab():
    """Render budgets management tab"""
    st.markdown('<h2><i data-lucide="wallet" class="icon"></i>Budget Management</h2>', unsafe_allow_html=True)
    
    # Implementation would go here
    st.info("Budget management functionality - implement based on existing code")

def render_ai_assistant_tab(openai_available, openai_client):
    """Render AI assistant tab"""
    st.markdown('<h2><i data-lucide="bot" class="icon"></i>AI Financial Assistant</h2>', unsafe_allow_html=True)
    
    if not openai_available:
        st.warning("AI features require an OpenAI API key. Add your OPENAI_API_KEY to Replit Secrets to enable this feature.")
    else:
        st.info("AI Assistant functionality - implement based on existing code")

def render_reports_tab():
    """Render reports tab"""
    st.markdown('<h2><i data-lucide="file-text" class="icon"></i>Tax Residency Reports</h2>', unsafe_allow_html=True)
    
    # Implementation would go here
    st.info("Reports functionality - implement based on existing code")

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

if __name__ == "__main__":
    main()
