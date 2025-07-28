import streamlit as st
import datetime
import os
import json
import csv
from io import StringIO

# Configure Streamlit with winter theme
st.set_page_config(
    page_title="❄️ Snowbird AI Financial Assistant", 
    layout="wide",
    page_icon="❄️",
    initial_sidebar_state="expanded"
)

# Initialize theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Initialize all session state variables
def initialize_session_state():
    defaults = {
        "states": {"Arizona": 0, "Minnesota": 0},
        "home_budgets": {
            "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
            "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
        },
        "seasonal_cash_flow": {
            "Travel": 300,
            "Healthcare": 400,
            "Supplemental Insurance": 200
        },
        "tax_threshold": 183,
        "chat_response": "",
        "day_log": [],
        "location_enabled": False,
        "current_location": None,
        "last_nudge_date": None,
        "active_tab": "Log Location"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, dict) else value

initialize_session_state()

# State tax information database
state_tax_info = {
    "Alabama": {"income_tax": "2.0% - 5.0%", "sales_tax": "4.0%", "property_tax": "0.41%", "retirement_friendly": "Moderate"},
    "Alaska": {"income_tax": "None", "sales_tax": "None", "property_tax": "1.19%", "retirement_friendly": "High"},
    "Arizona": {"income_tax": "2.59% - 4.5%", "sales_tax": "5.6%", "property_tax": "0.66%", "retirement_friendly": "High"},
    "Arkansas": {"income_tax": "2.0% - 5.9%", "sales_tax": "6.5%", "property_tax": "0.63%", "retirement_friendly": "Moderate"},
    "California": {"income_tax": "1.0% - 13.3%", "sales_tax": "7.25%", "property_tax": "0.75%", "retirement_friendly": "Low"},
    "Colorado": {"income_tax": "4.4%", "sales_tax": "2.9%", "property_tax": "0.51%", "retirement_friendly": "Moderate"},
    "Connecticut": {"income_tax": "3.0% - 6.99%", "sales_tax": "6.35%", "property_tax": "2.14%", "retirement_friendly": "Low"},
    "Delaware": {"income_tax": "0% - 6.6%", "sales_tax": "None", "property_tax": "0.57%", "retirement_friendly": "High"},
    "Florida": {"income_tax": "None", "sales_tax": "6.0%", "property_tax": "0.83%", "retirement_friendly": "Very High"},
    "Georgia": {"income_tax": "1.0% - 5.75%", "sales_tax": "4.0%", "property_tax": "0.93%", "retirement_friendly": "Moderate"},
    "Hawaii": {"income_tax": "1.4% - 11.0%", "sales_tax": "4.0%", "property_tax": "0.28%", "retirement_friendly": "Moderate"},
    "Idaho": {"income_tax": "1.125% - 6.925%", "sales_tax": "6.0%", "property_tax": "0.69%", "retirement_friendly": "Moderate"},
    "Illinois": {"income_tax": "4.95%", "sales_tax": "6.25%", "property_tax": "2.27%", "retirement_friendly": "Low"},
    "Indiana": {"income_tax": "3.23%", "sales_tax": "7.0%", "property_tax": "0.87%", "retirement_friendly": "Moderate"},
    "Iowa": {"income_tax": "0.33% - 8.53%", "sales_tax": "6.0%", "property_tax": "1.56%", "retirement_friendly": "Moderate"},
    "Kansas": {"income_tax": "3.1% - 5.7%", "sales_tax": "6.5%", "property_tax": "1.41%", "retirement_friendly": "Moderate"},
    "Kentucky": {"income_tax": "5.0%", "sales_tax": "6.0%", "property_tax": "0.86%", "retirement_friendly": "Moderate"},
    "Louisiana": {"income_tax": "1.85% - 4.25%", "sales_tax": "4.45%", "property_tax": "0.56%", "retirement_friendly": "Moderate"},
    "Maine": {"income_tax": "5.8% - 7.15%", "sales_tax": "5.5%", "property_tax": "1.28%", "retirement_friendly": "Low"},
    "Maryland": {"income_tax": "2.0% - 5.75%", "sales_tax": "6.0%", "property_tax": "1.09%", "retirement_friendly": "Low"},
    "Massachusetts": {"income_tax": "5.0%", "sales_tax": "6.25%", "property_tax": "1.23%", "retirement_friendly": "Low"},
    "Michigan": {"income_tax": "4.25%", "sales_tax": "6.0%", "property_tax": "1.54%", "retirement_friendly": "Moderate"},
    "Minnesota": {"income_tax": "5.35% - 9.85%", "sales_tax": "6.875%", "property_tax": "1.12%", "retirement_friendly": "Low"},
    "Mississippi": {"income_tax": "0% - 5.0%", "sales_tax": "7.0%", "property_tax": "0.81%", "retirement_friendly": "High"},
    "Missouri": {"income_tax": "1.5% - 5.4%", "sales_tax": "4.225%", "property_tax": "0.97%", "retirement_friendly": "Moderate"},
    "Montana": {"income_tax": "1.0% - 6.9%", "sales_tax": "None", "property_tax": "0.84%", "retirement_friendly": "Moderate"},
    "Nebraska": {"income_tax": "2.46% - 6.84%", "sales_tax": "5.5%", "property_tax": "1.73%", "retirement_friendly": "Moderate"},
    "Nevada": {"income_tax": "None", "sales_tax": "4.6%", "property_tax": "0.53%", "retirement_friendly": "Very High"},
    "New Hampshire": {"income_tax": "None*", "sales_tax": "None", "property_tax": "2.20%", "retirement_friendly": "High"},
    "New Jersey": {"income_tax": "1.4% - 10.75%", "sales_tax": "6.625%", "property_tax": "2.49%", "retirement_friendly": "Very Low"},
    "New Mexico": {"income_tax": "1.7% - 5.9%", "sales_tax": "5.125%", "property_tax": "0.80%", "retirement_friendly": "Moderate"},
    "New York": {"income_tax": "4.0% - 10.9%", "sales_tax": "4.0%", "property_tax": "1.69%", "retirement_friendly": "Low"},
    "North Carolina": {"income_tax": "4.99%", "sales_tax": "4.75%", "property_tax": "0.84%", "retirement_friendly": "Moderate"},
    "North Dakota": {"income_tax": "1.1% - 2.9%", "sales_tax": "5.0%", "property_tax": "1.04%", "retirement_friendly": "High"},
    "Ohio": {"income_tax": "0% - 3.99%", "sales_tax": "5.75%", "property_tax": "1.62%", "retirement_friendly": "Moderate"},
    "Oklahoma": {"income_tax": "0.25% - 5.0%", "sales_tax": "4.5%", "property_tax": "0.90%", "retirement_friendly": "Moderate"},
    "Oregon": {"income_tax": "4.75% - 9.9%", "sales_tax": "None", "property_tax": "0.93%", "retirement_friendly": "Moderate"},
    "Pennsylvania": {"income_tax": "3.07%", "sales_tax": "6.0%", "property_tax": "1.58%", "retirement_friendly": "High"},
    "Rhode Island": {"income_tax": "3.75% - 5.99%", "sales_tax": "7.0%", "property_tax": "1.63%", "retirement_friendly": "Low"},
    "South Carolina": {"income_tax": "0% - 7.0%", "sales_tax": "6.0%", "property_tax": "0.57%", "retirement_friendly": "High"},
    "South Dakota": {"income_tax": "None", "sales_tax": "4.2%", "property_tax": "1.31%", "retirement_friendly": "Very High"},
    "Tennessee": {"income_tax": "None", "sales_tax": "7.0%", "property_tax": "0.74%", "retirement_friendly": "Very High"},
    "Texas": {"income_tax": "None", "sales_tax": "6.25%", "property_tax": "1.80%", "retirement_friendly": "High"},
    "Utah": {"income_tax": "4.85%", "sales_tax": "6.1%", "property_tax": "0.58%", "retirement_friendly": "Moderate"},
    "Vermont": {"income_tax": "3.35% - 8.75%", "sales_tax": "6.0%", "property_tax": "1.90%", "retirement_friendly": "Low"},
    "Virginia": {"income_tax": "2.0% - 5.75%", "sales_tax": "5.3%", "property_tax": "0.81%", "retirement_friendly": "Moderate"},
    "Washington": {"income_tax": "None", "sales_tax": "6.5%", "property_tax": "0.94%", "retirement_friendly": "High"},
    "West Virginia": {"income_tax": "3.0% - 6.5%", "sales_tax": "6.0%", "property_tax": "0.60%", "retirement_friendly": "Moderate"},
    "Wisconsin": {"income_tax": "3.54% - 7.65%", "sales_tax": "5.0%", "property_tax": "1.85%", "retirement_friendly": "Moderate"},
    "Wyoming": {"income_tax": "None", "sales_tax": "4.0%", "property_tax": "0.62%", "retirement_friendly": "Very High"}
}

# Session state initialization
if "states" not in st.session_state:
    st.session_state.states = {"Arizona": 0, "Minnesota": 0}
if "home_budgets" not in st.session_state:
    st.session_state.home_budgets = {
        "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
        "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
    }
if "seasonal_cash_flow" not in st.session_state:
    st.session_state.seasonal_cash_flow = {
        "Travel": 300,
        "Healthcare": 400,
        "Supplemental Insurance": 200
    }
if "tax_threshold" not in st.session_state:
    st.session_state.tax_threshold = 183
if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""
if "state_tax_info" not in st.session_state:
    st.session_state.state_tax_info = state_tax_info
if "day_log" not in st.session_state:
    st.session_state.day_log = []
if "location_enabled" not in st.session_state:
    st.session_state.location_enabled = False
if "current_location" not in st.session_state:
    st.session_state.current_location = None
if "last_nudge_date" not in st.session_state:
    st.session_state.last_nudge_date = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Log Location"

# Winter theme CSS with enhanced navigation
def get_winter_theme_css():
    base_theme = """
    <style>
    /* CSS Variables for theme switching */
    :root {
        --primary-color: #12BDF2;
        --background-color: """ + ("#0D2540" if st.session_state.dark_mode else "#FFFFFF") + """;
        --secondary-bg-color: """ + ("#1a3a5c" if st.session_state.dark_mode else "#F0F4F8") + """;
        --text-color: """ + ("#FFFFFF" if st.session_state.dark_mode else "#0D2540") + """;
        --accent-color: """ + ("#F0F4F8" if st.session_state.dark_mode else "#12BDF2") + """;
        --card-bg: """ + ("#1a3a5c" if st.session_state.dark_mode else "#FFFFFF") + """;
        --border-color: """ + ("#2a4a6c" if st.session_state.dark_mode else "#E2E8F0") + """;
        --shadow: """ + ("rgba(18, 189, 242, 0.2)" if st.session_state.dark_mode else "rgba(13, 37, 64, 0.1)") + """;
        --gradient-start: #12BDF2;
        --gradient-end: #0891D1;
        --tab-active: """ + ("#12BDF2" if st.session_state.dark_mode else "#12BDF2") + """;
        --tab-inactive: """ + ("#2a4a6c" if st.session_state.dark_mode else "#F0F4F8") + """;
    }

    /* Auto-detect system preference */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #0D2540;
            --secondary-bg-color: #1a3a5c;
            --text-color: #FFFFFF;
            --card-bg: #1a3a5c;
            --border-color: #2a4a6c;
            --shadow: rgba(18, 189, 242, 0.2);
            --tab-inactive: #2a4a6c;
        }
    }

    /* Base styling */
    .stApp {
        background: var(--background-color) !important;
        color: var(--text-color) !important;
    }

    .main > div {
        padding: 1rem;
        background: var(--background-color);
        color: var(--text-color);
    }

    /* Snowflake animation */
    @keyframes snowfall {
        0% { transform: translateY(-100vh) translateX(0px); opacity: 1; }
        100% { transform: translateY(100vh) translateX(100px); opacity: 0; }
    }

    .snowflake {
        position: fixed;
        top: -10px;
        z-index: 1;
        user-select: none;
        pointer-events: none;
        animation: snowfall linear infinite;
        color: var(--primary-color);
        opacity: 0.6;
    }

    /* Winter header styling */
    .winter-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(18, 189, 242, 0.3);
    }

    .winter-subtitle {
        text-align: center;
        color: var(--text-color);
        opacity: 0.8;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-style: italic;
    }

    /* Enhanced Tab Navigation */
    .tab-container {
        background: var(--secondary-bg-color);
        border-radius: 15px;
        padding: 0.5rem;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 20px var(--shadow);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }

    .tab-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }

    .tab-button {
        padding: 12px 20px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        min-width: 120px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .tab-button.active {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(18, 189, 242, 0.4);
        transform: translateY(-2px);
    }

    .tab-button.inactive {
        background: var(--tab-inactive);
        color: var(--text-color);
        opacity: 0.8;
        border: 1px solid var(--border-color);
    }

    .tab-button.inactive:hover {
        background: var(--primary-color);
        color: white;
        opacity: 1;
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(18, 189, 242, 0.3);
    }

    .tab-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .tab-button:hover::before {
        left: 100%;
    }

    /* Winter cards */
    .winter-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px var(--shadow);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .winter-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow);
    }

    .winter-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(18, 189, 242, 0.05) 0%, transparent 70%);
        animation: shimmer 4s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
    }

    .ice-card {
        background: linear-gradient(135deg, rgba(18, 189, 242, 0.1) 0%, rgba(240, 244, 248, 0.1) 100%);
        border: 1px solid rgba(18, 189, 242, 0.3);
        backdrop-filter: blur(15px);
    }

    .frost-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(18, 189, 242, 0.3);
        box-shadow: 0 8px 32px rgba(18, 189, 242, 0.15);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(18, 189, 242, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(18, 189, 242, 0.5) !important;
        filter: brightness(1.1) !important;
    }

    /* Sidebar styling */
    .stSidebar > div {
        background: var(--secondary-bg-color) !important;
        border-right: 2px solid var(--border-color) !important;
    }

    /* Theme toggle */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(18, 189, 242, 0.4);
        transition: all 0.3s ease;
        font-size: 1.2rem;
    }

    .theme-toggle:hover {
        transform: scale(1.1) rotate(15deg);
        box-shadow: 0 6px 20px rgba(18, 189, 242, 0.6);
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
        border-radius: 10px !important;
    }

    .stProgress > div > div {
        background: var(--secondary-bg-color) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Form elements */
    .stSelectbox > div > div, 
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--secondary-bg-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-color) !important;
        transition: all 0.3s ease !important;
    }

    .stSelectbox > div > div:focus-within, 
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 10px rgba(18, 189, 242, 0.3) !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background: var(--secondary-bg-color);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(18, 189, 242, 0.3);
        backdrop-filter: blur(10px);
    }

    /* Status indicators */
    .status-safe { color: #10B981; font-weight: bold; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
    .status-warning { color: #F59E0B; font-weight: bold; text-shadow: 0 0 10px rgba(245, 158, 11, 0.3); }
    .status-danger { color: #EF4444; font-weight: bold; text-shadow: 0 0 10px rgba(239, 68, 68, 0.3); }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
        text-align: center;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .tab-row {
            flex-direction: column;
            align-items: stretch;
        }

        .tab-button {
            min-width: auto;
            margin: 0.25rem 0;
        }

        .winter-header {
            font-size: 2rem;
        }

        .winter-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }

        .theme-toggle {
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.8rem;
        }
    }

    @media (max-width: 480px) {
        .main > div {
            padding: 0.5rem;
        }

        .winter-header {
            font-size: 1.5rem;
        }
    }

    /* Data tables */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px var(--shadow);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--secondary-bg-color);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--gradient-end);
    }
    </style>
    """
    return base_theme

# Apply theme CSS
st.markdown(get_winter_theme_css(), unsafe_allow_html=True)

# Snowflake animation
snowflake_script = """
<script>
function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.className = 'snowflake';
    snowflake.innerHTML = ['❄', '❅', '❆'][Math.floor(Math.random() * 3)];
    snowflake.style.left = Math.random() * 100 + 'vw';
    snowflake.style.animationDuration = Math.random() * 4 + 3 + 's';
    snowflake.style.opacity = Math.random() * 0.6 + 0.2;
    snowflake.style.fontSize = Math.random() * 8 + 12 + 'px';
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 7000);
}

setInterval(createSnowflake, 500);
</script>
"""
st.components.v1.html(snowflake_script, height=0)

# Header with theme toggle
header_col1, header_col2 = st.columns([9, 1])
with header_col1:
    st.markdown('<h1 class="winter-header">❄️ Snowbird AI Financial Assistant 🏖️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="winter-subtitle">Navigate your seasonal finances with intelligence and style</p>', unsafe_allow_html=True)

with header_col2:
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(f"{theme_icon}", key="theme_toggle", help="Toggle day/night mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Navigation Tabs
tab_options = [
    ("📍 Log Location", "Log Location"),
    ("💰 Budget", "Budget"), 
    ("💸 Seasonal Cash Flow", "Seasonal Cash Flow"),
    ("📅 Residency Tracker", "Residency Tracker"),
    ("🏛️ State Tax Info", "State Tax Info"),
    ("🤖 AI Advice", "AI Advice"),
    ("🔄 Reset", "Reset")
]

st.markdown('<div class="tab-container">', unsafe_allow_html=True)
tab_cols = st.columns(len(tab_options))

for i, (tab_display, tab_key) in enumerate(tab_options):
    with tab_cols[i]:
        button_class = "active" if st.session_state.active_tab == tab_key else "inactive"
        if st.button(tab_display, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = tab_key
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Import page modules
def load_location_page():
    from pages import location_tracking
    location_tracking.show_page()

def load_budget_page():
    from pages import budget_management
    budget_management.show_page()

def load_seasonal_page():
    from pages import seasonal_cash_flow
    seasonal_cash_flow.show_page()

def load_residency_page():
    from pages import residency_tracker
    residency_tracker.show_page()

def load_tax_info_page():
    from pages import state_tax_info
    state_tax_info.show_page()

def load_ai_page():
    from pages import ai_advice
    ai_advice.show_page()

def load_reset_page():
    from pages import reset_data
    reset_data.show_page()

# Route to appropriate page
try:
    if st.session_state.active_tab == "Log Location":
        load_location_page()
    elif st.session_state.active_tab == "Budget":
        load_budget_page()
    elif st.session_state.active_tab == "Seasonal Cash Flow":
        load_seasonal_page()
    elif st.session_state.active_tab == "Residency Tracker":
        load_residency_page()
    elif st.session_state.active_tab == "State Tax Info":
        load_tax_info_page()
    elif st.session_state.active_tab == "AI Advice":
        load_ai_page()
    elif st.session_state.active_tab == "Reset":
        load_reset_page()
except Exception as e:
    st.error(f"Error loading page: {e}")
    st.info("Creating page structure... Please wait.")

# Sidebar settings
with st.sidebar:
    st.markdown('<div class="winter-card"><h2>⚙️ Global Settings</h2></div>', unsafe_allow_html=True)

    # Theme settings
    st.subheader("🎨 Theme Settings")
    theme_mode = st.radio(
        "Choose theme mode:",
        options=["Auto (System)", "Day Mode ☀️", "Night Mode 🌙"],
        index=0 if not hasattr(st.session_state, 'manual_theme') else 
              (1 if not st.session_state.dark_mode else 2)
    )

    if theme_mode == "Day Mode ☀️":
        st.session_state.dark_mode = False
        st.session_state.manual_theme = True
    elif theme_mode == "Night Mode 🌙":
        st.session_state.dark_mode = True
        st.session_state.manual_theme = True
    else:
        st.session_state.manual_theme = False

    # Quick stats
    st.subheader("📊 Quick Stats")
    total_days = sum(st.session_state.states.values())
    st.metric("Total Days Logged", total_days)

    # Show current date and status
    today = datetime.date.today()
    st.write(f"📅 Today: {today.strftime('%B %d, %Y')}")

    # Day streak info
    if st.session_state.day_log:
        recent_logs = [log for log in st.session_state.day_log 
                      if log['date'] >= (today - datetime.timedelta(days=7)).isoformat()]
        if recent_logs:
            last_state = recent_logs[-1]['state']
            st.success(f"🏠 Last logged: {last_state}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**❄️ Winter Theme Active**")
with col2:
    st.markdown(f"**🌡️ Mode: {'Night' if st.session_state.dark_mode else 'Day'}**")
with col3:
    st.markdown(f"**📊 Active Tab: {st.session_state.active_tab}**")