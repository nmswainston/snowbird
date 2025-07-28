"""
Simplified Theme Selector Component
"""

import streamlit as st
from components.theme_manager import ThemeManager, THEMES

def render_theme_selector():
    """Render theme selector with previews"""
    st.markdown("### 🎨 Theme Selection")

    available_themes = ThemeManager.get_available_themes()
    current_theme = ThemeManager.get_current_theme()

    # Create columns for theme previews
    cols = st.columns(len(available_themes))

    for idx, (theme_key, theme_name) in enumerate(available_themes.items()):
        with cols[idx]:
            theme_colors = THEMES[theme_key]
            is_current = theme_key == current_theme

            border_style = "border: 3px solid var(--primary);" if is_current else "border: 1px solid var(--border-light);"

            preview_html = f"""
            <div style="
                {border_style}
                border-radius: 12px;
                padding: 1rem;
                background: {theme_colors.background};
                margin-bottom: 0.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
            ">
                <div style="color: {theme_colors.primary}; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">
                    {theme_name}
                </div>
                <div style="display: flex; justify-content: center; gap: 4px; margin-bottom: 0.5rem;">
                    <div style="width: 16px; height: 16px; background: {theme_colors.primary}; border-radius: 50%;"></div>
                    <div style="width: 16px; height: 16px; background: {theme_colors.secondary}; border-radius: 50%;"></div>
                    <div style="width: 16px; height: 16px; background: {theme_colors.accent}; border-radius: 50%;"></div>
                </div>
                <div style="color: {theme_colors.text_secondary}; font-size: 0.7rem;">
                    {'✓ Active' if is_current else 'Click to apply'}
                </div>
            </div>
            """

            st.markdown(preview_html, unsafe_allow_html=True)

            if st.button("Apply", key=f"theme_{theme_key}", help=f"Apply {theme_name} theme"):
                ThemeManager.set_theme(theme_key)
                st.success(f"Applied {theme_name} theme!")
                st.rerun()

def render_theme_sidebar():
    """Render theme selector in sidebar"""
    with st.sidebar:
        with st.expander("🎨 Themes", expanded=False):
            available_themes = ThemeManager.get_available_themes()
            current_theme = ThemeManager.get_current_theme()

            selected_theme = st.selectbox(
                "Select Theme:",
                options=list(available_themes.keys()),
                format_func=lambda x: available_themes[x],
                index=list(available_themes.keys()).index(current_theme),
                key="sidebar_theme_selector"
            )

            if selected_theme != current_theme:
                if st.button("Apply Theme", key="sidebar_apply_theme"):
                    ThemeManager.set_theme(selected_theme)
                    st.rerun()