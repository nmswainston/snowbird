import streamlit as st
from components.theme_manager import ThemeManager, initialize_theme_system

def load_custom_css():
    """Load custom CSS styles for the Snowbird app using theme system"""
    # Initialize and apply theme system
    initialize_theme_system()
    ThemeManager.apply_theme_css()
    
    # Apply light/dark theme toggle
    apply_theme_toggle()
    
    # Add accessibility improvements
    from utils.accessibility import add_accessibility_css
    add_accessibility_css()

def apply_theme_toggle():
    """Apply light/dark theme based on user selection"""
    # Get theme from session state, default to Light
    theme = st.session_state.get("theme", "Light")
    
    if theme == "Dark":
        # Inject dark mode CSS
        st.markdown("""
        <style>
        /* Dark theme override styles */
        .stApp {
            background-color: #121212 !important;
            color: #eeeeee !important;
        }
        
        body {
            background-color: #121212 !important;
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
        
        .winter-card {
            background: #1e1e1e !important;
            border: 1px solid #333333 !important;
            color: #eeeeee !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #2d2d2d !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }
        
        .stSelectbox > div > div {
            background-color: #2d2d2d !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }
        
        .stDateInput > div > div > input {
            background-color: #2d2d2d !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }
        
        .stNumberInput > div > div > input {
            background-color: #2d2d2d !important;
            border-color: #444444 !important;
            color: #eeeeee !important;
        }
        
        /* Sidebar dark theme */
        .css-1d391kg {
            background-color: #1a1a1a !important;
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
        
        /* Headers and text */
        h1, h2, h3, h4, h5, h6 {
            color: #eeeeee !important;
        }
        
        .stMarkdown {
            color: #eeeeee !important;
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
        
        # Update session state when selection changes
        if theme_option != st.session_state.get("theme", "Light"):
            st.session_state["theme"] = theme_option
            st.rerun()

def render_main_header():
    """Render the enhanced sleek application header"""
    st.markdown("""
    <div class="main-header fade-in floating">
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
    """Render a premium styled metric card with enhanced effects"""
    delta_html = f'<div style="color: var(--success); font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">{delta}</div>' if delta else ""

    st.markdown(f"""
    <div class="metric-card slide-up pulse-glow">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <i data-lucide="{icon}" class="icon-large" style="margin-right: 0.75rem; filter: drop-shadow(0 0 8px var(--primary));"></i>
            <span style="color: var(--text-secondary); font-size: 1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{title}</span>
        </div>
        <div style="color: var(--primary); font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem; text-shadow: var(--glow-primary);">{value}</div>
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
"""Basic styling for Snowbird app"""
import streamlit as st

def load_custom_css():
    """Load custom CSS styles"""
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
    </style>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render main application header"""
    st.title("❄️ Snowbird Financial Assistant 🏖️")
    st.markdown("Helping you fly between seasons with your finances in check.")
    st.markdown("---")
