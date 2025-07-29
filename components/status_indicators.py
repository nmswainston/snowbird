
"""
Professional status indicators and notification badges for Snowbird
"""

import streamlit as st
from typing import Literal, Optional

StatusType = Literal["success", "warning", "error", "info", "neutral"]

def render_status_indicator(
    status: StatusType,
    title: str,
    message: str,
    icon: Optional[str] = None,
    action_text: Optional[str] = None,
    action_callback: Optional[callable] = None
):
    """Render a professional status indicator with optional action"""
    
    status_configs = {
        "success": {
            "color": "var(--success)",
            "bg": "color-mix(in srgb, var(--success) 10%, transparent)",
            "border": "color-mix(in srgb, var(--success) 30%, transparent)",
            "icon": icon or "check-circle"
        },
        "warning": {
            "color": "var(--warning)",
            "bg": "color-mix(in srgb, var(--warning) 10%, transparent)",
            "border": "color-mix(in srgb, var(--warning) 30%, transparent)",
            "icon": icon or "alert-triangle"
        },
        "error": {
            "color": "var(--error)",
            "bg": "color-mix(in srgb, var(--error) 10%, transparent)",
            "border": "color-mix(in srgb, var(--error) 30%, transparent)",
            "icon": icon or "x-circle"
        },
        "info": {
            "color": "var(--info)",
            "bg": "color-mix(in srgb, var(--info) 10%, transparent)",
            "border": "color-mix(in srgb, var(--info) 30%, transparent)",
            "icon": icon or "info"
        },
        "neutral": {
            "color": "var(--text-secondary)",
            "bg": "var(--overlay-light)",
            "border": "var(--border-light)",
            "icon": icon or "circle"
        }
    }
    
    config = status_configs[status]
    action_html = ""
    
    if action_text and action_callback:
        action_html = f"""
        <button class="status-action-btn" onclick="{action_callback}">
            {action_text}
        </button>
        """
    
    st.markdown(f"""
    <div class="status-indicator status-{status}">
        <div class="status-content">
            <div class="status-icon-title">
                <i data-lucide="{config['icon']}" class="status-icon"></i>
                <div class="status-text">
                    <div class="status-title">{title}</div>
                    <div class="status-message">{message}</div>
                </div>
            </div>
            {action_html}
        </div>
    </div>
    
    <style>
    .status-indicator {{
        background: {config['bg']};
        border: 1px solid {config['border']};
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    .status-indicator:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px {config['border']};
    }}
    
    .status-content {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }}
    
    .status-icon-title {{
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        flex: 1;
    }}
    
    .status-icon {{
        width: 20px;
        height: 20px;
        color: {config['color']};
        margin-top: 0.125rem;
        flex-shrink: 0;
    }}
    
    .status-text {{
        flex: 1;
    }}
    
    .status-title {{
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }}
    
    .status-message {{
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.4;
    }}
    
    .status-action-btn {{
        background: {config['color']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }}
    
    .status-action-btn:hover {{
        transform: translateY(-1px);
        box-shadow: 0 2px 8px {config['color']}40;
    }}
    
    @media (max-width: 768px) {{
        .status-content {{
            flex-direction: column;
            align-items: flex-start;
        }}
        
        .status-action-btn {{
            width: 100%;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_compact_badge(text: str, status: StatusType = "neutral", icon: Optional[str] = None):
    """Render a compact status badge"""
    status_colors = {
        "success": "var(--success)",
        "warning": "var(--warning)", 
        "error": "var(--error)",
        "info": "var(--info)",
        "neutral": "var(--text-secondary)"
    }
    
    color = status_colors[status]
    icon_html = f'<i data-lucide="{icon}" class="badge-icon-small"></i>' if icon else ''
    
    st.markdown(f"""
    <span class="compact-badge compact-badge-{status}">
        {icon_html}{text}
    </span>
    
    <style>
    .compact-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        background: color-mix(in srgb, {color} 15%, transparent);
        border: 1px solid color-mix(in srgb, {color} 30%, transparent);
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
    }}
    
    .badge-icon-small {{
        width: 12px;
        height: 12px;
    }}
    </style>
    """, unsafe_allow_html=True)
