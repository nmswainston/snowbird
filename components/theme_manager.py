"""
Enhanced Theme Manager for Snowbird Financial Assistant
Provides comprehensive theming with premium sleek styling and visual effects.
"""

import streamlit as st
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ThemeColors:
    """Enhanced theme color definition with additional sleek properties"""
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

    # Enhanced gradients for sleek design
    primary_gradient: str
    secondary_gradient: str
    background_gradient: str
    surface_gradient: str
    accent_gradient: str

    # Sophisticated shadows and effects
    shadow_primary: str
    shadow_secondary: str
    shadow_light: str
    shadow_heavy: str
    glow_primary: str
    glow_accent: str

    # Enhanced borders and overlays
    border_light: str
    border_medium: str
    border_heavy: str
    overlay_light: str
    overlay_medium: str

# Premium sleek themes
THEMES = {
    "winter_luxury": ThemeColors(
        primary="#0EA5E9",
        secondary="#0284C7", 
        accent="#38BDF8",
        background="#FAFBFC",
        surface="#FFFFFF",
        text_primary="#0F172A",
        text_secondary="#475569",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #0EA5E9 0%, #0284C7 50%, #0369A1 100%)",
        secondary_gradient="linear-gradient(135deg, #0284C7 0%, #0369A1 100%)",
        background_gradient="linear-gradient(135deg, #FAFBFC 0%, #F1F5F9 50%, #E2E8F0 100%)",
        surface_gradient="linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)",
        accent_gradient="linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%)",
        shadow_primary="0 10px 25px -5px rgba(14, 165, 233, 0.25)",
        shadow_secondary="0 4px 15px -2px rgba(14, 165, 233, 0.15)",
        shadow_light="0 2px 8px -1px rgba(0, 0, 0, 0.08)",
        shadow_heavy="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        glow_primary="0 0 30px rgba(14, 165, 233, 0.3)",
        glow_accent="0 0 20px rgba(56, 189, 248, 0.4)",
        border_light="#E2E8F0",
        border_medium="#CBD5E1",
        border_heavy="#94A3B8",
        overlay_light="rgba(255, 255, 255, 0.8)",
        overlay_medium="rgba(255, 255, 255, 0.95)"
    ),

    "midnight_premium": ThemeColors(
        primary="#6366F1",
        secondary="#4F46E5",
        accent="#8B5CF6",
        background="#0F0F23",
        surface="#1E1E3A",
        text_primary="#F1F5F9",
        text_secondary="#CBD5E1",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #3730A3 100%)",
        secondary_gradient="linear-gradient(135deg, #4F46E5 0%, #3730A3 100%)",
        background_gradient="linear-gradient(135deg, #0F0F23 0%, #1E1B4B 50%, #312E81 100%)",
        surface_gradient="linear-gradient(135deg, #1E1E3A 0%, #2D2D5A 100%)",
        accent_gradient="linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)",
        shadow_primary="0 10px 25px -5px rgba(99, 102, 241, 0.4)",
        shadow_secondary="0 4px 15px -2px rgba(99, 102, 241, 0.25)",
        shadow_light="0 2px 8px -1px rgba(0, 0, 0, 0.3)",
        shadow_heavy="0 25px 50px -12px rgba(0, 0, 0, 0.6)",
        glow_primary="0 0 30px rgba(99, 102, 241, 0.5)",
        glow_accent="0 0 20px rgba(139, 92, 246, 0.6)",
        border_light="#374151",
        border_medium="#4B5563",
        border_heavy="#6B7280",
        overlay_light="rgba(15, 15, 35, 0.8)",
        overlay_medium="rgba(15, 15, 35, 0.95)"
    ),

    "forest_modern": ThemeColors(
        primary="#059669",
        secondary="#047857",
        accent="#10B981",
        background="#F0FDF7",
        surface="#FFFFFF",
        text_primary="#064E3B",
        text_secondary="#047857",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #059669 0%, #047857 50%, #065F46 100%)",
        secondary_gradient="linear-gradient(135deg, #047857 0%, #065F46 100%)",
        background_gradient="linear-gradient(135deg, #F0FDF7 0%, #ECFDF5 50%, #D1FAE5 100%)",
        surface_gradient="linear-gradient(135deg, #FFFFFF 0%, #F9FDF9 100%)",
        accent_gradient="linear-gradient(135deg, #10B981 0%, #059669 100%)",
        shadow_primary="0 10px 25px -5px rgba(5, 150, 105, 0.25)",
        shadow_secondary="0 4px 15px -2px rgba(5, 150, 105, 0.15)",
        shadow_light="0 2px 8px -1px rgba(0, 0, 0, 0.08)",
        shadow_heavy="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        glow_primary="0 0 30px rgba(5, 150, 105, 0.3)",
        glow_accent="0 0 20px rgba(16, 185, 129, 0.4)",
        border_light="#D1FAE5",
        border_medium="#A7F3D0",
        border_heavy="#6EE7B7",
        overlay_light="rgba(240, 253, 247, 0.8)",
        overlay_medium="rgba(240, 253, 247, 0.95)"
    ),
    "sunset_elite": ThemeColors(
        primary="#EA580C",
        secondary="#DC2626",
        accent="#F97316",
        background="#FEF9F3",
        surface="#FFFFFF",
        text_primary="#9A3412",
        text_secondary="#C2410C",
        success="#10B981",
        warning="#F59E0B",
        error="#DC2626",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #EA580C 0%, #DC2626 50%, #B91C1C 100%)",
        secondary_gradient="linear-gradient(135deg, #DC2626 0%, #B91C1C 100%)",
        background_gradient="linear-gradient(135deg, #FEF9F3 0%, #FED7AA 50%, #FDBA74 100%)",
        surface_gradient="linear-gradient(135deg, #FFFFFF 0%, #FEF9F3 100%)",
        accent_gradient="linear-gradient(135deg, #F97316 0%, #EA580C 100%)",
        shadow_primary="0 10px 25px -5px rgba(234, 88, 12, 0.25)",
        shadow_secondary="0 4px 15px -2px rgba(234, 88, 12, 0.15)",
        shadow_light="0 2px 8px -1px rgba(0, 0, 0, 0.08)",
        shadow_heavy="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        glow_primary="0 0 30px rgba(234, 88, 12, 0.3)",
        glow_accent="0 0 20px rgba(249, 115, 22, 0.4)",
        border_light="#FED7AA",
        border_medium="#FDBA74",
        border_heavy="#FB923C",
        overlay_light="rgba(254, 249, 243, 0.8)",
        overlay_medium="rgba(254, 249, 243, 0.95)"
    ),
    
    "arctic_glass": ThemeColors(
        primary="#0891B2",
        secondary="#0E7490",
        accent="#06B6D4",
        background="#F0FDFF",
        surface="#FFFFFF",
        text_primary="#083344",
        text_secondary="#0E7490",
        success="#10B981",
        warning="#F59E0B",
        error="#EF4444",
        info="#3B82F6",
        primary_gradient="linear-gradient(135deg, #0891B2 0%, #0E7490 50%, #155E75 100%)",
        secondary_gradient="linear-gradient(135deg, #0E7490 0%, #155E75 100%)",
        background_gradient="linear-gradient(135deg, #F0FDFF 0%, #E6FFFA 50%, #CCFBF1 100%)",
        surface_gradient="linear-gradient(135deg, #FFFFFF 0%, #F0FDFF 100%)",
        accent_gradient="linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)",
        shadow_primary="0 10px 25px -5px rgba(8, 145, 178, 0.25)",
        shadow_secondary="0 4px 15px -2px rgba(8, 145, 178, 0.15)",
        shadow_light="0 2px 8px -1px rgba(0, 0, 0, 0.08)",
        shadow_heavy="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        glow_primary="0 0 30px rgba(8, 145, 178, 0.3)",
        glow_accent="0 0 20px rgba(6, 182, 212, 0.4)",
        border_light="#CCFBF1",
        border_medium="#99F6E4",
        border_heavy="#5EEAD4",
        overlay_light="rgba(240, 253, 255, 0.8)",
        overlay_medium="rgba(240, 253, 255, 0.95)"
    )
}

class ThemeManager:
    """Enhanced theme management with sleek design features"""

    @staticmethod
    def get_available_themes() -> Dict[str, str]:
        """Get list of available sleek themes"""
        return {
            "winter_luxury": "❄️ Winter Luxury",
            "midnight_premium": "🌙 Midnight Premium", 
            "forest_modern": "🌲 Forest Modern",
            "sunset_elite": "🌅 Sunset Elite",
            "arctic_glass": "🏔️ Arctic Glass"
        }

    @staticmethod
    def get_current_theme() -> str:
        """Get currently selected theme"""
        return st.session_state.get('selected_theme', 'winter_luxury')

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
        return THEMES.get(theme_name, THEMES['winter_luxury'])

    @staticmethod
    def apply_theme_css():
        """Apply enhanced sleek theme CSS"""
        theme = ThemeManager.get_theme_colors()

        css = f"""
        <style>
            /* Premium font imports - Enhanced typography */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Satoshi:wght@300;400;500;600;700;800;900&display=swap');
            
            /* Fallback for Satoshi font */
            @font-face {
                font-family: 'Satoshi-Fallback';
                src: local('Inter'), local('system-ui'), local('-apple-system');
                font-weight: 100 900;
                font-style: normal;
            }

            /* Enhanced CSS Variables */
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

                /* Enhanced gradients */
                --primary-gradient: {theme.primary_gradient};
                --secondary-gradient: {theme.secondary_gradient};
                --background-gradient: {theme.background_gradient};
                --surface-gradient: {theme.surface_gradient};
                --accent-gradient: {theme.accent_gradient};

                /* Sophisticated shadows */
                --shadow-primary: {theme.shadow_primary};
                --shadow-secondary: {theme.shadow_secondary};
                --shadow-light: {theme.shadow_light};
                --shadow-heavy: {theme.shadow_heavy};
                --glow-primary: {theme.glow_primary};
                --glow-accent: {theme.glow_accent};

                /* Enhanced borders */
                --border-light: {theme.border_light};
                --border-medium: {theme.border_medium};
                --border-heavy: {theme.border_heavy};
                --overlay-light: {theme.overlay_light};
                --overlay-medium: {theme.overlay_medium};
            }}

            /* Global sleek styling with enhanced typography */
            .stApp {{
                background: var(--background-gradient);
                font-family: 'Plus Jakarta Sans', 'Satoshi', 'Satoshi-Fallback', 'Manrope', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                color: var(--text-primary);
                min-height: 100vh;
                font-weight: 400;
                line-height: 1.7;
                letter-spacing: -0.005em;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                text-rendering: optimizeLegibility;
                font-feature-settings: "liga" 1, "kern" 1, "calt" 1;
            }}
            
            /* Enhanced typography hierarchy */
            h1, h2, h3, h4, h5, h6 {{
                font-family: 'Satoshi', 'Plus Jakarta Sans', 'Manrope', system-ui, sans-serif;
                font-weight: 700;
                letter-spacing: -0.02em;
                line-height: 1.3;
                margin-bottom: 0.75em;
                color: var(--text-primary);
            }}
            
            h1 {{ 
                font-size: clamp(2rem, 5vw, 3.5rem); 
                font-weight: 800; 
                letter-spacing: -0.04em; 
            }}
            
            h2 {{ 
                font-size: clamp(1.5rem, 4vw, 2.5rem); 
                font-weight: 700; 
                letter-spacing: -0.03em; 
            }}
            
            h3 {{ 
                font-size: clamp(1.25rem, 3vw, 2rem); 
                font-weight: 600; 
                letter-spacing: -0.02em; 
            }}
            
            h4 {{ 
                font-size: clamp(1.125rem, 2.5vw, 1.5rem); 
                font-weight: 600; 
            }}
            
            h5 {{ 
                font-size: clamp(1rem, 2vw, 1.25rem); 
                font-weight: 600; 
            }}
            
            h6 {{ 
                font-size: clamp(0.875rem, 1.5vw, 1.125rem); 
                font-weight: 600; 
            }}
            
            /* Enhanced body text */
            p, .stMarkdown p {{
                font-family: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif;
                font-weight: 400;
                line-height: 1.7;
                letter-spacing: -0.003em;
                margin-bottom: 1em;
                color: var(--text-primary);
            }}
            
            /* Enhanced code and monospace */
            code, pre, .stCode {{
                font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'JetBrains Mono', 'Fira Code', monospace;
                font-feature-settings: "liga" 1, "calt" 1;
                font-variant-ligatures: contextual;
            }}

            /* Sleek container styling */
            .main .block-container {{
                padding: 2rem 1rem;
                max-width: 1200px;
                margin: 0 auto;
            }}

            /* Premium header with glass effect */
            .main-header {{
                text-align: center;
                padding: 2rem 1.5rem;
                background: var(--overlay-light);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 12px;
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow-light);
                border: 0.5px solid var(--border-light);
                position: relative;
                overflow: hidden;
            }}

            .main-header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: var(--primary-gradient);
                opacity: 0.6;
            }}

            .main-title {{
                color: var(--primary);
                font-family: 'Satoshi', 'Plus Jakarta Sans', system-ui, sans-serif;
                font-size: clamp(2.25rem, 6vw, 4rem);
                font-weight: 900;
                margin-bottom: 1rem;
                letter-spacing: -0.04em;
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: var(--glow-primary);
                line-height: 1.1;
                text-rendering: optimizeLegibility;
                font-feature-settings: "liga" 1, "kern" 1;
            }}

            .subtitle {{
                color: var(--text-secondary);
                font-family: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif;
                font-size: clamp(1.125rem, 2.5vw, 1.375rem);
                font-weight: 500;
                letter-spacing: -0.015em;
                opacity: 0.9;
                line-height: 1.5;
                max-width: 42em;
                margin: 0 auto;
            }}
            
            .brand-tagline {{
                font-family: 'Inter', system-ui, sans-serif;
                font-size: clamp(0.875rem, 1.5vw, 1rem);
                font-weight: 600;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                opacity: 0.8;
                margin-top: 0.5rem;
            }}

            /* Enhanced glass-effect cards */
            .theme-card, .winter-card {{
                background: var(--overlay-light);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: var(--shadow-light);
                border: 0.5px solid var(--border-light);
                margin: 1rem 0;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
            }}

            .theme-card::before, .winter-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: var(--accent-gradient);
                opacity: 0;
                transition: opacity 0.3s ease;
            }}

            .theme-card:hover, .winter-card:hover {{
                transform: translateY(-8px);
                box-shadow: var(--shadow-heavy);
                border-color: var(--border-medium);
            }}

            .theme-card:hover::before, .winter-card:hover::before {{
                opacity: 1;
            }}

            /* Premium button styling with enhanced typography */
            .stButton > button {{
                background: var(--primary-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 14px !important;
                padding: 1rem 2rem !important;
                font-family: 'Satoshi', 'Plus Jakarta Sans', system-ui, sans-serif !important;
                font-weight: 700 !important;
                font-size: clamp(0.875rem, 1.5vw, 1rem) !important;
                letter-spacing: 0.025em !important;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                box-shadow: var(--shadow-secondary) !important;
                position: relative !important;
                overflow: hidden !important;
                text-transform: uppercase !important;
                min-height: 54px !important;
                text-rendering: optimizeLegibility !important;
            }}

            .stButton > button::before {{
                content: '' !important;
                position: absolute !important;
                top: 0 !important;
                left: -100% !important;
                width: 100% !important;
                height: 100% !important;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
                transition: left 0.5s !important;
            }}

            .stButton > button:hover {{
                transform: translateY(-4px) scale(1.02) !important;
                box-shadow: var(--glow-primary) !important;
                filter: brightness(1.1) !important;
            }}

            .stButton > button:hover::before {{
                left: 100% !important;
            }}

            .stButton > button:active {{
                transform: translateY(-2px) scale(0.98) !important;
            }}

            /* Enhanced status indicators with glow */
            .status-safe {{ 
                color: var(--success);
                font-weight: 700;
                padding: 0.5rem 1rem;
                background: color-mix(in srgb, var(--success) 15%, transparent);
                border-radius: 12px;
                border: 2px solid color-mix(in srgb, var(--success) 30%, transparent);
                box-shadow: 0 0 20px color-mix(in srgb, var(--success) 20%, transparent);
                backdrop-filter: blur(10px);
            }}

            .status-warning {{ 
                color: var(--warning);
                font-weight: 700;
                padding: 0.5rem 1rem;
                background: color-mix(in srgb, var(--warning) 15%, transparent);
                border-radius: 12px;
                border: 2px solid color-mix(in srgb, var(--warning) 30%, transparent);
                box-shadow: 0 0 20px color-mix(in srgb, var(--warning) 20%, transparent);
                backdrop-filter: blur(10px);
            }}

            .status-danger {{ 
                color: var(--error);
                font-weight: 700;
                padding: 0.5rem 1rem;
                background: color-mix(in srgb, var(--error) 15%, transparent);
                border-radius: 12px;
                border: 2px solid color-mix(in srgb, var(--error) 30%, transparent);
                box-shadow: 0 0 20px color-mix(in srgb, var(--error) 20%, transparent);
                backdrop-filter: blur(10px);
            }}

            /* Sleek tabs with floating effect */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background: transparent;
                backdrop-filter: none;
                padding: 0.25rem;
                border-radius: 8px;
                border: none;
                box-shadow: none;
            }}

            .stTabs [data-baseweb="tab"] {{
                height: 44px;
                padding: 0 1.5rem;
                background: transparent;
                border-radius: 8px;
                color: var(--text-secondary);
                border: 0.5px solid var(--border-light);
                font-family: 'Satoshi', 'Plus Jakarta Sans', system-ui, sans-serif;
                font-weight: 600;
                font-size: clamp(0.875rem, 1.5vw, 0.95rem);
                letter-spacing: -0.01em;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                text-rendering: optimizeLegibility;
            }}

            .stTabs [aria-selected="true"] {{
                background: var(--primary-gradient) !important;
                color: white !important;
                box-shadow: var(--shadow-secondary);
                transform: scale(1.05);
            }}

            /* Premium metric cards */
            .metric-card {{
                background: var(--overlay-light);
                backdrop-filter: blur(10px);
                padding: 1.25rem;
                border-radius: 10px;
                box-shadow: var(--shadow-light);
                border: 0.5px solid var(--border-light);
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
            }}

            .metric-card::after {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: var(--accent-gradient);
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
            }}

            .metric-card:hover {{
                transform: translateY(-6px) scale(1.02);
                box-shadow: var(--shadow-primary);
                border-color: var(--border-medium);
            }}

            .metric-card:hover::after {{
                opacity: 0.1;
            }}

            /* Enhanced sidebar with glass effect */
            .css-1d391kg {{
                background: var(--overlay-medium) !important;
                backdrop-filter: blur(20px) !important;
                border-right: 1px solid var(--border-light) !important;
            }}

            /* Sleek input styling with enhanced typography */
            .stTextInput > div > div > input {{
                background: var(--overlay-light) !important;
                border: 0.5px solid var(--border-light) !important;
                border-radius: 8px !important;
                color: var(--text-primary) !important;
                font-family: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif !important;
                font-weight: 500 !important;
                font-size: 0.95rem !important;
                letter-spacing: -0.005em !important;
                padding: 0.75rem 1rem !important;
                transition: all 0.3s ease !important;
                backdrop-filter: blur(5px) !important;
                line-height: 1.5 !important;
            }}
            
            .stTextInput > div > div > input::placeholder {{
                color: var(--text-secondary) !important;
                opacity: 0.7 !important;
                font-weight: 400 !important;
            }}
            
            .stNumberInput > div > div > input,
            .stDateInput > div > div > input,
            .stTimeInput > div > div > input {{
                font-family: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif !important;
                font-weight: 500 !important;
                font-size: 0.95rem !important;
                letter-spacing: -0.005em !important;
            }}

            .stTextInput > div > div > input:focus {{
                border-color: var(--primary) !important;
                box-shadow: 0 0 0 1px var(--primary) !important;
                transform: none !important;
            }}

            .stSelectbox > div > div {{
                background: var(--overlay-light) !important;
                border: 0.5px solid var(--border-light) !important;
                border-radius: 8px !important;
                backdrop-filter: blur(5px) !important;
                transition: all 0.3s ease !important;
            }}

            .stSelectbox > div > div:hover {{
                border-color: var(--primary) !important;
                box-shadow: var(--shadow-light) !important;
            }}

            /* Enhanced progress bars */
            .stProgress > div > div > div > div {{
                background: var(--primary-gradient) !important;
                border-radius: 8px !important;
                box-shadow: var(--glow-primary) !important;
            }}
            
            /* Sleek expanders */
            .streamlit-expanderHeader {{
                background: var(--overlay-light) !important;
                border-radius: 8px !important;
                border: 0.5px solid var(--border-light) !important;
                backdrop-filter: blur(5px) !important;
                transition: all 0.3s ease !important;
            }}
            
            .streamlit-expanderHeader:hover {{
                box-shadow: var(--shadow-light) !important;
                transform: translateY(-2px) !important;
            }}

            /* Icon styling with glow effects */
            .icon {{
                width: 18px;
                height: 18px;
                display: inline-block;
                margin-right: 8px;
                vertical-align: middle;
                color: var(--primary);
                filter: drop-shadow(0 0 4px var(--primary));
            }}

            .icon-large {{
                width: 28px;
                height: 28px;
                margin-right: 12px;
                color: var(--primary);
                filter: drop-shadow(0 0 8px var(--primary));
            }}

            /* Mobile responsiveness with enhanced spacing */
            @media (max-width: 768px) {{
                .main-header {{
                    padding: 2rem 1.5rem;
                    border-radius: 20px;
                }}

                .main-title {{
                    font-size: 2rem !important;
                }}

                .theme-card, .winter-card {{
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border-radius: 16px;
                }}

                .stButton > button {{
                    min-height: 48px !important;
                    padding: 0.875rem 1.5rem !important;
                    font-size: 0.95rem !important;
                }}
            }}

            /* Advanced animations */
            .fade-in {{
                animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            @keyframes fadeInUp {{
                0% {{ 
                    opacity: 0; 
                    transform: translateY(30px) scale(0.95);
                }}
                100% {{ 
                    opacity: 1; 
                    transform: translateY(0) scale(1);
                }}
            }}

            .slide-up {{
                animation: slideUpScale 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            @keyframes slideUpScale {{
                0% {{ 
                    transform: translateY(40px) scale(0.9);
                    opacity: 0;
                }}
                100% {{ 
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }}
            }}
            
            /* Floating animation for interactive elements */
            .floating {{
                animation: floating 3s ease-in-out infinite;
            }}
            
            @keyframes floating {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
            }}
            
            /* Pulse animation for important elements */
            .pulse-glow {{
                animation: pulseGlow 2s ease-in-out infinite;
            }}
            
            @keyframes pulseGlow {{
                0%, 100% {{ 
                    box-shadow: var(--shadow-light);
                }}
                50% {{ 
                    box-shadow: var(--glow-primary);
                }}
            }}
        </style>

        <!-- Enhanced Lucide Icons Script -->
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
        <script>
            // Enhanced icon initialization with smooth transitions
            function initializeIcons() {{
                if (typeof lucide !== 'undefined') {{
                    lucide.createIcons();
                    
                    // Add smooth transitions to icons
                    document.querySelectorAll('[data-lucide]').forEach(icon => {{
                        icon.style.transition = 'all 0.3s ease';
                    }});
                }}
            }}

            document.addEventListener('DOMContentLoaded', initializeIcons);

            // Enhanced mutation observer for dynamic content
            const observer = new MutationObserver(function(mutations) {{
                let shouldUpdate = false;
                mutations.forEach(mutation => {{
                    if (mutation.addedNodes.length > 0) {{
                        shouldUpdate = true;
                    }}
                }});

                if (shouldUpdate) {{
                    setTimeout(initializeIcons, 100);
                }}
            }});

            observer.observe(document.body, {{ 
                childList: true, 
                subtree: true,
                attributes: false 
            }});

            // Add smooth scrolling
            document.documentElement.style.scrollBehavior = 'smooth';
        </script>
        """

        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def render_theme_selector():
        """Render enhanced theme selection interface"""
        st.markdown('<div class="theme-card fade-in">', unsafe_allow_html=True)
        st.markdown('**🎨 Premium Theme Selection**')

        current_theme = ThemeManager.get_current_theme()
        available_themes = ThemeManager.get_available_themes()

        col1, col2 = st.columns([3, 1])

        with col1:
            selected_theme = st.selectbox(
                "Choose your premium theme:",
                options=list(available_themes.keys()),
                format_func=lambda x: available_themes[x],
                index=list(available_themes.keys()).index(current_theme),
                key="theme_selector"
            )

        with col2:
            if st.button("Apply Theme", key="apply_theme_btn"):
                ThemeManager.set_theme(selected_theme)
                st.success("✨ Premium theme applied!")

        # Enhanced theme preview
        if selected_theme != current_theme:
            st.info(f"🎭 Preview: **{available_themes[selected_theme]}** theme selected. Click 'Apply Theme' to activate this premium experience.")

        st.markdown('</div>', unsafe_allow_html=True)

def initialize_theme_system():
    """Initialize the enhanced theme system"""
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = 'winter_luxury'

    # Apply the current theme with enhanced effects
    ThemeManager.apply_theme_css()