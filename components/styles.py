"""
Simplified styling for Snowbird app using the enhanced theme system
"""

import streamlit as st
from components.theme_manager import ThemeManager, initialize_theme_system

def load_custom_css():
    """Load custom CSS styles for the Snowbird app using theme system"""
    # Initialize and apply theme system
    initialize_theme_system()
    ThemeManager.apply_theme_css()

    # Apply Pro user custom branding if available
    apply_pro_branding()

    # Apply light/dark theme toggle if needed
    apply_theme_toggle()

def apply_theme_toggle():
    """Apply light/dark theme based on user selection"""
    theme = st.session_state.get("theme", "Light")

    if theme == "Dark":
        st.markdown("""
        <style>
        /* Dark theme overrides */
        .stApp {
            background-color: #121212 !important;
            color: #eeeeee !important;
        }

        .winter-card {
            background: #1e1e1e !important;
            border: 1px solid #333333 !important;
            color: #eeeeee !important;
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stDateInput > div > div > input,
        .stNumberInput > div > div > input {
            background-color: #2d2d2d !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }

        .css-1d391kg {
            background-color: #1a1a1a !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #eeeeee !important;
        }

                .stButton>button {
            background-color: #444444 !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }

        .stButton>button:hover {
            background-color: #555555 !important;
            border-color: #555555 !important;
        }
        /* Tabs dark theme */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2d2d2d !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #1e1e1e !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #444444 !important;
            color: #eeeeee !important;
        }
        /* Progress bars */
        .stProgress > div > div {
            background-color: #333333 !important;
        }

        /* Metric cards */
        [data-testid="metric-container"] {
            background-color: #1e1e1e !important;
            border: 1px solid #333333 !important;
        }
        /* Success/warning/error messages */
        .stSuccess {
            background-color: #1a4a1a !important;
            color: #90ee90 !important;
        }

        .stWarning {
            background-color: #4a4a1a !important;
            color: #ffff90 !important;
        }

        .stError {
            background-color: #4a1a1a !important;
            color: #ff9090 !important;
        }

        .stInfo {
            background-color: #1a1a4a !important;
            color: #9090ff !important;
        }
        </style>
        """, unsafe_allow_html=True)

def render_theme_toggle():
    """Render theme toggle in sidebar"""
    with st.sidebar:
        st.markdown("### 🎨 Theme")
        theme_option = st.radio(
            "Choose theme:",
            options=["Light", "Dark"],
            index=0 if st.session_state.get("theme", "Light") == "Light" else 1,
            key="theme_toggle"
        )

        if theme_option != st.session_state.get("theme", "Light"):
            st.session_state["theme"] = theme_option
            st.rerun()

def render_main_header():
    """Render the enhanced application header with Pro branding support"""
    try:
        from utils.branding_manager import BrandingManager

        # Use custom header if Pro user with branding
        if BrandingManager.is_pro_user():
            BrandingManager.render_custom_header()
            return

    except ImportError:
        # Branding manager not available, use standard header
        pass
    except Exception:
        # Any error, fall back to standard header
        pass

    # Standard header for non-Pro users or fallback
    st.markdown("""
    <div class="main-header fade-in">
        <h1 class="main-title">
            <i data-lucide="home" class="icon-large"></i>
            Snowbird: Your Seasonal Financial Assistant
        </h1>
        <p class="subtitle">Manage your multi-state lifestyle with confidence and style</p>
        <div style="margin-top: 1rem; opacity: 0.7; font-size: 0.9rem;">
            <i data-lucide="sparkles" class="icon"></i>
            Premium Financial Management Experience
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, delta: str = None, icon: str = "activity"):
    """Render a styled metric card"""
    delta_html = f'<div style="color: var(--success); font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">{delta}</div>' if delta else ""

    st.markdown(f"""
    <div class="metric-card slide-up">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <i data-lucide="{icon}" class="icon-large" style="margin-right: 0.75rem;"></i>
            <span style="color: var(--text-secondary); font-size: 1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{title}</span>
        </div>
        <div style="color: var(--primary); font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">{value}</div>
        {delta_html}
        <div style="position: absolute; top: 1rem; right: 1rem; opacity: 0.3;">
            <i data-lucide="trending-up" style="width: 20px; height: 20px; color: var(--accent);"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str, text: str):
    """Render a status badge with appropriate styling"""
    st.markdown(f'<span class="status-{status}">{text}</span>', unsafe_allow_html=True)

def render_icon(name: str, size: str = "16", color: str = None):
    """Render a Lucide icon without React conflicts"""
    color_style = f'color: {color};' if color else ''
    # Use span instead of i to avoid React conflicts
    st.markdown(f'<span class="lucide-icon" data-icon="{name}" style="width: {size}px; height: {size}px; {color_style}; display: inline-block;"></span>', unsafe_allow_html=True)

def apply_pro_branding():
    """Apply Pro user custom branding if available"""
    try:
        from utils.branding_manager import BrandingManager

        # Apply custom branding CSS for Pro users
        custom_css = BrandingManager.apply_custom_branding_css()
        if custom_css:
            st.markdown(custom_css, unsafe_allow_html=True)

    except ImportError:
        # Branding manager not available, skip custom branding
        pass
    except Exception:
        # Any other error, fail silently to not break the app
        pass

def apply_basic_styles():
    """Basic styling for Snowbird app"""
    st.markdown("""
    <style>
    /* Light-blue accent for CTAs - consistent branding */
    .stButton>button {
        background-color: #AEDFF7 !important;
        border-color: #AEDFF7 !important;
        color: #1E293B !important;
        font-weight: 600 !important;
    }

    .stButton>button:hover {
        background-color: #8FD0F0 !important;
        border-color: #8FD0F0 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(174, 223, 247, 0.3) !important;
    }

    .stButton>button:active {
        background-color: #6FC1E8 !important;
        transform: translateY(0) !important;
    }

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

    .lucide-icon {
        display: inline-block;
        margin-right: 8px;
    }

    /* Prevent React conflicts with icons */
    [data-lucide]:not([data-rendered]) {
        opacity: 0;
    }

    [data-lucide][data-rendered] {
        opacity: 1;
        transition: opacity 0.2s ease;
    }

    /* PWA-specific styles */
    .pwa-standalone {
        padding-top: env(safe-area-inset-top);
        padding-bottom: env(safe-area-inset-bottom);
    }

    @media (display-mode: standalone) {
        body {
            -webkit-user-select: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
        }

        /* Hide Streamlit's hamburger menu in standalone mode */
        .css-1rs6os .css-17ziqus {
            display: none;
        }
    }

    /* Install button styling */
    #pwa-install-btn {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .winter-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }

        .main-title {
            font-size: 1.5rem;
        }
    }

    .status-danger { 
        color: var(--error);
        font-weight: 700;
        padding: 0.5rem 1rem;
        background: color-mix(in srgb, var(--error) 15%, transparent);
        border-radius: 12px;
        border: 2px solid color-mix(in srgb, var(--error) 30%, transparent);
        box-shadow: 0 0 20px color-mix(in srgb, var(--error) 20%, transparent);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

    # Add mobile optimizations
    st.markdown("""
    <style>
    /* Mobile-first responsive design with island vibes */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 0.5rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }

        /* Stack columns on mobile */
        .row-widget.stHorizontal > div {
            flex-direction: column !important;
            width: 100% !important;
        }

        /* Improve button sizes for touch */
        .stButton > button {
            min-height: 48px;
            font-size: 16px;
            border-radius: 12px;
            font-weight: 600;
        }

        /* Better tab sizing for mobile */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab-list"] button {
            font-size: 13px;
            padding: 6px 8px;
            border-radius: 8px;
            min-width: auto;
            flex: 1;
        }

        /* Better metric display on mobile */
        .metric-container {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 12px;
            text-align: center;
        }

        /* Improve form inputs on mobile */
        .stSelectbox > div > div {
            font-size: 16px; /* Prevents zoom on iOS */
        }

        .stTextInput > div > div > input {
            font-size: 16px; /* Prevents zoom on iOS */
        }

        /* Better spacing for mobile cards */
        .dashboard-card {
            margin-bottom: 1rem;
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Improve header on mobile */
        h1 {
            font-size: 1.75rem !important;
            line-height: 1.2;
        }

        h2 {
            font-size: 1.5rem !important;
            line-height: 1.3;
        }

        /* Better progress bars on mobile */
        .stProgress > div > div > div {
            border-radius: 8px;
            height: 12px;
        }

        /* Improve expander styling on mobile */
        .streamlit-expanderHeader {
            font-size: 16px;
            padding: 12px;
        }
    }

    /* Tablet optimizations */
    @media (max-width: 1024px) and (min-width: 769px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }

        .stTabs [data-baseweb="tab-list"] button {
            font-size: 14px;
            padding: 10px 16px;
        }
    }

    /* App theme colors and animations */
    .hawaii-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
        border: 1px solid #0ea5e9;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .hawaii-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
    }

    /* Improved loading animations */
    .loading-pulse {
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* Better touch targets */
    .touch-friendly {
        min-height: 44px;
        min-width: 44px;
        padding: 12px;
    }

    /* Professional header with enhanced branding */
    .main-header {
        text-align: center;
        padding: 2.5rem 2rem;
        background: var(--overlay-light);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-heavy);
        border: 1px solid var(--border-light);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--primary-gradient);
        opacity: 0.8;
    }

    .header-content {
        position: relative;
        z-index: 2;
    }

    .brand-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        gap: 1rem;
    }

    .icon-brand {
        width: 48px;
        height: 48px;
        color: var(--primary);
        filter: drop-shadow(0 0 12px var(--primary));
    }

    .brand-text {
        text-align: left;
    }

    .main-title {
        color: var(--primary);
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.04em;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }

    .brand-tagline {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
        margin-top: 0.25rem;
    }

    .subtitle {
        color: var(--text-secondary);
        font-size: 1.125rem;
        font-weight: 500;
        letter-spacing: -0.01em;
        opacity: 0.9;
        margin-bottom: 1.5rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .header-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .feature-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--overlay-medium);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-light);
        border-radius: 24px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }

    .feature-badge:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-secondary);
        border-color: var(--primary);
    }

    .badge-icon {
        width: 16px;
        height: 16px;
        color: var(--primary);
    }

    </style>
    """, unsafe_allow_html=True)
# Enhanced visual polish and branding are added to the CSS styles, focusing on improving the main header and overall visual presentation.