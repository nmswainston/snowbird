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
"""Basic styling for Snowbird app"""
import streamlit as st

def load_custom_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    .winter-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .status-safe { color: #059669; font-weight: bold; }
    .status-warning { color: #d97706; font-weight: bold; }
    .status-danger { color: #dc2626; font-weight: bold; }
    
    .icon {
        display: inline-block;
        width: 16px;
        height: 16px;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render main application header"""
    st.title("❄️ Snowbird Financial Assistant 🏖️")
    st.markdown("Helping you fly between seasons with your finances in check.")
    st.markdown("---")
