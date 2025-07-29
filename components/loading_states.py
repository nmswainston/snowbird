
"""
Professional loading states and micro-interactions for Snowbird
"""

import streamlit as st
import time
from typing import Optional, Callable, Any

def render_loading_spinner(message: str = "Loading...", duration: Optional[float] = None):
    """Render a professional loading spinner with message"""
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-message">{message}</div>
    </div>
    
    <style>
    .loading-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        gap: 1rem;
    }}
    
    .loading-spinner {{
        width: 40px;
        height: 40px;
        border: 3px solid var(--border-light);
        border-top: 3px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.3);
    }}
    
    .loading-message {{
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.95rem;
        text-align: center;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if duration:
        time.sleep(duration)

def render_skeleton_loader(lines: int = 3, height: str = "20px"):
    """Render skeleton loading placeholders"""
    skeleton_html = ""
    for i in range(lines):
        width = "100%" if i < lines - 1 else "75%"
        skeleton_html += f'<div class="skeleton-line" style="width: {width}; height: {height};"></div>'
    
    st.markdown(f"""
    <div class="skeleton-container">
        {skeleton_html}
    </div>
    
    <style>
    .skeleton-container {{
        padding: 1rem;
        gap: 0.75rem;
        display: flex;
        flex-direction: column;
    }}
    
    .skeleton-line {{
        background: linear-gradient(90deg, var(--border-light) 25%, var(--surface) 50%, var(--border-light) 75%);
        background-size: 200% 100%;
        border-radius: 4px;
        animation: shimmer 1.5s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def with_loading_state(func: Callable, loading_message: str = "Processing..."):
    """Decorator to add loading state to functions"""
    def wrapper(*args, **kwargs):
        with st.spinner(loading_message):
            return func(*args, **kwargs)
    return wrapper

def render_progress_card(title: str, current: int, total: int, description: str = ""):
    """Render a professional progress card"""
    percentage = (current / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class="progress-card">
        <div class="progress-header">
            <h4 class="progress-title">{title}</h4>
            <span class="progress-percentage">{percentage:.1f}%</span>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {percentage}%;"></div>
        </div>
        <div class="progress-details">
            <span class="progress-current">{current} of {total}</span>
            {f'<span class="progress-description">{description}</span>' if description else ''}
        </div>
    </div>
    
    <style>
    .progress-card {{
        background: var(--overlay-light);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }}
    
    .progress-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-secondary);
    }}
    
    .progress-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .progress-title {{
        margin: 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
    }}
    
    .progress-percentage {{
        color: var(--primary);
        font-weight: 700;
        font-size: 1.2rem;
    }}
    
    .progress-bar-container {{
        background: var(--border-light);
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }}
    
    .progress-bar {{
        background: var(--primary-gradient);
        height: 100%;
        border-radius: 8px;
        transition: width 0.6s ease;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
    }}
    
    .progress-details {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.9rem;
    }}
    
    .progress-current {{
        color: var(--text-secondary);
        font-weight: 500;
    }}
    
    .progress-description {{
        color: var(--text-secondary);
        font-style: italic;
    }}
    </style>
    """, unsafe_allow_html=True)
