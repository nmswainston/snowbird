import streamlit as st
from components.theme_manager import ThemeManager, initialize_theme_system

def load_custom_css():
    """Load custom CSS styles for the Snowbird app using theme system"""
    # Initialize and apply theme system
    initialize_theme_system()
    ThemeManager.apply_theme_css()

def render_main_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header fade-in">
        <h1 class="main-title">
            <i data-lucide="home" class="icon-large"></i>
            Snowbird: Your Seasonal Financial Assistant
        </h1>
        <p class="subtitle">Manage your multi-state lifestyle with confidence</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, delta: str = None, icon: str = "activity"):
    """Render a styled metric card"""
    delta_html = f'<div style="color: var(--success); font-size: 0.8rem; margin-top: 0.25rem;">{delta}</div>' if delta else ""

    st.markdown(f"""
    <div class="metric-card slide-up">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 0.5rem;">
            <i data-lucide="{icon}" class="icon" style="margin-right: 0.5rem;"></i>
            <span style="color: var(--text-secondary); font-size: 0.9rem; font-weight: 500;">{title}</span>
        </div>
        <div style="color: var(--primary); font-size: 1.8rem; font-weight: 700;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str, text: str):
    """Render a status badge with appropriate styling"""
    st.markdown(f'<span class="status-{status}">{text}</span>', unsafe_allow_html=True)

def render_icon(name: str, size: str = "16", color: str = None):
    """Render a Lucide icon"""
    color_style = f'color: {color};' if color else ''
    st.markdown(f'<i data-lucide="{name}" style="width: {size}px; height: {size}px; {color_style}"></i>', unsafe_allow_html=True)