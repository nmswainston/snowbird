
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

from utils.config import settings
from utils.logger import logger

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
            # Check if Firebase secrets are configured
            service_account_info = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT', None)
            firebase_config_info = getattr(settings, 'FIREBASE_CONFIG', None)
            
            if not service_account_info or not firebase_config_info:
                logger.error("Firebase configuration missing. Please check your Replit Secrets.")
                return False
            
            # Initialize Firebase Admin SDK if not already done
            if not firebase_admin._apps:
                try:
                    # Convert to proper format if needed
                    if isinstance(service_account_info, str):
                        # If it's a JSON string, parse it
                        service_account_info = json.loads(service_account_info)
                    
                    if isinstance(service_account_info, dict):
                        cred = credentials.Certificate(service_account_info)
                        self.app = firebase_admin.initialize_app(cred)
                        logger.info("Firebase Admin SDK initialized successfully")
                    else:
                        logger.error("Invalid Firebase service account format")
                        return False
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in FIREBASE_SERVICE_ACCOUNT: {e}")
                    return False
                except Exception as e:
                    logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
                    return False
            else:
                self.app = firebase_admin.get_app()
            
            # Initialize Firestore
            try:
                self.db = firestore.client()
            except Exception as e:
                logger.error(f"Failed to initialize Firestore: {e}")
                return False
            
            # Initialize Pyrebase for client-side auth
            try:
                if isinstance(firebase_config_info, str):
                    firebase_config_info = json.loads(firebase_config_info)
                
                self.firebase_app = pyrebase.initialize_app(firebase_config_info)
                self.auth_config = self.firebase_app.auth()
                logger.info("Pyrebase initialized successfully")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in FIREBASE_CONFIG: {e}")
                return False
            except Exception as e:
                logger.error(f"Failed to initialize Pyrebase: {e}")
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
