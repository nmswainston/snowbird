import streamlit as st
from utils.data_models import (
    DEFAULT_STATES, DEFAULT_HOME_BUDGETS, DEFAULT_SEASONAL_CASH_FLOW,
    DEFAULT_BILLS, DEFAULT_MIGRATION_CHECKLIST
)

def initialize_session_state():
    """Initialize session state variables with default values"""

    # Try to load saved data first
    try:
        from utils.data_persistence import load_user_data
        if load_user_data():
            # Data loaded successfully, add any missing keys
            if 'data_loaded' not in st.session_state:
                st.session_state.data_loaded = True
            return
    except ImportError:
        pass  # data_persistence module not available
    except Exception as e:
        st.warning(f"Could not load saved data: {e}")

    # Use defaults if no saved data

    # Core data
    if "states" not in st.session_state:
        st.session_state.states = DEFAULT_STATES.copy()

    if "home_budgets" not in st.session_state:
        st.session_state.home_budgets = DEFAULT_HOME_BUDGETS.copy()

    if "seasonal_cash_flow" not in st.session_state:
        st.session_state.seasonal_cash_flow = DEFAULT_SEASONAL_CASH_FLOW.copy()

    if "bills" not in st.session_state:
        st.session_state.bills = DEFAULT_BILLS.copy()

    if "migration_checklist" not in st.session_state:
        st.session_state.migration_checklist = DEFAULT_MIGRATION_CHECKLIST.copy()

    # Logging and history
    if "day_log" not in st.session_state:
        st.session_state.day_log = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "notification_history" not in st.session_state:
        st.session_state.notification_history = []

    # Settings
    if "tax_threshold" not in st.session_state:
        st.session_state.tax_threshold = 183

    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True

    # Preferences
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    if "alert_frequency" not in st.session_state:
        st.session_state.alert_frequency = "Weekly"

    if "auto_weekend" not in st.session_state:
        st.session_state.auto_weekend = False

    if "auto_travel" not in st.session_state:
        st.session_state.auto_travel = False

    if "auto_bills" not in st.session_state:
        st.session_state.auto_bills = False

    # Email notification preferences
    if "email_notifications" not in st.session_state:
        st.session_state.email_notifications = False
    
    if "daily_email_time" not in st.session_state:
        st.session_state.daily_email_time = "09:00"

def reset_session_state():
    """Reset session state to defaults"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()