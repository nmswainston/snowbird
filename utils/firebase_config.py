
"""
Firebase configuration and initialization for the Snowbird app.
Handles authentication and Firestore database connections.
"""

import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Dict, Any, Optional
import pyrebase

from utils.logging_config import logger

class FirebaseConfig:
    """Firebase configuration and connection manager"""
    
    def __init__(self):
        self.app = None
        self.db = None
        self.auth_config = None
        self.firebase_app = None
        
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK and Pyrebase"""
        try:
            # Initialize Firebase Admin SDK if not already done
            if not firebase_admin._apps:
                # Try to get service account from settings
                service_account_info = settings.FIREBASE_SERVICE_ACCOUNT
                
                if service_account_info:
                    # Convert to proper format if needed
                    if isinstance(service_account_info, dict):
                        cred = credentials.Certificate(service_account_info)
                    else:
                        # If it's a JSON string, parse it
                        cred = credentials.Certificate(json.loads(service_account_info))
                    
                    self.app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized successfully")
                else:
                    logger.warning("Firebase service account not found in secrets")
                    return False
            else:
                self.app = firebase_admin.get_app()
            
            # Initialize Firestore
            self.db = firestore.client()
            
            # Initialize Pyrebase for client-side auth
            firebase_config = settings.FIREBASE_CONFIG
            if firebase_config:
                self.firebase_app = pyrebase.initialize_app(firebase_config)
                self.auth_config = self.firebase_app.auth()
                logger.info("Pyrebase initialized successfully")
            else:
                logger.warning("Firebase config not found in secrets")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            return False
    
    def get_firestore_client(self):
        """Get Firestore database client"""
        if not self.db:
            self.initialize_firebase()
        return self.db
    
    def get_auth_client(self):
        """Get Firebase Auth client"""
        if not self.auth_config:
            self.initialize_firebase()
        return self.auth_config

# Global Firebase instance
firebase_config = FirebaseConfig()

def get_firebase_config():
    """Get the global Firebase configuration instance"""
    return firebase_config
