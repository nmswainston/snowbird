
import streamlit as st
from utils.data_models import (
    DEFAULT_STATES, DEFAULT_HOME_BUDGETS, DEFAULT_SEASONAL_CASH_FLOW,
    DEFAULT_BILLS, DEFAULT_MIGRATION_CHECKLIST
)

def initialize_session_state():
    """Initialize all session state variables"""
    
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

def reset_session_state():
    """Reset session state to defaults"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()
