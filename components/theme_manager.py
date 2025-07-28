
"""
Theme Manager for Snowbird Financial Assistant
Provides comprehensive theming and styling capabilities with multiple theme options.
"""

import streamlit as st
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class ThemeColors:
    """Theme color definition"""
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    success: str
    warning: str
    error: str
    info: str
    
    # Gradients
    primary_gradient: str
    background_gradient: str
    
    # Shadows and borders
    shadow_primary: str
    shadow_light: str
    border_light: str
    border_medium: str

# Predefined themes
THEMES = {
    "winter_classic": ThemeColors(
        primary="#12BDF2",
        secondary="#0EA5E9", 
        accent="#38BDF8",
        background="#FFFFFF",
        surface="#F8FAFC",
        text_primary="#1E293B",
        text_secondary="#64748B",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #12BDF2 0%, #0EA5E9 100%)",
        background_gradient="linear-gradient(135deg, #FFFFFF 0%, #E3F4FD 100%)",
        shadow_primary="rgba(18, 189, 242, 0.15)",
        shadow_light="rgba(18, 189, 242, 0.08)",
        border_light="#E2E8F0",
        border_medium="#CBD5E1"
    ),
    
    "arctic_blue": ThemeColors(
        primary="#0369A1",
        secondary="#0284C7",
        accent="#0EA5E9",
        background="#F0F9FF",
        surface="#E0F2FE",
        text_primary="#0C4A6E",
        text_secondary="#0369A1",
        success="#059669",
        warning="#D97706",
        error="#DC2626",
        info="#2563EB",
        primary_gradient="linear-gradient(135deg, #0369A1 0%, #0284C7 100%)",
        background_gradient="linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%)",
        shadow_primary="rgba(3, 105, 161, 0.15)",
        shadow_light="rgba(3, 105, 161, 0.08)",
        border_light="#BAE6FD",
        border_medium="#7DD3FC"
    ),
    
    "warm_sunset": ThemeColors(
        primary="#EA580C",
        secondary="#DC2626",
        accent="#F97316",
        background="#FEF7ED",
        surface="#FED7AA",
        text_primary="#9A3412",
        text_secondary="#C2410C",
        success="#16A34A",
        warning="#CA8A04",
        error="#DC2626",
        info="#2563EB",
        primary_gradient="linear-gradient(135deg, #EA580C 0%, #DC2626 100%)",
        background_gradient="linear-gradient(135deg, #FEF7ED 0%, #FED7AA 100%)",
        shadow_primary="rgba(234, 88, 12, 0.15)",
        shadow_light="rgba(234, 88, 12, 0.08)",
        border_light="#FDBA74",
        border_medium="#FB923C"
    ),
    
    "forest_green": ThemeColors(
        primary="#059669",
        secondary="#047857",
        accent="#10B981",
        background="#F0FDF4",
        surface="#DCFCE7",
        text_primary="#14532D",
        text_secondary="#166534",
        success="#16A34A",
        warning="#D97706",
        error="#DC2626",
        info="#2563EB",
        primary_gradient="linear-gradient(135deg, #059669 0%, #047857 100%)",
        background_gradient="linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)",
        shadow_primary="rgba(5, 150, 105, 0.15)",
        shadow_light="rgba(5, 150, 105, 0.08)",
        border_light="#BBF7D0",
        border_medium="#86EFAC"
    ),
    
    "midnight_dark": ThemeColors(
        primary="#3B82F6",
        secondary="#1D4ED8",
        accent="#60A5FA",
        background="#0F172A",
        surface="#1E293B",
        text_primary="#F1F5F9",
        text_secondary="#CBD5E1",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)",
        background_gradient="linear-gradient(135deg, #0F172A 0%, #1E293B 100%)",
        shadow_primary="rgba(59, 130, 246, 0.25)",
        shadow_light="rgba(59, 130, 246, 0.15)",
        border_light="#334155",
        border_medium="#475569"
    )
}

class ThemeManager:
    """Centralized theme management"""
    
    @staticmethod
    def get_available_themes() -> Dict[str, str]:
        """Get list of available themes with display names"""
        return {
            "winter_classic": "❄️ Winter Classic",
            "arctic_blue": "🏔️ Arctic Blue", 
            "warm_sunset": "🌅 Warm Sunset",
            "forest_green": "🌲 Forest Green",
            "midnight_dark": "🌙 Midnight Dark"
        }
    
    @staticmethod
    def get_current_theme() -> str:
        """Get currently selected theme"""
        return st.session_state.get('selected_theme', 'winter_classic')
    
    @staticmethod
    def set_theme(theme_name: str):
        """Set the current theme"""
        if theme_name in THEMES:
            st.session_state.selected_theme = theme_name
            st.rerun()
    
    @staticmethod
    def get_theme_colors(theme_name: Optional[str] = None) -> ThemeColors:
        """Get colors for specified theme or current theme"""
        if theme_name is None:
            theme_name = ThemeManager.get_current_theme()
        return THEMES.get(theme_name, THEMES['winter_classic'])
    
    @staticmethod
    def apply_theme_css():
        """Apply the current theme's CSS"""
        theme = ThemeManager.get_theme_colors()
        
        css = f"""
        <style>
            /* Import fonts and icons */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
            
            /* CSS Variables for current theme */
            :root {{
                --primary: {theme.primary};
                --secondary: {theme.secondary};
                --accent: {theme.accent};
                --background: {theme.background};
                --surface: {theme.surface};
                --text-primary: {theme.text_primary};
                --text-secondary: {theme.text_secondary};
                --success: {theme.success};
                --warning: {theme.warning};
                --error: {theme.error};
                --info: {theme.info};
                --primary-gradient: {theme.primary_gradient};
                --background-gradient: {theme.background_gradient};
                --shadow-primary: {theme.shadow_primary};
                --shadow-light: {theme.shadow_light};
                --border-light: {theme.border_light};
                --border-medium: {theme.border_medium};
            }}
            
            /* Global app styling */
            .stApp {{
                background: var(--background-gradient);
                font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                color: var(--text-primary);
                min-height: 100vh;
            }}
            
            /* Main container */
            .main .block-container {{
                padding-top: 1rem;
                padding-bottom: 1rem;
            }}
            
            /* Header styling */
            .main-header {{
                text-align: center;
                padding: 2rem 1rem;
                background: var(--background);
                border-radius: 16px;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px var(--shadow-light);
                border: 1px solid var(--border-light);
                backdrop-filter: blur(10px);
            }}
            
            .main-title {{
                color: var(--primary);
                font-size: clamp(1.5rem, 4vw, 2.5rem);
                font-weight: 700;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .subtitle {{
                color: var(--text-secondary);
                font-size: 1rem;
                font-weight: 400;
                letter-spacing: -0.01em;
            }}
            
            /* Card styling */
            .theme-card {{
                background: var(--background);
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px var(--shadow-light);
                border: 1px solid var(--border-light);
                margin: 1rem 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(10px);
            }}
            
            .theme-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px var(--shadow-primary);
                border-color: var(--border-medium);
            }}
            
            .winter-card {{
                background: var(--background);
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px var(--shadow-light);
                border: 1px solid var(--border-light);
                margin: 1rem 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .winter-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px var(--shadow-primary);
            }}
            
            /* Button styling */
            .stButton > button {{
                background: var(--primary-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                letter-spacing: -0.01em !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 4px 12px var(--shadow-light) !important;
            }}
            
            .stButton > button:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px var(--shadow-primary) !important;
                filter: brightness(1.05) !important;
            }}
            
            .stButton > button:active {{
                transform: translateY(0) !important;
            }}
            
            /* Status indicators */
            .status-safe {{ 
                color: var(--success); 
                font-weight: 600; 
                padding: 0.25rem 0.75rem;
                background: color-mix(in srgb, var(--success) 10%, transparent);
                border-radius: 6px;
                border: 1px solid color-mix(in srgb, var(--success) 20%, transparent);
            }}
            
            .status-warning {{ 
                color: var(--warning); 
                font-weight: 600;
                padding: 0.25rem 0.75rem;
                background: color-mix(in srgb, var(--warning) 10%, transparent);
                border-radius: 6px;
                border: 1px solid color-mix(in srgb, var(--warning) 20%, transparent);
            }}
            
            .status-danger {{ 
                color: var(--error); 
                font-weight: 600;
                padding: 0.25rem 0.75rem;
                background: color-mix(in srgb, var(--error) 10%, transparent);
                border-radius: 6px;
                border: 1px solid color-mix(in srgb, var(--error) 20%, transparent);
            }}
            
            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background: var(--surface);
                padding: 0.5rem;
                border-radius: 12px;
                border: 1px solid var(--border-light);
            }}
            
            .stTabs [data-baseweb="tab"] {{
                height: 50px;
                padding: 0 1.5rem;
                background: transparent;
                border-radius: 8px;
                color: var(--text-secondary);
                border: none;
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            
            .stTabs [aria-selected="true"] {{
                background: var(--primary-gradient) !important;
                color: white !important;
                box-shadow: 0 4px 12px var(--shadow-light);
            }}
            
            /* Metric styling */
            .metric-card {{
                background: var(--background);
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px var(--shadow-light);
                border: 1px solid var(--border-light);
                text-align: center;
                transition: all 0.3s ease;
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px var(--shadow-primary);
            }}
            
            /* Sidebar styling */
            .css-1d391kg {{
                background: var(--surface) !important;
            }}
            
            /* Input styling */
            .stTextInput > div > div > input {{
                background: var(--background) !important;
                border: 1px solid var(--border-light) !important;
                border-radius: 8px !important;
                color: var(--text-primary) !important;
            }}
            
            .stSelectbox > div > div {{
                background: var(--background) !important;
                border: 1px solid var(--border-light) !important;
                border-radius: 8px !important;
            }}
            
            /* Progress bar styling */
            .stProgress > div > div > div > div {{
                background: var(--primary-gradient) !important;
            }}
            
            /* Radio button styling */
            .stRadio > div {{
                background: var(--surface);
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid var(--border-light);
            }}
            
            /* Expander styling */
            .streamlit-expanderHeader {{
                background: var(--surface) !important;
                border-radius: 8px !important;
                border: 1px solid var(--border-light) !important;
            }}
            
            /* Icon styling */
            .icon {{
                width: 16px;
                height: 16px;
                display: inline-block;
                margin-right: 8px;
                vertical-align: middle;
                color: var(--primary);
            }}
            
            .icon-large {{
                width: 24px;
                height: 24px;
                margin-right: 12px;
                color: var(--primary);
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .main-header {{
                    padding: 1.5rem 1rem;
                }}
                
                .main-title {{
                    font-size: 1.75rem !important;
                }}
                
                .theme-card, .winter-card {{
                    padding: 1rem;
                    margin: 0.5rem 0;
                }}
                
                .stButton > button {{
                    min-height: 44px !important;
                    padding: 0.8rem 1.5rem !important;
                    font-size: 1rem !important;
                }}
            }}
            
            /* Animation utilities */
            .fade-in {{
                animation: fadeIn 0.5s ease-in;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .slide-up {{
                animation: slideUp 0.3s ease-out;
            }}
            
            @keyframes slideUp {{
                from {{ transform: translateY(20px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
        </style>
        
        <!-- Lucide Icons Script -->
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                if (typeof lucide !== 'undefined') {{
                    lucide.createIcons();
                }}
            }});
            
            // Re-run icon creation after Streamlit updates
            const observer = new MutationObserver(function() {{
                if (typeof lucide !== 'undefined') {{
                    lucide.createIcons();
                }}
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});
        </script>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def render_theme_selector():
        """Render theme selection interface"""
        st.markdown('<div class="theme-card">', unsafe_allow_html=True)
        st.markdown('**🎨 Theme Selection**')
        
        current_theme = ThemeManager.get_current_theme()
        available_themes = ThemeManager.get_available_themes()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_theme = st.selectbox(
                "Choose your theme:",
                options=list(available_themes.keys()),
                format_func=lambda x: available_themes[x],
                index=list(available_themes.keys()).index(current_theme),
                key="theme_selector"
            )
        
        with col2:
            if st.button("Apply Theme", key="apply_theme_btn"):
                ThemeManager.set_theme(selected_theme)
                st.success("Theme applied!")
        
        # Theme preview
        if selected_theme != current_theme:
            st.info(f"Preview: {available_themes[selected_theme]} theme selected. Click 'Apply Theme' to activate.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_theme_preview(theme_name: str):
        """Render a preview of the specified theme"""
        theme = ThemeManager.get_theme_colors(theme_name)
        
        st.markdown(f"""
        <div style="
            background: {theme.background};
            border: 2px solid {theme.border_light};
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="color: {theme.primary}; font-weight: 600; margin-bottom: 0.5rem;">
                {THEMES[theme_name] if theme_name in THEMES else theme_name}
            </div>
            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                <div style="width: 20px; height: 20px; background: {theme.primary}; border-radius: 4px;"></div>
                <div style="width: 20px; height: 20px; background: {theme.secondary}; border-radius: 4px;"></div>
                <div style="width: 20px; height: 20px; background: {theme.accent}; border-radius: 4px;"></div>
                <div style="width: 20px; height: 20px; background: {theme.success}; border-radius: 4px;"></div>
                <div style="width: 20px; height: 20px; background: {theme.warning}; border-radius: 4px;"></div>
            </div>
            <div style="color: {theme.text_secondary}; font-size: 0.8rem;">
                Click to preview this theme
            </div>
        </div>
        """, unsafe_allow_html=True)

def initialize_theme_system():
    """Initialize the theme system"""
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = 'winter_classic'
    
    # Apply the current theme
    ThemeManager.apply_theme_css()
