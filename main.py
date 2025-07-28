
import streamlit as st
import datetime
import os
import json
import csv
from io import StringIO

# Configure Streamlit for deployment
st.set_page_config(
    page_title="Snowbird AI Financial Assistant", 
    layout="wide",
    page_icon="❄️",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    /* Main app styling */
    .main > div {
        padding: 2rem 1rem;
    }
    
    /* Header styling */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Custom title styling */
    .main-title {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card-like containers */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-card {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Status indicators */
    .status-safe {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-danger {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #eee;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Location detection styling */
    .location-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Quick actions styling */
    .quick-actions {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Try to load OpenAI, handle if not available or no API key
try:
    from openai import OpenAI
    # Load your OpenAI API key from environment variables (Replit Secrets)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key.strip():
        try:
            client = OpenAI(api_key=api_key)
            openai_available = True
        except Exception:
            openai_available = False
            st.warning("OpenAI API key configured but invalid. AI features disabled.")
    else:
        openai_available = False
        st.info("OpenAI API key not found. AI chat features will be disabled.")
except ImportError:
    openai_available = False
    st.info("OpenAI library not available. AI chat features will be disabled.")

# Default values
default_states = {"Arizona": 0, "Minnesota": 0}
default_home_budgets = {
    "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
    "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
}
default_seasonal_cash_flow = {
    "Travel": 300,
    "Healthcare": 400,
    "Supplemental Insurance": 200
}
default_tax_threshold = 183

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
    st.session_state.states = default_states.copy()
if "home_budgets" not in st.session_state:
    st.session_state.home_budgets = default_home_budgets.copy()
if "seasonal_cash_flow" not in st.session_state:
    st.session_state.seasonal_cash_flow = default_seasonal_cash_flow.copy()
if "tax_threshold" not in st.session_state:
    st.session_state.tax_threshold = default_tax_threshold
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

# Streamlit UI with enhanced styling
st.markdown('<h1 class="main-title">❄️ Snowbird AI Financial Assistant 🏖️</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Helping you fly between seasons with your finances in check</p>', unsafe_allow_html=True)

# Settings section
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Tax threshold setting
    st.subheader("Tax Residency Threshold")
    new_threshold = st.number_input("Days to be considered tax resident:", 
                                   min_value=1, max_value=365, 
                                   value=st.session_state.tax_threshold)
    if new_threshold != st.session_state.tax_threshold:
        st.session_state.tax_threshold = new_threshold
    
    # Budget editing
    st.subheader("Edit Home Budgets")
    for state in ["Arizona", "Minnesota"]:
        st.write(f"**{state}**")
        for category in st.session_state.home_budgets[state]:
            new_value = st.number_input(f"{state} - {category} ($):", 
                                       min_value=0, 
                                       value=st.session_state.home_budgets[state][category],
                                       key=f"budget_{state}_{category}")
            st.session_state.home_budgets[state][category] = new_value
    
    # Seasonal cash flow editing
    st.subheader("Edit Seasonal Cash Flow")
    for category in st.session_state.seasonal_cash_flow:
        new_value = st.number_input(f"{category} ($):", 
                                   min_value=0, 
                                   value=st.session_state.seasonal_cash_flow[category],
                                   key=f"seasonal_{category}")
        st.session_state.seasonal_cash_flow[category] = new_value
    
    # Add new categories
    st.subheader("Add New Categories")
    new_seasonal_category = st.text_input("New seasonal expense category:")
    new_seasonal_amount = st.number_input("Amount ($):", min_value=0, key="new_seasonal_amount")
    if st.button("Add Seasonal Category") and new_seasonal_category:
        st.session_state.seasonal_cash_flow[new_seasonal_category] = new_seasonal_amount
        st.success(f"Added {new_seasonal_category}!")
        st.rerun()
    
    # State Management
    st.subheader("Manage Your States")
    current_states = list(st.session_state.states.keys())
    
    # Remove states
    if len(current_states) > 1:
        state_to_remove = st.selectbox("Remove a state:", [""] + current_states)
        if st.button("Remove State") and state_to_remove:
            del st.session_state.states[state_to_remove]
            if state_to_remove in st.session_state.home_budgets:
                del st.session_state.home_budgets[state_to_remove]
            st.success(f"Removed {state_to_remove}!")
            st.rerun()
    
    # Add new states
    all_states = list(state_tax_info.keys())
    available_states = [s for s in all_states if s not in current_states]
    if available_states:
        new_state = st.selectbox("Add a new state:", [""] + available_states)
        if st.button("Add State") and new_state:
            st.session_state.states[new_state] = 0
            st.session_state.home_budgets[new_state] = {"Utilities": 200, "Insurance": 150, "HOA": 100}
            st.success(f"Added {new_state}!")
            st.rerun()

# Location tracking and logging
st.markdown('<h2 class="section-header">📍 Location Tracking & Day Counter</h2>', unsafe_allow_html=True)

# Location detection section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="location-container">', unsafe_allow_html=True)
    st.markdown("### 🌐 Smart Location Detection")
    location_html = """
    <div id="location-info" style="text-align: center;">
        <p style="margin-bottom: 1rem;">Click the button below to detect your current location:</p>
        <button onclick="getLocation()" style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            📍 Detect My Location
        </button>
        <div id="location-result" style="margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.2); border-radius: 8px; min-height: 40px;"></div>
    </div>
    
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
            document.getElementById("location-result").innerHTML = "🔍 Detecting location...";
        } else {
            document.getElementById("location-result").innerHTML = "❌ Geolocation is not supported by this browser.";
        }
    }
    
    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        
        // Simple state detection based on coordinates
        let detectedState = "Unknown";
        if (lat >= 31.0 && lat <= 37.0 && lon >= -114.8 && lon <= -109.0) {
            detectedState = "Arizona";
        } else if (lat >= 43.5 && lat <= 49.4 && lon >= -97.2 && lon <= -89.5) {
            detectedState = "Minnesota";
        }
        
        document.getElementById("location-result").innerHTML = 
            `📍 Location detected: ${detectedState}<br>
             🌍 Coordinates: ${lat.toFixed(4)}, ${lon.toFixed(4)}<br>
             <small>Tip: Use the manual logging below to record your day!</small>`;
    }
    
    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                document.getElementById("location-result").innerHTML = "❌ Location access denied by user.";
                break;
            case error.POSITION_UNAVAILABLE:
                document.getElementById("location-result").innerHTML = "❌ Location information is unavailable.";
                break;
            case error.TIMEOUT:
                document.getElementById("location-result").innerHTML = "❌ Location request timed out.";
                break;
            default:
                document.getElementById("location-result").innerHTML = "❌ An unknown error occurred.";
                break;
        }
    }
    </script>
    """
    st.components.v1.html(location_html, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    st.subheader("📱 Quick Actions")
    today = datetime.date.today()
    st.write(f"📅 Today: {today.strftime('%B %d, %Y')}")
    
    # Show current streak
    if st.session_state.day_log:
        recent_logs = [log for log in st.session_state.day_log if log['date'] >= (today - datetime.timedelta(days=7)).isoformat()]
        if recent_logs:
            last_state = recent_logs[-1]['state']
            consecutive_days = 1
            for i in range(len(recent_logs) - 2, -1, -1):
                if recent_logs[i]['state'] == last_state:
                    consecutive_days += 1
                else:
                    break
            st.markdown(f'<div class="metric-container"><h4>🔥 Current Streak</h4><h2>{consecutive_days} days in {last_state}</h2></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Manual day logging
st.subheader("📝 Manual Day Logging")
state_options = list(st.session_state.states.keys())
location = st.radio("Where are you today?", state_options)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(f"✅ Log Today in {location}"):
        today_str = datetime.date.today().isoformat()
        # Check if today is already logged
        existing_log = next((log for log in st.session_state.day_log if log['date'] == today_str), None)
        if existing_log:
            st.warning(f"Already logged today in {existing_log['state']}!")
        else:
            st.session_state.states[location] += 1
            st.session_state.day_log.append({
                'date': today_str,
                'state': location,
                'method': 'manual',
                'timestamp': datetime.datetime.now().isoformat()
            })
            st.success(f"✅ Logged today in {location}!")
            st.rerun()

with col2:
    if st.button(f"➖ Remove Today") and st.session_state.states[location] > 0:
        today_str = datetime.date.today().isoformat()
        # Remove today's log if it exists
        st.session_state.day_log = [log for log in st.session_state.day_log if log['date'] != today_str]
        st.session_state.states[location] -= 1
        st.success(f"➖ Removed today from {location}!")
        st.rerun()

with col3:
    # Custom date logging
    custom_date = st.date_input("📅 Log custom date:", value=datetime.date.today(), key="custom_date")
    if st.button("📅 Log Custom Date"):
        custom_date_str = custom_date.isoformat()
        existing_log = next((log for log in st.session_state.day_log if log['date'] == custom_date_str), None)
        if existing_log:
            st.warning(f"Date {custom_date} already logged in {existing_log['state']}!")
        else:
            st.session_state.states[location] += 1
            st.session_state.day_log.append({
                'date': custom_date_str,
                'state': location,
                'method': 'custom',
                'timestamp': datetime.datetime.now().isoformat()
            })
            st.success(f"✅ Logged {custom_date} in {location}!")
            st.rerun()

with col4:
    # Bulk day adjustment
    manual_days = st.number_input(f"🔢 Set {location} total days:", 
                                 min_value=0, max_value=365,
                                 value=st.session_state.states[location],
                                 key=f"manual_{location}")
    if st.button("💾 Update Total"):
        st.session_state.states[location] = manual_days
        st.success(f"Updated {location} to {manual_days} days!")

# Smart nudges section
def check_and_show_nudges():
    today = datetime.date.today()
    today_str = today.isoformat()
    
    # Only show nudges once per day
    if st.session_state.last_nudge_date == today_str:
        return
    
    for state, days in st.session_state.states.items():
        threshold = st.session_state.tax_threshold
        
        # Different nudge levels
        if days >= threshold - 7 and days < threshold:
            days_left = threshold - days
            st.warning(f"⚠️ **Gentle Reminder**: You're {days_left} days away from tax residency in {state}! ({days}/{threshold} days)")
            st.session_state.last_nudge_date = today_str
        elif days >= threshold - 3 and days < threshold:
            days_left = threshold - days
            st.error(f"🚨 **Close Call**: Only {days_left} days until tax residency in {state}! ({days}/{threshold} days)")
            st.session_state.last_nudge_date = today_str
        elif days >= threshold:
            st.error(f"🔴 **Tax Alert**: You are now considered a tax resident of {state}! ({days}/{threshold} days)")

check_and_show_nudges()

# Show budgets
st.markdown('<h2 class="section-header">📊 Home Maintenance Budget</h2>', unsafe_allow_html=True)
budget_home = st.selectbox("Select a home to view budget:", list(st.session_state.states.keys()))
budget = st.session_state.home_budgets[budget_home]

st.markdown(f'<div class="metric-card"><h3>🏠 {budget_home} Budget</h3>', unsafe_allow_html=True)

# Display budget with total
total_budget = 0
budget_cols = st.columns(len(budget))
for i, (category, amount) in enumerate(budget.items()):
    with budget_cols[i]:
        st.metric(category, f"${amount}", delta="per month")
    total_budget += amount

st.markdown(f'<h3 style="text-align: center; color: #667eea; margin-top: 1rem;">💰 Total Monthly Budget: ${total_budget}</h3></div>', unsafe_allow_html=True)

# Seasonal cash flow
st.markdown('<h2 class="section-header">💸 Seasonal Cash Flow Plan</h2>', unsafe_allow_html=True)
st.markdown('<div class="metric-card">', unsafe_allow_html=True)

total_seasonal = 0
if st.session_state.seasonal_cash_flow:
    seasonal_cols = st.columns(min(3, len(st.session_state.seasonal_cash_flow)))
    for i, (category, amount) in enumerate(st.session_state.seasonal_cash_flow.items()):
        with seasonal_cols[i % 3]:
            st.metric(category, f"${amount}", delta="per month")
        total_seasonal += amount

st.markdown(f'<h3 style="text-align: center; color: #667eea; margin-top: 1rem;">💰 Total Monthly Seasonal Expenses: ${total_seasonal}</h3></div>', unsafe_allow_html=True)

# Residency tracker
st.markdown('<h2 class="section-header">📅 Tax Residency Tracker</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; font-style: italic; color: #666;">Tax residency threshold: {st.session_state.tax_threshold} days</p>', unsafe_allow_html=True)

# Create visual cards for each state
for state, days in st.session_state.states.items():
    progress = min(days / st.session_state.tax_threshold, 1.0)
    
    # Determine status and color
    if days >= st.session_state.tax_threshold:
        status = "🔴 TAX RESIDENT"
        status_class = "status-danger"
        card_class = "warning-card"
    elif days >= st.session_state.tax_threshold * 0.85:
        status = "⚠️ CRITICAL"
        status_class = "status-warning" 
        card_class = "warning-card"
    elif days >= st.session_state.tax_threshold * 0.7:
        status = "🟡 CAUTION"
        status_class = "status-warning"
        card_class = "info-card"
    else:
        status = "✅ SAFE"
        status_class = "status-safe"
        card_class = "success-card"
    
    st.markdown(f'''
    <div class="{card_class}">
        <h4>🏠 {state}</h4>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.2rem; font-weight: bold;">{days} days</span>
            <span class="{status_class}">{status}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress, text=f"{state}: {days}/{st.session_state.tax_threshold} days ({progress*100:.1f}%)")

# Tax Information
st.header("💰 State Tax Information")
tax_state = st.selectbox("Select a state to view tax info:", list(st.session_state.states.keys()), key="tax_info_selector")
if tax_state in st.session_state.state_tax_info:
    tax_info = st.session_state.state_tax_info[tax_state]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Income Tax Rate", tax_info["income_tax"])
        st.metric("Sales Tax Rate", tax_info["sales_tax"])
    with col2:
        st.metric("Property Tax Rate", tax_info["property_tax"])
        st.metric("Retirement Friendly", tax_info["retirement_friendly"])
    
    # Show comparison if multiple states
    if len(st.session_state.states) > 1:
        st.subheader("State Tax Comparison")
        comparison_data = []
        for state_name in st.session_state.states.keys():
            if state_name in st.session_state.state_tax_info:
                info = st.session_state.state_tax_info[state_name]
                comparison_data.append({
                    "State": state_name,
                    "Income Tax": info["income_tax"],
                    "Sales Tax": info["sales_tax"],
                    "Property Tax": info["property_tax"],
                    "Retirement Friendly": info["retirement_friendly"]
                })
        
        if comparison_data:
            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

# Ask the AI
st.header("🤖 Ask Snowbird AI")
question = st.text_input("Ask a financial question:")
if st.button("Get AI Advice"):
    if not openai_available:
        st.session_state.chat_response = "OpenAI API key not configured. Please add your OPENAI_API_KEY to Replit Secrets."
    elif not question.strip():
        st.session_state.chat_response = "Please enter a question first."
    else:
        try:
            # Include current data in the AI context
            context = f"""
            Current situation:
            - Days in Arizona: {st.session_state.states['Arizona']}
            - Days in Minnesota: {st.session_state.states['Minnesota']}
            - Tax threshold: {st.session_state.tax_threshold} days
            - Arizona monthly budget: ${sum(st.session_state.home_budgets['Arizona'].values())}
            - Minnesota monthly budget: ${sum(st.session_state.home_budgets['Minnesota'].values())}
            - Total seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a friendly AI financial assistant for seasonal residents (snowbirds). Here's their current situation: {context}"},
                    {"role": "user", "content": question}
                ]
            )
            st.session_state.chat_response = response.choices[0].message.content
        except Exception as e:
            st.session_state.chat_response = f"Error: {e}"

if st.session_state.chat_response:
    st.markdown("**AI Response:**")
    st.write(st.session_state.chat_response)

# Day Log and Audit Report
st.header("📋 Day Log & Audit Report")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Recent Activity Log")
    if st.session_state.day_log:
        # Show last 10 entries
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.write(f"📅 {date_obj.strftime('%b %d, %Y')} - {log['state']} ({log['method']})")
    else:
        st.write("No activity logged yet.")
    
    # Export options
    st.subheader("📤 Export Data")
    
    col_csv, col_json = st.columns(2)
    
    with col_csv:
        if st.button("📄 Export as CSV"):
            # Create CSV data
            csv_data = StringIO()
            fieldnames = ['date', 'state', 'method', 'timestamp']
            writer = csv.DictWriter(csv_data, fieldnames=fieldnames)
            writer.writeheader()
            for log in st.session_state.day_log:
                writer.writerow(log)
            
            st.download_button(
                label="💾 Download CSV",
                data=csv_data.getvalue(),
                file_name=f"snowbird_log_{datetime.date.today().isoformat()}.csv",
                mime="text/csv"
            )
    
    with col_json:
        if st.button("📋 Export as JSON"):
            export_data = {
                'export_date': datetime.date.today().isoformat(),
                'day_log': st.session_state.day_log,
                'state_totals': st.session_state.states,
                'tax_threshold': st.session_state.tax_threshold
            }
            
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"snowbird_data_{datetime.date.today().isoformat()}.json",
                mime="application/json"
            )

with col2:
    st.subheader("📈 Audit Report")
    
    # Generate comprehensive audit report
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)
    
    # Calculate days by month for current year
    monthly_breakdown = {}
    for log in st.session_state.day_log:
        log_date = datetime.datetime.fromisoformat(log['date']).date()
        if log_date >= year_start:
            month_key = log_date.strftime('%Y-%m')
            state = log['state']
            if month_key not in monthly_breakdown:
                monthly_breakdown[month_key] = {}
            if state not in monthly_breakdown[month_key]:
                monthly_breakdown[month_key][state] = 0
            monthly_breakdown[month_key][state] += 1
    
    # Risk assessment
    st.write("**🎯 Tax Residency Risk Assessment:**")
    for state, days in st.session_state.states.items():
        threshold = st.session_state.tax_threshold
        risk_percentage = (days / threshold) * 100
        
        if risk_percentage >= 100:
            risk_level = "🔴 HIGH RISK - Tax Resident"
        elif risk_percentage >= 85:
            risk_level = "🟠 CRITICAL - Very Close"
        elif risk_percentage >= 70:
            risk_level = "🟡 CAUTION - Monitor Closely"
        else:
            risk_level = "🟢 LOW RISK - Safe"
        
        st.write(f"**{state}**: {days} days ({risk_percentage:.1f}%) - {risk_level}")
    
    # Monthly breakdown
    if monthly_breakdown:
        st.write("**📅 Monthly Breakdown (Current Year):**")
        for month in sorted(monthly_breakdown.keys()):
            month_name = datetime.datetime.strptime(month, '%Y-%m').strftime('%B %Y')
            st.write(f"**{month_name}:**")
            for state, count in monthly_breakdown[month].items():
                st.write(f"  • {state}: {count} days")
    
    # Recommendations
    st.write("**💡 Recommendations:**")
    for state, days in st.session_state.states.items():
        remaining_days = st.session_state.tax_threshold - days
        if remaining_days > 0:
            days_left_in_year = (datetime.date(today.year, 12, 31) - today).days
            if remaining_days < days_left_in_year:
                st.write(f"• ⚠️ Limit {state} stays to {remaining_days} more days this year")
            else:
                st.write(f"• ✅ You can safely spend {remaining_days} more days in {state}")
        else:
            st.write(f"• 🚨 Already exceeded threshold for {state}")

# Enhanced AI Chat with Context
st.markdown('<h2 class="section-header">🤖 Enhanced Snowbird AI Assistant</h2>', unsafe_allow_html=True)

# Add planning features
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    question = st.text_input("💬 Ask about your travel plans, tax implications, or get smart suggestions:")
    
    # Quick suggestion buttons
    st.markdown("**⚡ Quick Questions:**")
    quick_questions = [
        "How many more days can I safely stay in Arizona?",
        "What's my tax risk assessment?", 
        "Suggest an optimal travel schedule for next month",
        "Compare costs between my residences",
        "When should I plan my next move?"
    ]
    
    # Display quick questions in a more organized way
    for i in range(0, len(quick_questions), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(quick_questions):
                with col:
                    if st.button(quick_questions[i + j], key=f"quick_{i+j}", use_container_width=True):
                        question = quick_questions[i + j]
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div class="info-card">
        <h4>🎯 Smart Features</h4>
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li>🚨 Real-time nudges</li>
            <li>📊 Risk assessments</li>
            <li>🗓️ Travel optimization</li>
            <li>💰 Cost comparisons</li>
            <li>📋 Tax planning advice</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

if st.button("🚀 Get AI Advice"):
    if not openai_available:
        st.session_state.chat_response = "OpenAI API key not configured. Please add your OPENAI_API_KEY to Replit Secrets."
    elif not question.strip():
        st.session_state.chat_response = "Please enter a question first."
    else:
        try:
            # Enhanced context for AI
            context = f"""
            Current Snowbird Situation (as of {datetime.date.today()}):
            
            RESIDENCY STATUS:
            - Tax threshold: {st.session_state.tax_threshold} days
            {chr(10).join([f"- {state}: {days} days ({(days/st.session_state.tax_threshold)*100:.1f}% of threshold)" for state, days in st.session_state.states.items()])}
            
            FINANCIAL OVERVIEW:
            - Total monthly budgets: {', '.join([f"{state}: ${sum(budget.values())}" for state, budget in st.session_state.home_budgets.items()])}
            - Seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
            
            RECENT ACTIVITY:
            {chr(10).join([f"- {log['date']}: {log['state']}" for log in sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:5]])}
            
            Please provide helpful, specific advice considering tax implications, costs, and optimal planning.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert financial and tax planning assistant for snowbirds (seasonal residents). You help optimize travel schedules, minimize tax burdens, and manage multi-residence expenses. Provide specific, actionable advice. Current context: {context}"},
                    {"role": "user", "content": question}
                ]
            )
            st.session_state.chat_response = response.choices[0].message.content
        except Exception as e:
            st.session_state.chat_response = f"Error: {e}"

if st.session_state.chat_response:
    st.markdown('''
    <div class="metric-card" style="border-left: 4px solid #28a745;">
        <h4>🤖 AI Response:</h4>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(st.session_state.chat_response)

# Reset option
st.header("🔄 Reset Data")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset Day Counters Only", type="secondary"):
        st.session_state.states = default_states.copy()
        st.session_state.day_log = []
        st.success("Day counters and log reset!")
        st.rerun()

with col2:
    if st.button("🗑️ Reset All Data to Defaults", type="secondary"):
        st.session_state.states = default_states.copy()
        st.session_state.home_budgets = default_home_budgets.copy()
        st.session_state.seasonal_cash_flow = default_seasonal_cash_flow.copy()
        st.session_state.tax_threshold = default_tax_threshold
        st.session_state.chat_response = ""
        st.session_state.day_log = []
        st.success("All data reset to defaults!")
        st.rerun()
