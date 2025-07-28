
import streamlit as st
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    
    if 'gmail_creds' in st.session_state:
        creds = st.session_state.gmail_creds
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                st.error(f"Failed to refresh credentials: {e}")
                return None
        else:
            st.warning("Gmail integration requires OAuth setup. Please contact support for setup instructions.")
            return None
    
    st.session_state.gmail_creds = creds
    return creds

def check_openai_availability():
    """Check if OpenAI is available and configured"""
    try:
        from openai import OpenAI
        from utils.config import settings
        
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
            try:
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                return True, client
            except Exception:
                return False, None
        else:
            return False, None
    except ImportError:
        return False, None
