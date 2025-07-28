
import datetime
from typing import Dict, List, Any

# Default data structures
DEFAULT_STATES = {"Arizona": 0, "Minnesota": 0}

DEFAULT_HOME_BUDGETS = {
    "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100, "Maintenance": 75},
    "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90, "Maintenance": 100}
}

DEFAULT_SEASONAL_CASH_FLOW = {
    "Travel": 500,
    "Healthcare": 400,
    "Supplemental Insurance": 200,
    "Emergency Fund": 300
}

DEFAULT_BILLS = {
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

DEFAULT_MIGRATION_CHECKLIST = [
    {"task": "Adjust thermostat", "category": "HVAC", "completed": False},
    {"task": "Empty refrigerator", "category": "Kitchen", "completed": False},
    {"task": "Forward mail", "category": "Mail", "completed": False},
    {"task": "Turn off water main", "category": "Utilities", "completed": False},
    {"task": "Set up security system", "category": "Security", "completed": False},
    {"task": "Arrange lawn service", "category": "Exterior", "completed": False},
    {"task": "Clean out gutters", "category": "Exterior", "completed": False},
    {"task": "Pack seasonal clothes", "category": "Personal", "completed": False}
]

class SnowbirdData:
    """Data management class for Snowbird app"""
    
    def __init__(self):
        self.tax_threshold = 183
    
    def get_tax_status(self, days: int, threshold: int = None):
        """Get tax residency status for a state"""
        if threshold is None:
            threshold = self.tax_threshold
            
        percentage = (days / threshold) * 100
        if days >= threshold:
            return "TAX RESIDENT", "status-danger"
        elif days >= threshold * 0.9:
            return "CRITICAL", "status-warning"
        elif days >= threshold * 0.75:
            return "CAUTION", "status-warning"
        else:
            return "SAFE", "status-safe"
    
    def add_day_log(self, state: str, date_str: str = None, auto_logged: bool = False):
        """Add a day to the log"""
        import streamlit as st
        
        if date_str is None:
            date_str = datetime.date.today().isoformat()

        # Check if already logged
        existing = next((log for log in st.session_state.day_log if log['date'] == date_str), None)
        if existing:
            return False, f"Already logged {date_str} in {existing['state']}"

        st.session_state.day_log.append({
            'date': date_str,
            'state': state,
            'timestamp': datetime.datetime.now().isoformat(),
            'auto_logged': auto_logged
        })
        st.session_state.states[state] += 1
        return True, f"Logged {date_str} in {state}" + (" (auto)" if auto_logged else "")
    
    def generate_report_data(self):
        """Generate comprehensive report data"""
        import streamlit as st
        
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
