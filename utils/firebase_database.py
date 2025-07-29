
"""
Firebase Firestore database utilities for the Snowbird app.
Handles user profiles and data persistence.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.firebase_config import get_firebase_config
from utils.logging_config import logger

class FirebaseDatabase:
    """Firebase Firestore database manager"""
    
    def __init__(self):
        self.firebase_config = get_firebase_config()
        self.db = None
        
    def initialize(self):
        """Initialize Firestore database"""
        if self.firebase_config.initialize_firebase():
            self.db = self.firebase_config.get_firestore_client()
            return True
        return False
    
    def create_user_profile(self, uid: str, email: str, display_name: str = "", additional_data: Dict = None) -> bool:
        """Create a new user profile in Firestore"""
        try:
            if not self.db:
                if not self.initialize():
                    return False
            
            profile_data = {
                'uid': uid,
                'email': email,
                'display_name': display_name or email.split('@')[0],
                'created_at': datetime.now(),
                'last_login': datetime.now(),
                'states': {'Arizona': 0, 'Minnesota': 0},
                'home_budgets': {
                    'Arizona': {'Utilities': 200, 'Insurance': 150, 'HOA': 100},
                    'Minnesota': {'Utilities': 250, 'Insurance': 170, 'HOA': 90}
                },
                'seasonal_cash_flow': {
                    'Travel': 300,
                    'Healthcare': 400,
                    'Supplemental Insurance': 200
                },
                'preferences': {
                    'theme': 'light',
                    'notifications': True,
                    'auto_tracking': False
                },
                'trip_plans': [],
                'financial_notes': [],
                'saved_destinations': []
            }
            
            if additional_data:
                profile_data.update(additional_data)
            
            # Create document in users collection
            self.db.collection('users').document(uid).set(profile_data)
            
            logger.info(f"User profile created for UID: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user profile: {e}")
            return False
    
    def get_user_profile(self, uid: str) -> Optional[Dict[str, Any]]:
        """Get user profile from Firestore"""
        try:
            if not self.db:
                if not self.initialize():
                    return None
            
            doc = self.db.collection('users').document(uid).get()
            
            if doc.exists:
                profile = doc.to_dict()
                logger.info(f"User profile retrieved for UID: {uid}")
                return profile
            else:
                logger.warning(f"User profile not found for UID: {uid}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return None
    
    def update_user_profile(self, uid: str, data: Dict[str, Any]) -> bool:
        """Update user profile in Firestore"""
        try:
            if not self.db:
                if not self.initialize():
                    return False
            
            # Add timestamp
            data['updated_at'] = datetime.now()
            
            # Update document
            self.db.collection('users').document(uid).update(data)
            
            logger.info(f"User profile updated for UID: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user profile: {e}")
            return False
    
    def update_last_login(self, uid: str) -> bool:
        """Update user's last login timestamp"""
        return self.update_user_profile(uid, {'last_login': datetime.now()})
    
    def save_location_data(self, uid: str, states: Dict[str, int]) -> bool:
        """Save user's location tracking data"""
        try:
            # Also save day_log if it exists in session state
            import streamlit as st
            update_data = {'states': states}
            
            if 'day_log' in st.session_state:
                update_data['day_log'] = st.session_state.day_log
            
            return self.update_user_profile(uid, update_data)
        except Exception as e:
            logger.error(f"Failed to save location data: {e}")
            return self.update_user_profile(uid, {'states': states})
    
    def save_budget_data(self, uid: str, budgets: Dict[str, Dict]) -> bool:
        """Save user's budget data"""
        return self.update_user_profile(uid, {'home_budgets': budgets})
    
    def save_preferences(self, uid: str, preferences: Dict[str, Any]) -> bool:
        """Save user preferences"""
        return self.update_user_profile(uid, {'preferences': preferences})
    
    def log_activity(self, uid: str, activity_type: str, data: Dict[str, Any] = None) -> bool:
        """Log user activity for analytics"""
        try:
            if not self.db:
                if not self.initialize():
                    return False
            
            activity_data = {
                'uid': uid,
                'activity_type': activity_type,
                'timestamp': datetime.now(),
                'data': data or {}
            }
            
            # Add to activities collection
            self.db.collection('activities').add(activity_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
            return False
    
    def get_user_activities(self, uid: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's recent activities"""
        try:
            if not self.db:
                if not self.initialize():
                    return []
            
            activities = (
                self.db.collection('activities')
                .where('uid', '==', uid)
                .order_by('timestamp', direction='DESCENDING')
                .limit(limit)
                .stream()
            )
            
            return [activity.to_dict() for activity in activities]
            
        except Exception as e:
            logger.error(f"Failed to get user activities: {e}")
            return []
    
    def save_trip_plans(self, uid: str, trip_plans: List[Dict[str, Any]]) -> bool:
        """Save user's trip plans"""
        return self.update_user_profile(uid, {'trip_plans': trip_plans})
    
    def save_financial_notes(self, uid: str, notes: List[Dict[str, Any]]) -> bool:
        """Save user's financial notes"""
        return self.update_user_profile(uid, {'financial_notes': notes})
    
    def save_saved_destinations(self, uid: str, destinations: List[Dict[str, Any]]) -> bool:
        """Save user's saved destinations"""
        return self.update_user_profile(uid, {'saved_destinations': destinations})
    
    def get_trip_plans(self, uid: str) -> List[Dict[str, Any]]:
        """Get user's trip plans"""
        profile = self.get_user_profile(uid)
        if profile:
            return profile.get('trip_plans', [])
        return []
    
    def get_financial_notes(self, uid: str) -> List[Dict[str, Any]]:
        """Get user's financial notes"""
        profile = self.get_user_profile(uid)
        if profile:
            return profile.get('financial_notes', [])
        return []
    
    def get_saved_destinations(self, uid: str) -> List[Dict[str, Any]]:
        """Get user's saved destinations"""
        profile = self.get_user_profile(uid)
        if profile:
            return profile.get('saved_destinations', [])
        return []
    
    def listen_to_user_changes(self, uid: str, callback):
        """Listen for real-time changes to user data"""
        try:
            if not self.db:
                if not self.initialize():
                    return None
            
            # Create a listener for real-time updates
            doc_ref = self.db.collection('users').document(uid)
            
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    if doc.exists:
                        callback(doc.to_dict())
            
            return doc_ref.on_snapshot(on_snapshot)
            
        except Exception as e:
            logger.error(f"Failed to create listener: {e}")
            return None

# Global database instance
firebase_db = FirebaseDatabase()

def get_firebase_database():
    """Get the global Firebase database instance"""
    return firebase_db
