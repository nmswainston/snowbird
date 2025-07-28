
"""
Profile synchronization utilities for the Snowbird app.
Syncs local session state with Firebase user profiles.
"""

import streamlit as st
from typing import Dict, Any, Optional
from utils.firebase_auth import get_firebase_auth
from utils.firebase_database import get_firebase_database
from utils.logging_config import logger

class ProfileSync:
    """Profile synchronization manager"""
    
    def __init__(self):
        self.auth = get_firebase_auth()
        self.db = get_firebase_database()
    
    def load_user_profile_to_session(self, uid: str) -> bool:
        """Load user profile from Firebase to session state"""
        try:
            profile = self.db.get_user_profile(uid)
            
            if profile:
                # Load location tracking data
                st.session_state.states = profile.get('states', {'Arizona': 0, 'Minnesota': 0})
                
                # Load budget data
                st.session_state.home_budgets = profile.get('home_budgets', {
                    'Arizona': {'Utilities': 200, 'Insurance': 150, 'HOA': 100},
                    'Minnesota': {'Utilities': 250, 'Insurance': 170, 'HOA': 90}
                })
                
                # Load cash flow data
                st.session_state.seasonal_cash_flow = profile.get('seasonal_cash_flow', {
                    'Travel': 300,
                    'Healthcare': 400,
                    'Supplemental Insurance': 200
                })
                
                # Load preferences
                st.session_state.user_preferences = profile.get('preferences', {
                    'theme': 'default',
                    'notifications': True,
                    'auto_tracking': False
                })
                
                # Load other user data
                st.session_state.user_profile = profile
                
                logger.info(f"User profile loaded to session for UID: {uid}")
                return True
            else:
                logger.warning(f"No profile found for UID: {uid}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to load user profile: {e}")
            return False
    
    def save_session_to_profile(self, uid: str) -> bool:
        """Save session state data to user profile"""
        try:
            update_data = {}
            
            # Save location tracking data if it exists
            if 'states' in st.session_state:
                update_data['states'] = st.session_state.states
            
            # Save budget data if it exists
            if 'home_budgets' in st.session_state:
                update_data['home_budgets'] = st.session_state.home_budgets
            
            # Save cash flow data if it exists
            if 'seasonal_cash_flow' in st.session_state:
                update_data['seasonal_cash_flow'] = st.session_state.seasonal_cash_flow
            
            # Save preferences if they exist
            if 'user_preferences' in st.session_state:
                update_data['preferences'] = st.session_state.user_preferences
            
            if update_data:
                success = self.db.update_user_profile(uid, update_data)
                if success:
                    logger.info(f"Session data saved to profile for UID: {uid}")
                return success
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save session to profile: {e}")
            return False
    
    def sync_location_data(self, uid: str, states: Dict[str, int]) -> bool:
        """Sync location tracking data"""
        try:
            # Update session state
            st.session_state.states = states
            
            # Save to Firebase
            success = self.db.save_location_data(uid, states)
            
            if success:
                # Log activity
                self.db.log_activity(uid, 'location_update', {'states': states})
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to sync location data: {e}")
            return False
    
    def sync_budget_data(self, uid: str, budgets: Dict[str, Dict]) -> bool:
        """Sync budget data"""
        try:
            # Update session state
            st.session_state.home_budgets = budgets
            
            # Save to Firebase
            success = self.db.save_budget_data(uid, budgets)
            
            if success:
                # Log activity
                self.db.log_activity(uid, 'budget_update', {'budgets': budgets})
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to sync budget data: {e}")
            return False
    
    def auto_sync(self):
        """Automatically sync session data with profile"""
        user = self.auth.get_current_user()
        
        if user:
            uid = user['uid']
            
            # Auto-save critical data periodically
            if 'states' in st.session_state:
                self.sync_location_data(uid, st.session_state.states)
            
            if 'home_budgets' in st.session_state:
                self.sync_budget_data(uid, st.session_state.home_budgets)

# Global sync instance
profile_sync = ProfileSync()

def get_profile_sync():
    """Get the global profile sync instance"""
    return profile_sync

def initialize_user_session():
    """Initialize user session with profile data"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if user:
        uid = user['uid']
        sync = get_profile_sync()
        
        # Load profile data if not already loaded
        if 'user_profile' not in st.session_state:
            sync.load_user_profile_to_session(uid)
        
        return True
    
    return False

def save_user_session():
    """Save current session data to user profile"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if user:
        uid = user['uid']
        sync = get_profile_sync()
        return sync.save_session_to_profile(uid)
    
    return False
