
import streamlit as st
import datetime
import os
import json
import csv
from io import StringIO
import pandas as pd

# Configure Streamlit for deployment with winter theme
st.set_page_config(
    page_title="Snowbird: Your Seasonal Financial Assistant", 
    layout="wide",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)

# Winter-themed CSS with Lucide icons
st.markdown("""
<style>
    /* Import Google Fonts and Lucide Icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.js');

    /* Root variables for winter theme */
    :root {
        --primary-blue: #12BDF2;
        --light-blue: #E3F4FD;
        --ice-white: #FFFFFF;
        --snow-gray: #F8FAFC;
        --text-dark: #1E293B;
        --text-light: #64748B;
        --border-light: #E2E8F0;
        --shadow: rgba(18, 189, 242, 0.1);
    }

    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--ice-white) 0%, var(--light-blue) 100%);
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 400;
        letter-spacing: -0.01em;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: var(--ice-white);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px var(--shadow);
        border: 1px solid var(--border-light);
    }

    .main-title {
        color: var(--primary-blue);
        font-size: clamp(1.5rem, 3vw, 2.2rem);
        font-weight: 600;
        margin-bottom: 0.3rem;
        text-shadow: none;
        letter-spacing: -0.02em;
    }

    .subtitle {
        color: var(--text-light);
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: -0.01em;
    }

    /* Icon styling */
    .icon {
        width: 16px;
        height: 16px;
        display: inline-block;
        margin-right: 8px;
        vertical-align: middle;
    }

    .icon-large {
        width: 24px;
        height: 24px;
        margin-right: 12px;
    }

    /* Card styling */
    .winter-card {
        background: var(--ice-white);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px var(--shadow);
        border: 1px solid var(--border-light);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .winter-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--shadow);
    }

    .winter-card h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 1rem !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #0EA5E9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(18, 189, 242, 0.3) !important;
    }

    /* Metric styling */
    .metric-card {
        background: var(--ice-white);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 2px 10px var(--shadow);
        margin: 0.5rem 0;
    }

    /* Status indicators */
    .status-safe { color: #10B981; font-weight: 600; }
    .status-warning { color: #F59E0B; font-weight: 600; }
    .status-danger { color: #EF4444; font-weight: 600; }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, #0EA5E9 100%) !important;
    }

    /* Sidebar styling */
    .stSidebar > div {
        background: var(--ice-white) !important;
        border-right: 2px solid var(--border-light) !important;
    }

    /* Global text styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: var(--text-dark) !important;
    }

    p, div, span, label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 400 !important;
        letter-spacing: -0.005em !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--snow-gray);
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-dark);
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: -0.01em !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-blue) !important;
        color: white !important;
    }

    /* Streamlit specific overrides */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }

    .stMetric label {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }

    .stMetric [data-testid="metric-value"] {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header { padding: 1rem; }
        .main-title { font-size: 1.4rem !important; }
        .winter-card { padding: 1rem; margin: 0.5rem 0; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
    }

    /* Alert styling */
    .alert-success {
        background: #D1FAE5;
        border: 1px solid #34D399;
        color: #065F46;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .alert-warning {
        background: #FEF3C7;
        border: 1px solid #FBBF24;
        color: #92400E;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .alert-danger {
        background: #FEE2E2;
        border: 1px solid #F87171;
        color: #991B1B;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>

<!-- Lucide Icons Script -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        lucide.createIcons();
    });
</script>
""", unsafe_allow_html=True)

# Try to load OpenAI, handle if not available or no API key
try:
    from openai import OpenAI
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
        st.info("To enable AI features, add your OPENAI_API_KEY to Replit Secrets.")
except ImportError:
    openai_available = False
    st.info("OpenAI library not available. AI chat features will be disabled.")

# Try to load Gmail API components
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import base64
    import email
    import re
    gmail_available = True
except ImportError:
    gmail_available = False
    st.info("Gmail API libraries not available. Gmail features will be disabled.")

# Gmail API setup
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    
    # Check if we have stored credentials
    if 'gmail_creds' in st.session_state:
        creds = st.session_state.gmail_creds
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                st.error(f"Failed to refresh credentials: {e}")
                return None
        else:
            # For production, you'd need to set up OAuth credentials
            st.warning("Gmail integration requires OAuth setup. Please contact support for setup instructions.")
            return None
    
    st.session_state.gmail_creds = creds
    return creds

def search_bills_in_gmail(service, query="bill OR invoice OR payment due", max_results=50):
    """Search for bills and invoices in Gmail"""
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        bills_found = []
        
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            # Extract email content
            bill_info = extract_bill_info(msg)
            if bill_info:
                bills_found.append(bill_info)
        
        return bills_found
    except Exception as e:
        st.error(f"Error searching Gmail: {e}")
        return []

def extract_bill_info(message):
    """Extract bill information from email message"""
    try:
        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Get email body
        body = get_email_body(message['payload'])
        
        # Extract amount using regex
        amount_patterns = [
            r'\$(\d+[,.]?\d*)',
            r'(\d+[,.]?\d*)\s*USD',
            r'Amount.*?\$(\d+[,.]?\d*)',
            r'Total.*?\$(\d+[,.]?\d*)'
        ]
        
        amount = None
        for pattern in amount_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(',', '')
                break
        
        # Extract due date
        due_date_patterns = [
            r'due\s+(?:on\s+)?(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'payment\s+due\s+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'due\s+date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        ]
        
        due_date = None
        for pattern in due_date_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                due_date = match.group(1)
                break
        
        # Determine bill category based on sender
        category = categorize_bill(sender, subject)
        
        if amount or due_date:
            return {
                'subject': subject,
                'sender': sender,
                'amount': float(amount) if amount else 0,
                'due_date': due_date,
                'category': category,
                'email_date': date,
                'message_id': message['id']
            }
        
        return None
    except Exception as e:
        return None

def get_email_body(payload):
    """Extract text body from email payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        if payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    
    return body

def categorize_bill(sender, subject):
    """Categorize bill based on sender and subject"""
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    if any(word in sender_lower for word in ['electric', 'power', 'energy', 'utility']):
        return 'Utilities'
    elif any(word in sender_lower for word in ['water', 'sewer']):
        return 'Utilities'
    elif any(word in sender_lower for word in ['gas', 'propane']):
        return 'Utilities'
    elif any(word in sender_lower for word in ['insurance', 'allstate', 'geico', 'progressive']):
        return 'Insurance'
    elif any(word in sender_lower for word in ['hoa', 'association', 'community']):
        return 'HOA'
    elif any(word in sender_lower for word in ['mortgage', 'loan', 'bank']):
        return 'Mortgage'
    elif any(word in sender_lower for word in ['credit', 'visa', 'mastercard', 'amex']):
        return 'Credit Card'
    else:
        return 'Other'

def search_travel_confirmations(service):
    """Search for travel confirmations in Gmail"""
    try:
        travel_queries = [
            'flight confirmation',
            'booking confirmation',
            'itinerary',
            'travel confirmation',
            'airline',
            'hotel reservation'
        ]
        
        travel_info = []
        
        for query in travel_queries:
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=20
            ).execute()
            
            messages = results.get('messages', [])
            
            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                travel_data = extract_travel_info(msg)
                if travel_data:
                    travel_info.append(travel_data)
        
        return travel_info
    except Exception as e:
        st.error(f"Error searching travel confirmations: {e}")
        return []

def extract_travel_info(message):
    """Extract travel information from email"""
    try:
        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        
        body = get_email_body(message['payload'])
        
        # Extract travel dates
        date_patterns = [
            r'(?:departure|depart|leaving)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(?:arrival|arrive|arriving)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            dates.extend(matches)
        
        # Extract destinations
        destination_patterns = [
            r'(?:to|destination)\s*:?\s*([A-Z]{3})',  # Airport codes
            r'(?:to|destination)\s*:?\s*([A-Za-z\s]+?)(?:\n|,)',
        ]
        
        destinations = []
        for pattern in destination_patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            destinations.extend(matches)
        
        if dates or destinations:
            return {
                'subject': subject,
                'sender': sender,
                'dates': dates,
                'destinations': destinations,
                'type': 'travel',
                'message_id': message['id']
            }
        
        return None
    except Exception as e:
        return None

# Default data
default_states = {"Arizona": 0, "Minnesota": 0}
default_home_budgets = {
    "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100, "Maintenance": 75},
    "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90, "Maintenance": 100}
}
default_seasonal_cash_flow = {
    "Travel": 500,
    "Healthcare": 400,
    "Supplemental Insurance": 200,
    "Emergency Fund": 300
}
default_bills = {
    "Arizona": [
        {"name": "Electric", "amount": 150, "due_date": "15", "frequency": "monthly"},
        {"name": "Water", "amount": 80, "due_date": "1", "frequency": "monthly"},
        {"name": "HOA", "amount": 100, "due_date": "1", "frequency": "monthly"}
    ],
    "Minnesota": [
        {"name": "Gas", "amount": 120, "due_date": "10", "frequency": "monthly"},
        {"name": "Electric", "amount": 95, "due_date": "20", "frequency": "monthly"},
        {"name": "Property Tax", "amount": 400, "due_date": "15", "frequency": "quarterly"}
    ]
}
default_migration_checklist = [
    {"task": "Adjust thermostat", "category": "HVAC", "completed": False},
    {"task": "Empty refrigerator", "category": "Kitchen", "completed": False},
    {"task": "Forward mail", "category": "Mail", "completed": False},
    {"task": "Turn off water main", "category": "Utilities", "completed": False},
    {"task": "Set up security system", "category": "Security", "completed": False},
    {"task": "Arrange lawn service", "category": "Exterior", "completed": False},
    {"task": "Clean out gutters", "category": "Exterior", "completed": False},
    {"task": "Pack seasonal clothes", "category": "Personal", "completed": False}
]

# Session state initialization
if "states" not in st.session_state:
    st.session_state.states = default_states.copy()
if "home_budgets" not in st.session_state:
    st.session_state.home_budgets = default_home_budgets.copy()
if "seasonal_cash_flow" not in st.session_state:
    st.session_state.seasonal_cash_flow = default_seasonal_cash_flow.copy()
if "bills" not in st.session_state:
    st.session_state.bills = default_bills.copy()
if "migration_checklist" not in st.session_state:
    st.session_state.migration_checklist = default_migration_checklist.copy()
if "day_log" not in st.session_state:
    st.session_state.day_log = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "tax_threshold" not in st.session_state:
    st.session_state.tax_threshold = 183

# Helper functions
def get_tax_status(days, threshold):
    """Get tax residency status for a state"""
    percentage = (days / threshold) * 100
    if days >= threshold:
        return "TAX RESIDENT", "status-danger"
    elif days >= threshold * 0.9:
        return "CRITICAL", "status-warning"
    elif days >= threshold * 0.75:
        return "CAUTION", "status-warning"
    else:
        return "SAFE", "status-safe"

def add_day_log(state, date_str=None):
    """Add a day to the log"""
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    # Check if already logged
    existing = next((log for log in st.session_state.day_log if log['date'] == date_str), None)
    if existing:
        return False, f"Already logged {date_str} in {existing['state']}"

    st.session_state.day_log.append({
        'date': date_str,
        'state': state,
        'timestamp': datetime.datetime.now().isoformat()
    })
    st.session_state.states[state] += 1
    return True, f"Logged {date_str} in {state}"

def generate_report_data():
    """Generate comprehensive report data"""
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)

    # Filter logs for current year
    current_year_logs = [
        log for log in st.session_state.day_log 
        if datetime.datetime.fromisoformat(log['date']).date() >= year_start
    ]

    # Monthly breakdown
    monthly_data = {}
    for log in current_year_logs:
        month = datetime.datetime.fromisoformat(log['date']).strftime('%Y-%m')
        if month not in monthly_data:
            monthly_data[month] = {}
        state = log['state']
        monthly_data[month][state] = monthly_data[month].get(state, 0) + 1

    return {
        'year': today.year,
        'total_days': st.session_state.states,
        'monthly_breakdown': monthly_data,
        'threshold': st.session_state.tax_threshold,
        'generated_date': today.isoformat()
    }

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">
        <i data-lucide="home" class="icon-large"></i>
        Snowbird: Your Seasonal Financial Assistant
    </h1>
    <p class="subtitle">Manage your multi-state lifestyle with confidence</p>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Dashboard", 
    "Day Tracker", 
    "Budgets", 
    "AI Assistant", 
    "Reports", 
    "Migration Checklist",
    "Bill Tracker",
    "Gmail Integration"
])

# Tab 1: Dashboard
with tab1:
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="bar-chart-3" class="icon"></i>Current Status Overview</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        total_days = sum(st.session_state.states.values())
        st.metric("Total Days Logged", total_days)

    with col2:
        days_left = (365 - total_days) if total_days < 365 else 0
        st.metric("Days Remaining in Year", days_left)

    with col3:
        threshold = st.session_state.tax_threshold
        closest_to_threshold = max(st.session_state.states.values())
        risk_level = "High" if closest_to_threshold >= threshold * 0.9 else "Medium" if closest_to_threshold >= threshold * 0.75 else "Low"
        st.metric("Tax Risk Level", risk_level)

    st.markdown('</div>', unsafe_allow_html=True)

    # State residency status
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="map-pin" class="icon"></i>State Residency Status</h3>', unsafe_allow_html=True)

    for state, days in st.session_state.states.items():
        status_text, status_class = get_tax_status(days, st.session_state.tax_threshold)
        progress = min(days / st.session_state.tax_threshold, 1.0)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{state}**")
            st.progress(progress, text=f"{days}/{st.session_state.tax_threshold} days ({progress*100:.1f}%)")
        with col2:
            st.metric("Days", days)
        with col3:
            st.markdown(f'<span class="{status_class}"><i data-lucide="alert-circle" class="icon"></i>{status_text}</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Quick financial overview
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="dollar-sign" class="icon"></i>Financial Overview</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('**<i data-lucide="home" class="icon"></i>Monthly Home Budgets**', unsafe_allow_html=True)
        for state, budget in st.session_state.home_budgets.items():
            total_budget = sum(budget.values())
            st.write(f"• {state}: ${total_budget:,}")

    with col2:
        st.markdown('**<i data-lucide="calendar" class="icon"></i>Seasonal Expenses**', unsafe_allow_html=True)
        total_seasonal = sum(st.session_state.seasonal_cash_flow.values())
        st.write(f"• Total Monthly: ${total_seasonal:,}")
        for category, amount in st.session_state.seasonal_cash_flow.items():
            st.write(f"  - {category}: ${amount}")

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Day Tracker
with tab2:
    st.markdown('<h2><i data-lucide="calendar-days" class="icon"></i>Residency Day Tracker</h2>', unsafe_allow_html=True)

    # Current location logging
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="map-pin" class="icon"></i>Log Your Current Location**', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        current_location = st.selectbox("Where are you today?", list(st.session_state.states.keys()))
        custom_date = st.date_input("Select date:", value=datetime.date.today())

    with col2:
        if st.button("Log Day", type="primary"):
            success, message = add_day_log(current_location, custom_date.isoformat())
            if success:
                st.success(message)
                st.rerun()
            else:
                st.warning(message)

    st.markdown('</div>', unsafe_allow_html=True)

    # Recent activity
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="activity" class="icon"></i>Recent Activity**', unsafe_allow_html=True)

    if st.session_state.day_log:
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.markdown(f'<i data-lucide="calendar" class="icon"></i>{date_obj.strftime("%b %d, %Y")} - **{log["state"]}**', unsafe_allow_html=True)
    else:
        st.write("No activity logged yet. Start by logging your current location!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Bulk operations
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="settings" class="icon"></i>Bulk Operations**', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        bulk_state = st.selectbox("State for bulk operation:", list(st.session_state.states.keys()), key="bulk_state")
        bulk_days = st.number_input("Set total days:", min_value=0, max_value=365, value=st.session_state.states[bulk_state])

        if st.button("Update Total Days"):
            st.session_state.states[bulk_state] = bulk_days
            st.success(f"Updated {bulk_state} to {bulk_days} days")
            st.rerun()

    with col2:
        if st.button("Clear All Logs", type="secondary"):
            st.session_state.day_log = []
            st.session_state.states = {state: 0 for state in st.session_state.states.keys()}
            st.success("All logs cleared!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Budgets
with tab3:
    st.markdown('<h2><i data-lucide="wallet" class="icon"></i>Budget Management</h2>', unsafe_allow_html=True)

    # Home budgets
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="home" class="icon"></i>Home Budgets**', unsafe_allow_html=True)

    budget_state = st.selectbox("Select home to edit:", list(st.session_state.home_budgets.keys()))

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{budget_state} Budget Categories**")
        budget = st.session_state.home_budgets[budget_state]
        total_budget = 0

        for category in list(budget.keys()):
            new_amount = st.number_input(f"{category} ($):", 
                                       min_value=0, 
                                       value=budget[category],
                                       key=f"budget_{budget_state}_{category}")
            budget[category] = new_amount
            total_budget += new_amount

        # Add new budget category
        new_category = st.text_input("Add new category:")
        new_amount = st.number_input("Amount ($):", min_value=0, key=f"new_budget_{budget_state}")

        if st.button("Add Category") and new_category:
            budget[new_category] = new_amount
            st.success(f"Added {new_category} to {budget_state} budget!")
            st.rerun()

    with col2:
        st.metric(f"{budget_state} Total Monthly Budget", f"${total_budget:,}")

        # Budget breakdown chart
        if budget:
            chart_data = pd.DataFrame([
                {"Category": category, "Amount": amount} 
                for category, amount in budget.items()
            ])
            st.bar_chart(chart_data.set_index("Category"))

    st.markdown('</div>', unsafe_allow_html=True)

    # Seasonal cash flow
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="trending-up" class="icon"></i>Seasonal Cash Flow Planning**', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        seasonal_total = 0
        for category in list(st.session_state.seasonal_cash_flow.keys()):
            new_amount = st.number_input(f"{category} ($):", 
                                       min_value=0, 
                                       value=st.session_state.seasonal_cash_flow[category],
                                       key=f"seasonal_{category}")
            st.session_state.seasonal_cash_flow[category] = new_amount
            seasonal_total += new_amount

        # Add new seasonal category
        new_seasonal = st.text_input("Add new seasonal expense:")
        new_seasonal_amount = st.number_input("Amount ($):", min_value=0, key="new_seasonal")

        if st.button("Add Seasonal Category") and new_seasonal:
            st.session_state.seasonal_cash_flow[new_seasonal] = new_seasonal_amount
            st.success(f"Added {new_seasonal}!")
            st.rerun()

    with col2:
        st.metric("Total Monthly Seasonal Expenses", f"${seasonal_total:,}")

        # Annual projection
        annual_total = seasonal_total * 12
        st.metric("Annual Projection", f"${annual_total:,}")

        # Seasonal breakdown chart
        if st.session_state.seasonal_cash_flow:
            seasonal_chart = pd.DataFrame([
                {"Category": category, "Amount": amount} 
                for category, amount in st.session_state.seasonal_cash_flow.items()
            ])
            st.bar_chart(seasonal_chart.set_index("Category"))

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: AI Assistant
with tab4:
    st.markdown('<h2><i data-lucide="bot" class="icon"></i>AI Financial Assistant</h2>', unsafe_allow_html=True)

    if not openai_available:
        st.warning("AI features require an OpenAI API key. Add your OPENAI_API_KEY to Replit Secrets to enable this feature.")

        # Show example functionality
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="lightbulb" class="icon"></i>Example AI Features (when enabled):**', unsafe_allow_html=True)
        st.write("• Ask about tax residency implications")
        st.write("• Get budget optimization suggestions")
        st.write("• Receive travel timing recommendations")
        st.write("• Query state tax information")
        st.write("• Get migration planning advice")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # AI Chat interface
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)

        # Quick questions
        st.markdown('**<i data-lucide="help-circle" class="icon"></i>Quick Questions:**', unsafe_allow_html=True)
        quick_questions = [
            "How many more days can I safely stay in Arizona this year?",
            "What are the tax implications of my current residency status?",
            "How can I optimize my budget between both homes?",
            "When should I plan my next move to minimize tax risk?",
            "What financial preparations should I make before traveling?"
        ]

        question_cols = st.columns(2)
        for i, question in enumerate(quick_questions):
            with question_cols[i % 2]:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    st.session_state.current_question = question

        # Custom question input
        custom_question = st.text_area("Or ask your own question:", 
                                     value=getattr(st.session_state, 'current_question', ''),
                                     height=100)

        if st.button("Ask AI", type="primary") and custom_question:
            with st.spinner("Thinking..."):
                try:
                    # Prepare context
                    context = f"""
                    Current Snowbird Status:
                    - States: {', '.join([f"{state}: {days} days" for state, days in st.session_state.states.items()])}
                    - Tax threshold: {st.session_state.tax_threshold} days
                    - Total budgets: {', '.join([f"{state}: ${sum(budget.values())}" for state, budget in st.session_state.home_budgets.items()])}
                    - Seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
                    - Today's date: {datetime.date.today()}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"You are an expert financial advisor for snowbirds (seasonal residents). Provide specific, actionable advice considering tax residency rules, multi-state budgeting, and seasonal migration planning. Context: {context}"},
                            {"role": "user", "content": custom_question}
                        ],
                        temperature=0.7
                    )

                    ai_response = response.choices[0].message.content

                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": custom_question,
                        "response": ai_response,
                        "timestamp": datetime.datetime.now().isoformat()
                    })

                    st.success("Response generated!")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

        # Display chat history
        if st.session_state.chat_history:
            st.markdown('<div class="winter-card">', unsafe_allow_html=True)
            st.markdown('**<i data-lucide="message-circle" class="icon"></i>Recent AI Conversations:**', unsafe_allow_html=True)

            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.expander(f"{chat['question'][:60]}..."):
                    st.write("**Question:**", chat['question'])
                    st.write("**AI Response:**", chat['response'])
                    st.caption(f"Asked on {datetime.datetime.fromisoformat(chat['timestamp']).strftime('%B %d, %Y at %I:%M %p')}")

            st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Reports
with tab5:
    st.markdown('<h2><i data-lucide="file-text" class="icon"></i>Tax Residency Reports</h2>', unsafe_allow_html=True)

    # Generate report
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="clipboard" class="icon"></i>Tax Residency Summary Report**', unsafe_allow_html=True)

    report_data = generate_report_data()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('**<i data-lucide="calendar-check" class="icon"></i>Current Year Status:**', unsafe_allow_html=True)
        for state, days in report_data['total_days'].items():
            status_text, status_class = get_tax_status(days, report_data['threshold'])
            st.write(f"• **{state}**: {days} days - {status_text}")

        st.write(f"**Tax Threshold**: {report_data['threshold']} days")
        st.write(f"**Report Generated**: {report_data['generated_date']}")

    with col2:
        # Monthly breakdown
        if report_data['monthly_breakdown']:
            st.markdown('**<i data-lucide="bar-chart" class="icon"></i>Monthly Breakdown:**', unsafe_allow_html=True)
            monthly_df_data = []
            for month, states in report_data['monthly_breakdown'].items():
                month_name = datetime.datetime.strptime(month, '%Y-%m').strftime('%b %Y')
                for state, count in states.items():
                    monthly_df_data.append({
                        "Month": month_name,
                        "State": state,
                        "Days": count
                    })

            if monthly_df_data:
                monthly_df = pd.DataFrame(monthly_df_data)
                st.dataframe(monthly_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Export options
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="download" class="icon"></i>Export Options**', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # CSV Export
        if st.button("Export as CSV"):
            # Prepare CSV data
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)

            # Write header
            csv_writer.writerow(['Date', 'State', 'Days_in_State', 'Tax_Status'])

            # Write data
            for log in sorted(st.session_state.day_log, key=lambda x: x['date']):
                date_str = log['date']
                state = log['state']
                current_days = len([l for l in st.session_state.day_log if l['state'] == state and l['date'] <= date_str])
                status, _ = get_tax_status(current_days, st.session_state.tax_threshold)
                csv_writer.writerow([date_str, state, current_days, status])

            st.download_button(
                label="Download CSV Report",
                data=csv_buffer.getvalue(),
                file_name=f"snowbird_tax_report_{datetime.date.today().isoformat()}.csv",
                mime="text/csv"
            )

    with col2:
        # JSON Export
        if st.button("Export as JSON"):
            json_data = {
                "report_metadata": {
                    "generated_date": datetime.date.today().isoformat(),
                    "tax_threshold": st.session_state.tax_threshold,
                    "report_type": "snowbird_tax_residency"
                },
                "state_summary": report_data['total_days'],
                "monthly_breakdown": report_data['monthly_breakdown'],
                "detailed_log": st.session_state.day_log,
                "budgets": st.session_state.home_budgets,
                "seasonal_expenses": st.session_state.seasonal_cash_flow
            }

            st.download_button(
                label="Download JSON Report",
                data=json.dumps(json_data, indent=2),
                file_name=f"snowbird_complete_report_{datetime.date.today().isoformat()}.json",
                mime="application/json"
            )

    with col3:
        # TODO: PDF Export
        st.button("Export as PDF", disabled=True, help="PDF export coming soon!")

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Migration Checklist
with tab6:
    st.markdown('<h2><i data-lucide="list-checks" class="icon"></i>Seasonal Migration Checklist</h2>', unsafe_allow_html=True)

    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="clipboard-list" class="icon"></i>Pre-Travel Checklist**', unsafe_allow_html=True)
    st.caption("Complete these tasks before leaving for your seasonal home")

    # Organize checklist by category
    categories = {}
    for item in st.session_state.migration_checklist:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    # Display checklist by category
    for category, items in categories.items():
        st.write(f"**{category}**")

        for i, item in enumerate(items):
            # Find the item in the main list to update it
            main_index = next(j for j, main_item in enumerate(st.session_state.migration_checklist) 
                            if main_item['task'] == item['task'])

            col1, col2 = st.columns([3, 1])

            with col1:
                completed = st.checkbox(
                    item['task'], 
                    value=item['completed'],
                    key=f"checklist_{main_index}"
                )
                st.session_state.migration_checklist[main_index]['completed'] = completed

            with col2:
                if st.button("Delete", key=f"delete_{main_index}", help="Delete this item"):
                    st.session_state.migration_checklist.pop(main_index)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new checklist item
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="plus" class="icon"></i>Add New Checklist Item**', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        new_task = st.text_input("Task description:")

    with col2:
        new_category = st.selectbox("Category:", 
                                  ["HVAC", "Kitchen", "Mail", "Utilities", "Security", "Exterior", "Personal", "Other"])

    with col3:
        if st.button("Add Task") and new_task:
            st.session_state.migration_checklist.append({
                "task": new_task,
                "category": new_category,
                "completed": False
            })
            st.success(f"Added: {new_task}")
            st.rerun()

    # Progress summary
    completed_count = sum(1 for item in st.session_state.migration_checklist if item['completed'])
    total_count = len(st.session_state.migration_checklist)
    progress = completed_count / total_count if total_count > 0 else 0

    st.progress(progress, text=f"Checklist Progress: {completed_count}/{total_count} completed ({progress*100:.1f}%)")

    if progress == 1.0 and total_count > 0:
        st.balloons()
        st.success("Congratulations! All checklist items completed. Have a safe trip!")

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 7: Bill Tracker
with tab7:
    st.markdown('<h2><i data-lucide="credit-card" class="icon"></i>Bill Reminder System</h2>', unsafe_allow_html=True)

    # Select state for bill management
    bill_state = st.selectbox("Select home for bill management:", list(st.session_state.bills.keys()))

    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown(f'**<i data-lucide="receipt" class="icon"></i>{bill_state} Bills**', unsafe_allow_html=True)

    # Display current bills
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    for i, bill in enumerate(st.session_state.bills[bill_state]):
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

        with col1:
            st.write(f"**{bill['name']}**")

        with col2:
            st.write(f"${bill['amount']}")

        with col3:
            due_day = int(bill['due_date'])
            due_date = datetime.date(current_year, current_month, due_day)

            # Check if overdue
            today = datetime.date.today()
            if today > due_date:
                st.markdown('<span class="status-danger"><i data-lucide="alert-triangle" class="icon"></i>OVERDUE</span>', unsafe_allow_html=True)
            elif (due_date - today).days <= 3:
                st.markdown('<span class="status-warning"><i data-lucide="clock" class="icon"></i>DUE SOON</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-safe"><i data-lucide="check-circle" class="icon"></i>CURRENT</span>', unsafe_allow_html=True)

        with col4:
            st.write(f"Due: {bill['due_date']}")

        with col5:
            if st.button("Delete", key=f"delete_bill_{bill_state}_{i}", help="Delete bill"):
                st.session_state.bills[bill_state].pop(i)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new bill
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="plus-circle" class="icon"></i>Add New Bill**', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        new_bill_name = st.text_input("Bill name:")

    with col2:
        new_bill_amount = st.number_input("Amount ($):", min_value=0, step=1)

    with col3:
        new_bill_due = st.selectbox("Due date (day of month):", list(range(1, 32)))

    with col4:
        new_bill_freq = st.selectbox("Frequency:", ["monthly", "quarterly", "annually"])

    if st.button("Add Bill") and new_bill_name:
        st.session_state.bills[bill_state].append({
            "name": new_bill_name,
            "amount": new_bill_amount,
            "due_date": str(new_bill_due),
            "frequency": new_bill_freq
        })
        st.success(f"Added {new_bill_name} to {bill_state} bills!")
        st.rerun()

    # Upcoming bills summary
    st.markdown('**<i data-lucide="calendar-clock" class="icon"></i>Upcoming Bills (Next 7 Days)**', unsafe_allow_html=True)
    upcoming_bills = []
    today = datetime.date.today()

    for state, bills in st.session_state.bills.items():
        for bill in bills:
            due_day = int(bill['due_date'])
            try:
                due_date = datetime.date(current_year, current_month, due_day)
                days_until_due = (due_date - today).days

                if -3 <= days_until_due <= 7:  # Include overdue up to 3 days
                    upcoming_bills.append({
                        "state": state,
                        "name": bill['name'],
                        "amount": bill['amount'],
                        "due_date": due_date,
                        "days_until_due": days_until_due
                    })
            except ValueError:
                # Handle invalid dates (e.g., Feb 30)
                continue

    if upcoming_bills:
        upcoming_bills.sort(key=lambda x: x['days_until_due'])
        for bill in upcoming_bills:
            if bill['days_until_due'] < 0:
                st.error(f"OVERDUE: {bill['state']} - {bill['name']} (${bill['amount']}) - Due {abs(bill['days_until_due'])} days ago")
            elif bill['days_until_due'] <= 3:
                st.warning(f"DUE SOON: {bill['state']} - {bill['name']} (${bill['amount']}) - Due in {bill['days_until_due']} days")
            else:
                st.info(f"UPCOMING: {bill['state']} - {bill['name']} (${bill['amount']}) - Due in {bill['days_until_due']} days")
    else:
        st.success("No bills due in the next 7 days!")

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 8: Gmail Integration
with tab8:
    st.markdown('<h2><i data-lucide="mail" class="icon"></i>Gmail Integration</h2>', unsafe_allow_html=True)

    if not gmail_available:
        st.warning("Gmail integration requires additional libraries. Install google-api-python-client and related packages.")
        
        # Show setup instructions
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="settings" class="icon"></i>Setup Instructions:**', unsafe_allow_html=True)
        st.write("1. Install required packages (already added to requirements.txt)")
        st.write("2. Set up Google Cloud Project and enable Gmail API")
        st.write("3. Create OAuth 2.0 credentials")
        st.write("4. Add credentials to Replit Secrets")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show demo of what the features would do
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="eye" class="icon"></i>Available Features (when enabled):**', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('**<i data-lucide="receipt" class="icon"></i>Bill Detection:**', unsafe_allow_html=True)
            st.write("• Auto-scan emails for utility bills")
            st.write("• Extract due dates and amounts")
            st.write("• Categorize by bill type")
            st.write("• Add to bill tracker automatically")
            
        with col2:
            st.markdown('**<i data-lucide="plane" class="icon"></i>Travel Tracking:**', unsafe_allow_html=True)
            st.write("• Find flight confirmations")
            st.write("• Extract travel dates")
            st.write("• Track destination changes")
            st.write("• Auto-log location changes")
        
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Gmail authentication section
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.markdown('**<i data-lucide="key" class="icon"></i>Gmail Connection**', unsafe_allow_html=True)
        
        if 'gmail_authenticated' not in st.session_state:
            st.session_state.gmail_authenticated = False
        
        if not st.session_state.gmail_authenticated:
            if st.button("Connect to Gmail", type="primary"):
                creds = authenticate_gmail()
                if creds:
                    st.session_state.gmail_authenticated = True
                    st.success("Successfully connected to Gmail!")
                    st.rerun()
                else:
                    st.error("Failed to connect to Gmail. Please check your credentials.")
        else:
            st.success("Connected to Gmail!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Your Gmail account is connected and ready to scan for bills and travel confirmations.")
            with col2:
                if st.button("Disconnect"):
                    st.session_state.gmail_authenticated = False
                    if 'gmail_creds' in st.session_state:
                        del st.session_state.gmail_creds
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Bill scanning section
        if st.session_state.gmail_authenticated:
            st.markdown('<div class="winter-card">', unsafe_allow_html=True)
            st.markdown('**<i data-lucide="search" class="icon"></i>Scan for Bills**', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                search_query = st.text_input(
                    "Custom search query:",
                    value="bill OR invoice OR payment due",
                    help="Modify the search terms to find specific bills"
                )
                
                max_emails = st.number_input("Max emails to scan:", min_value=10, max_value=200, value=50)
            
            with col2:
                if st.button("Scan Bills", type="primary"):
                    with st.spinner("Scanning your Gmail for bills..."):
                        try:
                            creds = st.session_state.gmail_creds
                            service = build('gmail', 'v1', credentials=creds)
                            
                            bills = search_bills_in_gmail(service, search_query, max_emails)
                            
                            if bills:
                                st.success(f"Found {len(bills)} potential bills!")
                                st.session_state.scanned_bills = bills
                            else:
                                st.info("No bills found with current search criteria.")
                        except Exception as e:
                            st.error(f"Error scanning emails: {e}")
            
            # Display scanned bills
            if 'scanned_bills' in st.session_state and st.session_state.scanned_bills:
                st.markdown('**<i data-lucide="list" class="icon"></i>Found Bills:**', unsafe_allow_html=True)
                
                for i, bill in enumerate(st.session_state.scanned_bills):
                    with st.expander(f"{bill['sender']} - ${bill['amount']} ({bill['category']})"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Subject:** {bill['subject']}")
                            st.write(f"**Amount:** ${bill['amount']}")
                            st.write(f"**Category:** {bill['category']}")
                        
                        with col2:
                            st.write(f"**Due Date:** {bill['due_date'] or 'Not found'}")
                            st.write(f"**Sender:** {bill['sender']}")
                        
                        with col3:
                            # Option to add to bill tracker
                            bill_state = st.selectbox(
                                "Add to state:",
                                list(st.session_state.bills.keys()),
                                key=f"bill_state_{i}"
                            )
                            
                            if st.button(f"Add to {bill_state}", key=f"add_bill_{i}"):
                                # Extract day from due date if available
                                due_day = "15"  # Default
                                if bill['due_date']:
                                    try:
                                        # Try to extract day from various date formats
                                        import datetime as dt
                                        for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y']:
                                            try:
                                                date_obj = dt.datetime.strptime(bill['due_date'], fmt)
                                                due_day = str(date_obj.day)
                                                break
                                            except:
                                                continue
                                    except:
                                        pass
                                
                                new_bill = {
                                    "name": bill['category'],
                                    "amount": int(bill['amount']),
                                    "due_date": due_day,
                                    "frequency": "monthly"
                                }
                                
                                st.session_state.bills[bill_state].append(new_bill)
                                st.success(f"Added {bill['category']} bill to {bill_state}!")
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Travel confirmation scanning
            st.markdown('<div class="winter-card">', unsafe_allow_html=True)
            st.markdown('**<i data-lucide="plane-takeoff" class="icon"></i>Scan for Travel Confirmations**', unsafe_allow_html=True)
            
            if st.button("Scan Travel Confirmations", type="secondary"):
                with st.spinner("Scanning for travel confirmations..."):
                    try:
                        creds = st.session_state.gmail_creds
                        service = build('gmail', 'v1', credentials=creds)
                        
                        travel_info = search_travel_confirmations(service)
                        
                        if travel_info:
                            st.success(f"Found {len(travel_info)} travel confirmations!")
                            st.session_state.scanned_travel = travel_info
                        else:
                            st.info("No travel confirmations found.")
                    except Exception as e:
                        st.error(f"Error scanning travel emails: {e}")
            
            # Display travel confirmations
            if 'scanned_travel' in st.session_state and st.session_state.scanned_travel:
                st.markdown('**<i data-lucide="calendar-days" class="icon"></i>Found Travel Confirmations:**', unsafe_allow_html=True)
                
                for i, travel in enumerate(st.session_state.scanned_travel):
                    with st.expander(f"Travel: {travel['subject'][:60]}..."):
                        st.write(f"**From:** {travel['sender']}")
                        st.write(f"**Dates Found:** {', '.join(travel['dates'])}")
                        st.write(f"**Destinations:** {', '.join(travel['destinations'])}")
                        
                        # Option to log location changes
                        if travel['dates']:
                            for date_str in travel['dates'][:2]:  # Limit to first 2 dates
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.write(f"Date: {date_str}")
                                
                                with col2:
                                    travel_state = st.selectbox(
                                        "Destination state:",
                                        list(st.session_state.states.keys()),
                                        key=f"travel_state_{i}_{date_str}"
                                    )
                                
                                with col3:
                                    if st.button(f"Log {date_str}", key=f"log_travel_{i}_{date_str}"):
                                        try:
                                            # Convert date format if needed
                                            import datetime as dt
                                            date_obj = dt.datetime.strptime(date_str, '%m/%d/%Y').date()
                                            success, message = add_day_log(travel_state, date_obj.isoformat())
                                            if success:
                                                st.success(message)
                                            else:
                                                st.warning(message)
                                        except:
                                            st.error("Could not parse date format")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Footer with TODO notes
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.9rem; padding: 1rem;">
    <p><strong><i data-lucide="rocket" class="icon"></i>Coming Soon:</strong></p>
    <p><i data-lucide="calendar" class="icon"></i>Google Calendar Integration • <i data-lucide="shield" class="icon"></i>Multi-device Sync • <i data-lucide="smartphone" class="icon"></i>Mobile App (CapacitorJS) • <i data-lucide="database" class="icon"></i>Banking Integration (Plaid)</p>
    <p><em>Built with <i data-lucide="snowflake" class="icon"></i> by Snowbird Financial Assistant</em></p>
</div>

<script>
    // Initialize Lucide icons after content loads
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
</script>
""", unsafe_allow_html=True)
