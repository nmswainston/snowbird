
"""
Firebase authentication utilities for the Snowbird app.
Handles user login, logout, and session management.
"""

import streamlit as st
import json
from typing import Optional, Dict, Any
from utils.firebase_config import get_firebase_config
from utils.logging_config import logger

class FirebaseAuth:
    """Firebase authentication manager"""
    
    def __init__(self):
        self.firebase_config = get_firebase_config()
        self.auth = None
        
    def initialize(self):
        """Initialize Firebase authentication"""
        if self.firebase_config.initialize_firebase():
            self.auth = self.firebase_config.get_auth_client()
            return True
        return False
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Log in a user with email and password
        
        Returns:
            Dict with success status, user data, and any error messages
        """
        try:
            if not self.auth:
                if not self.initialize():
                    return {"success": False, "error": "Firebase not initialized"}
            
            # Sign in user
            user = self.auth.sign_in_with_email_and_password(email, password)
            
            # Get user info
            user_info = self.auth.get_account_info(user['idToken'])
            
            # Store in session state
            st.session_state.user = {
                'uid': user['localId'],
                'email': user['email'],
                'token': user['idToken'],
                'refresh_token': user['refreshToken'],
                'user_info': user_info
            }
            
            logger.info(f"User logged in successfully: {email}")
            return {"success": True, "user": st.session_state.user}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Login failed for {email}: {error_msg}")
            return {"success": False, "error": error_msg}
    
    def register_user(self, email: str, password: str, display_name: str = "") -> Dict[str, Any]:
        """
        Register a new user
        
        Returns:
            Dict with success status, user data, and any error messages
        """
        try:
            if not self.auth:
                if not self.initialize():
                    return {"success": False, "error": "Firebase not initialized"}
            
            # Create user
            user = self.auth.create_user_with_email_and_password(email, password)
            
            # Update profile if display name provided
            if display_name:
                self.auth.update_profile(user['idToken'], display_name=display_name)
            
            # Store in session state
            st.session_state.user = {
                'uid': user['localId'],
                'email': user['email'],
                'token': user['idToken'],
                'refresh_token': user['refreshToken'],
                'display_name': display_name
            }
            
            logger.info(f"User registered successfully: {email}")
            return {"success": True, "user": st.session_state.user}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Registration failed for {email}: {error_msg}")
            return {"success": False, "error": error_msg}
    
    def logout_user(self):
        """Log out the current user"""
        try:
            # Clear session state
            if 'user' in st.session_state:
                del st.session_state.user
            
            # Clear any other user-related session data
            user_keys = [key for key in st.session_state.keys() if key.startswith('user_')]
            for key in user_keys:
                del st.session_state[key]
            
            logger.info("User logged out successfully")
            return True
            
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return 'user' in st.session_state and st.session_state.user is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        if self.is_authenticated():
            return st.session_state.user
        return None
    
    def refresh_token(self) -> bool:
        """Refresh the user's authentication token"""
        try:
            if not self.is_authenticated():
                return False
            
            user = st.session_state.user
            refresh_token = user.get('refresh_token')
            
            if not refresh_token:
                return False
            
            # Refresh the token
            new_token = self.auth.refresh(refresh_token)
            
            # Update session state
            st.session_state.user.update({
                'token': new_token['idToken'],
                'refresh_token': new_token['refreshToken']
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return False

# Global auth instance
firebase_auth = FirebaseAuth()

def get_firebase_auth():
    """Get the global Firebase auth instance"""
    return firebase_auth
