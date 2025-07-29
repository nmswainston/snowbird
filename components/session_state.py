import streamlit as st
from utils.data_models import (
    DEFAULT_STATES, DEFAULT_HOME_BUDGETS, DEFAULT_SEASONAL_CASH_FLOW,
    DEFAULT_BILLS,
)

try:
    from utils.data_models import DEFAULT_MIGRATION_CHECKLIST
except ImportError:
    # Fallback if data_models isn't available
    DEFAULT_MIGRATION_CHECKLIST = []


def initialize_session_state():
    """Initialize all session state variables with default values"""

    # Core data initialization
    if 'states' not in st.session_state:
        st.session_state.states = DEFAULT_STATES.copy()

    if 'home_budgets' not in st.session_state:
        st.session_state.home_budgets = DEFAULT_HOME_BUDGETS.copy()

    if 'seasonal_cash_flow' not in st.session_state:
        st.session_state.seasonal_cash_flow = DEFAULT_SEASONAL_CASH_FLOW.copy()

    if 'bills' not in st.session_state:
        st.session_state.bills = DEFAULT_BILLS.copy()

    if 'migration_checklist' not in st.session_state:
        st.session_state.migration_checklist = DEFAULT_MIGRATION_CHECKLIST.copy()

    # Settings and preferences
    if 'tax_threshold' not in st.session_state:
        st.session_state.tax_threshold = 183

    if 'day_log' not in st.session_state:
        st.session_state.day_log = []

    # Currency and Financial Settings
    if 'primary_currency' not in st.session_state:
        st.session_state.primary_currency = 'USD'  # Default currency

    if 'inflation_enabled' not in st.session_state:
        st.session_state.inflation_enabled = False  # Default: inflation adjustment disabled

    if 'inflation_rate' not in st.session_state:
        st.session_state.inflation_rate = 0.03  # Default: 3% annual inflation rate (as decimal)

    if 'inflation_rate_percent' not in st.session_state:
        st.session_state.inflation_rate_percent = 3.0  # Default: 3% annual inflation rate (as percentage)

    # Exchange rate cache (will be populated when needed)
    if 'exchange_rates_cache' not in st.session_state:
        st.session_state.exchange_rates_cache = {}

    if 'exchange_rates_timestamp' not in st.session_state:
        st.session_state.exchange_rates_timestamp = None

    # Feature flags
    if 'email_notifications_enabled' not in st.session_state:
        st.session_state.email_notifications_enabled = False

    if 'auto_logging_enabled' not in st.session_state:
        st.session_state.auto_logging_enabled = False

    # UI state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Dashboard"

    # Theme settings
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = "Winter Luxury"

    if 'theme_animations_enabled' not in st.session_state:
        st.session_state.theme_animations_enabled = True

    # Pro User Features and Branding
    if 'is_pro_user' not in st.session_state:
        st.session_state.is_pro_user = False  # Default: not a Pro user

    if 'custom_logo_base64' not in st.session_state:
        st.session_state.custom_logo_base64 = None  # No custom logo by default

    if 'custom_primary_color' not in st.session_state:
        st.session_state.custom_primary_color = '#0EA5E9'  # Default primary color

    if 'custom_accent_color' not in st.session_state:
        st.session_state.custom_accent_color = '#38BDF8'  # Default accent color

    if 'custom_secondary_color' not in st.session_state:
        st.session_state.custom_secondary_color = '#0284C7'  # Default secondary color

    # Onboarding tracking
    if 'onboarded' not in st.session_state:
        st.session_state.onboarded = False

    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0

    if 'onboarding_dismissed' not in st.session_state:
        st.session_state.onboarding_dismissed = False

    if 'first_day_logged' not in st.session_state:
        st.session_state.first_day_logged = False

    if 'ai_question_asked' not in st.session_state:
        st.session_state.ai_question_asked = False

def reset_session_state():
    """Reset session state to defaults"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()