
"""
Data persistence utilities for the Snowbird app.
Handles saving and loading user data to/from local files.
"""

import json
import os
from typing import Dict, Any
from datetime import datetime
import streamlit as st
from utils.logging_config import logger

DATA_DIR = "user_data"
DATA_FILE = "snowbird_data.json"

def ensure_data_directory():
    """Ensure the data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_user_data():
    """Save current session state to file"""
    try:
        ensure_data_directory()
        
        data = {
            'states': st.session_state.get('states', {}),
            'home_budgets': st.session_state.get('home_budgets', {}),
            'seasonal_cash_flow': st.session_state.get('seasonal_cash_flow', {}),
            'tax_threshold': st.session_state.get('tax_threshold', 183),
            'risk_warning_days': st.session_state.get('risk_warning_days', 14),
            'default_state': st.session_state.get('default_state', 'Arizona'),
            'auto_save': st.session_state.get('auto_save', True),
            'show_tips': st.session_state.get('show_tips', True),
            'last_saved': datetime.now().isoformat()
        }
        
        file_path = os.path.join(DATA_DIR, DATA_FILE)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info("User data saved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save user data: {e}")
        return False

def load_user_data():
    """Load user data from file"""
    try:
        file_path = os.path.join(DATA_DIR, DATA_FILE)
        
        if not os.path.exists(file_path):
            logger.info("No saved data found, using defaults")
            return False
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Load data into session state
        st.session_state.states = data.get('states', {"Arizona": 0, "Minnesota": 0})
        st.session_state.home_budgets = data.get('home_budgets', {
            "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100, "Maintenance": 75},
            "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90, "Maintenance": 100}
        })
        st.session_state.seasonal_cash_flow = data.get('seasonal_cash_flow', {
            "Travel": 500, "Healthcare": 400, "Supplemental Insurance": 200, "Emergency Fund": 300
        })
        st.session_state.tax_threshold = data.get('tax_threshold', 183)
        st.session_state.risk_warning_days = data.get('risk_warning_days', 14)
        st.session_state.default_state = data.get('default_state', 'Arizona')
        st.session_state.auto_save = data.get('auto_save', True)
        st.session_state.show_tips = data.get('show_tips', True)
        
        logger.info("User data loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load user data: {e}")
        return False

def auto_save_data():
    """Auto-save data if enabled"""
    if st.session_state.get('auto_save', True):
        save_user_data()

def get_data_file_info():
    """Get information about the saved data file"""
    try:
        file_path = os.path.join(DATA_DIR, DATA_FILE)
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                'exists': True,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'path': file_path
            }
        else:
            return {'exists': False}
    except Exception as e:
        logger.error(f"Failed to get data file info: {e}")
        return {'exists': False, 'error': str(e)}
