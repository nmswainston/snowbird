"""
Simplified Theme Utilities
Helper functions for theming throughout the application.
"""

import streamlit as st
from components.theme_manager import ThemeManager
from typing import Optional

def themed_container(content_func, title: Optional[str] = None, icon: Optional[str] = None):
    """Create a themed container with optional title and icon"""
    st.markdown('<div class="winter-card fade-in">', unsafe_allow_html=True)

    if title:
        icon_html = f'<i data-lucide="{icon}" class="icon"></i>' if icon else ''
        st.markdown(f'**{icon_html}{title}**', unsafe_allow_html=True)

    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

def themed_metric_row(metrics: list):
    """Create a row of themed metrics"""
    cols = st.columns(len(metrics))

    for idx, metric in enumerate(metrics):
        with cols[idx]:
            from components.styles import render_metric_card
            render_metric_card(
                title=metric.get('title', ''),
                value=metric.get('value', ''),
                delta=metric.get('delta'),
                icon=metric.get('icon', 'activity')
            )

def themed_info_box(message: str, type: str = "info", icon: str = None):
    """Create a themed information box"""
    theme = ThemeManager.get_theme_colors()

    type_colors = {
        "info": theme.info,
        "success": theme.success,
        "warning": theme.warning,
        "error": theme.error
    }

    color = type_colors.get(type, theme.info)
    icon_html = f'<i data-lucide="{icon}" class="icon"></i>' if icon else ''

    st.markdown(f"""
    <div style="
        background: color-mix(in srgb, {color} 10%, transparent);
        border: 1px solid color-mix(in srgb, {color} 30%, transparent);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: {color};
    ">
        {icon_html}{message}
    </div>
    """, unsafe_allow_html=True)

def get_theme_aware_plotly_config():
    """Get Plotly configuration that matches current theme"""
    theme = ThemeManager.get_theme_colors()

    return {
        'displayModeBar': False,
        'paper_bgcolor': theme.background,
        'plot_bgcolor': theme.surface,
        'font': {'color': theme.text_primary},
        'colorway': [
            theme.primary,
            theme.secondary,
            theme.accent,
            theme.success,
            theme.warning,
            theme.error
        ]
    }