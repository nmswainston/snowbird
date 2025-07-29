import streamlit as st
import time
from typing import Optional

def show_loading(message: str = "Loading...", duration: Optional[float] = None):
    """Show a loading message with spinner"""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; 
                    background-color: #f0f8ff; border-radius: 8px; border-left: 4px solid #0ea5e9;">
            <div style="margin-right: 10px;">🔄</div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)

    if duration:
        time.sleep(duration)
        placeholder.empty()

    return placeholder

def show_success(message: str, duration: float = 2.0):
    """Show a success message"""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; 
                    background-color: #f0fdf4; border-radius: 8px; border-left: 4px solid #22c55e;">
            <div style="margin-right: 10px;">✅</div>
            <div style="color: #16a34a;">{message}</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(duration)
    placeholder.empty()

def show_error(message: str, duration: float = 3.0):
    """Show an error message"""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; 
                    background-color: #fef2f2; border-radius: 8px; border-left: 4px solid #ef4444;">
            <div style="margin-right: 10px;">❌</div>
            <div style="color: #dc2626;">{message}</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(duration)
    placeholder.empty()

def show_warning(message: str, duration: float = 2.5):
    """Show a warning message"""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; 
                    background-color: #fffbeb; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <div style="margin-right: 10px;">⚠️</div>
            <div style="color: #d97706;">{message}</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(duration)
    placeholder.empty()

def show_info(message: str, duration: float = 2.0):
    """Show an info message"""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; 
                    background-color: #f0f9ff; border-radius: 8px; border-left: 4px solid #0ea5e9;">
            <div style="margin-right: 10px;">ℹ️</div>
            <div style="color: #0284c7;">{message}</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(duration)
    placeholder.empty()

def create_status_indicator(status: str, message: str = "") -> str:
    """Create a status indicator HTML"""
    status_configs = {
        'online': {'color': '#22c55e', 'icon': '🟢', 'text': 'Online'},
        'offline': {'color': '#ef4444', 'icon': '🔴', 'text': 'Offline'},
        'syncing': {'color': '#f59e0b', 'icon': '🔄', 'text': 'Syncing'},
        'error': {'color': '#ef4444', 'icon': '❌', 'text': 'Error'},
        'warning': {'color': '#f59e0b', 'icon': '⚠️', 'text': 'Warning'}
    }

    config = status_configs.get(status, status_configs['offline'])
    display_text = message or config['text']

    return f"""
    <div style="display: inline-flex; align-items: center; padding: 0.25rem 0.5rem; 
                background-color: {config['color']}20; border-radius: 12px; 
                border: 1px solid {config['color']}40;">
        <span style="margin-right: 4px;">{config['icon']}</span>
        <span style="color: {config['color']}; font-size: 0.875rem;">{display_text}</span>
    </div>
    """

def show_connection_status():
    """Show real-time connection status"""
    from utils.profile_sync import get_sync_status

    status = get_sync_status()

    if status['is_syncing']:
        st.markdown(create_status_indicator('syncing', 'Real-time sync active'), unsafe_allow_html=True)
    else:
        st.markdown(create_status_indicator('offline', 'Sync inactive'), unsafe_allow_html=True)

    if status['last_remote_sync']:
        st.caption(f"Last synced: {status['last_remote_sync'].strftime('%I:%M:%S %p')}")