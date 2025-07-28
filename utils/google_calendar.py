
"""
Google Calendar integration for Snowbird Financial Assistant.
Syncs residency logs and reminders with user's Google Calendar.
"""

import streamlit as st
import datetime
from typing import Dict, List, Optional, Any
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
from utils.logging_config import logger

class GoogleCalendarSync:
    """Handle Google Calendar integration for Snowbird app"""
    
    # OAuth 2.0 scopes for calendar access
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        """Initialize Google Calendar sync handler"""
        self.credentials = None
        self.service = None
        
    def is_authenticated(self) -> bool:
        """Check if user has authenticated with Google Calendar"""
        return 'google_calendar_credentials' in st.session_state and st.session_state.google_calendar_credentials is not None
    
    def get_auth_url(self) -> Optional[str]:
        """
        Generate Google OAuth URL for calendar access.
        Returns the authorization URL for user to visit.
        """
        try:
            # Google OAuth configuration - in production, store this in secrets
            oauth_config = {
                "web": {
                    "client_id": st.secrets.get("GOOGLE_CLIENT_ID", ""),
                    "client_secret": st.secrets.get("GOOGLE_CLIENT_SECRET", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:8501/oauth2callback"]
                }
            }
            
            if not oauth_config["web"]["client_id"]:
                return None
                
            # Create OAuth flow
            flow = Flow.from_client_config(
                oauth_config,
                scopes=self.SCOPES
            )
            flow.redirect_uri = "http://localhost:8501/oauth2callback"
            
            # Generate authorization URL
            auth_url, _ = flow.authorization_url(prompt='consent')
            return auth_url
            
        except Exception as e:
            logger.error(f"Error generating auth URL: {e}")
            return None
    
    def authenticate_with_code(self, auth_code: str) -> bool:
        """
        Complete OAuth flow with authorization code.
        
        Args:
            auth_code: Authorization code from Google OAuth callback
            
        Returns:
            bool: True if authentication successful
        """
        try:
            # Complete OAuth flow with authorization code
            oauth_config = {
                "web": {
                    "client_id": st.secrets.get("GOOGLE_CLIENT_ID", ""),
                    "client_secret": st.secrets.get("GOOGLE_CLIENT_SECRET", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:8501/oauth2callback"]
                }
            }
            
            flow = Flow.from_client_config(oauth_config, scopes=self.SCOPES)
            flow.redirect_uri = "http://localhost:8501/oauth2callback"
            
            # Exchange code for credentials
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            
            # Store credentials in session state
            st.session_state.google_calendar_credentials = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            return True
            
        except Exception as e:
            logger.error(f"Error authenticating with code: {e}")
            return False
    
    def _get_service(self):
        """
        Get Google Calendar API service instance.
        Handles token refresh if needed.
        """
        if not self.is_authenticated():
            return None
            
        try:
            # Create credentials from session state
            creds_data = st.session_state.google_calendar_credentials
            credentials = Credentials(
                token=creds_data['token'],
                refresh_token=creds_data.get('refresh_token'),
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )
            
            # Refresh token if expired
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                # Update session state with new token
                st.session_state.google_calendar_credentials['token'] = credentials.token
            
            # Build Calendar API service
            service = build('calendar', 'v3', credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Error getting calendar service: {e}")
            return None
    
    def create_residency_log_event(self, state: str, date: datetime.date, notes: str = "") -> bool:
        """
        Create a calendar event for a residency day log.
        
        Args:
            state: State where the day was logged (e.g., "Arizona", "Minnesota")
            date: Date of the residency day
            notes: Optional notes for the event
            
        Returns:
            bool: True if event created successfully
        """
        service = self._get_service()
        if not service:
            return False
            
        try:
            # Create event details
            event = {
                'summary': f'Snowbird: {state} Day Logged',
                'description': f'Tax residency day logged in {state}. {notes}'.strip(),
                'start': {
                    'date': date.isoformat(),
                    'timeZone': 'America/Phoenix',  # Default timezone
                },
                'end': {
                    'date': date.isoformat(),
                    'timeZone': 'America/Phoenix',
                },
                'colorId': '2' if state == 'Arizona' else '9',  # Orange for AZ, Blue for MN
                'extendedProperties': {
                    'private': {
                        'snowbird_type': 'residency_log',
                        'state': state,
                        'app_version': '1.0'
                    }
                }
            }
            
            # Create the event in primary calendar
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"Created calendar event for {state} day: {created_event.get('id')}")
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error creating calendar event: {e}")
            return False
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return False
    
    def create_reminder_event(self, title: str, description: str, due_date: datetime.date, 
                            reminder_type: str = "bill") -> bool:
        """
        Create a calendar reminder event for bills or threshold alerts.
        
        Args:
            title: Event title (e.g., "Arizona Electric Bill Due")
            description: Detailed description
            due_date: Date when the reminder is due
            reminder_type: Type of reminder ("bill", "threshold", "tax")
            
        Returns:
            bool: True if event created successfully
        """
        service = self._get_service()
        if not service:
            return False
            
        try:
            # Set color based on reminder type
            color_map = {
                'bill': '3',      # Purple for bills
                'threshold': '11', # Red for threshold alerts
                'tax': '5'        # Yellow for tax reminders
            }
            
            # Create event details
            event = {
                'summary': f'Snowbird Reminder: {title}',
                'description': description,
                'start': {
                    'date': due_date.isoformat(),
                    'timeZone': 'America/Phoenix',
                },
                'end': {
                    'date': due_date.isoformat(),
                    'timeZone': 'America/Phoenix',
                },
                'colorId': color_map.get(reminder_type, '1'),
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before
                    ],
                },
                'extendedProperties': {
                    'private': {
                        'snowbird_type': 'reminder',
                        'reminder_type': reminder_type,
                        'app_version': '1.0'
                    }
                }
            }
            
            # Create the event
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"Created reminder event: {created_event.get('id')}")
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error creating reminder event: {e}")
            return False
        except Exception as e:
            logger.error(f"Error creating reminder event: {e}")
            return False
    
    def get_snowbird_events(self, start_date: datetime.date, end_date: datetime.date) -> List[Dict]:
        """
        Retrieve Snowbird-created events from calendar within date range.
        
        Args:
            start_date: Start date for event search
            end_date: End date for event search
            
        Returns:
            List of event dictionaries
        """
        service = self._get_service()
        if not service:
            return []
            
        try:
            # Query events with Snowbird identifier
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_date.isoformat() + 'T00:00:00Z',
                timeMax=end_date.isoformat() + 'T23:59:59Z',
                singleEvents=True,
                orderBy='startTime',
                q='Snowbird'  # Search for events containing "Snowbird"
            ).execute()
            
            events = events_result.get('items', [])
            
            # Filter to only Snowbird app events
            snowbird_events = []
            for event in events:
                extended_props = event.get('extendedProperties', {}).get('private', {})
                if extended_props.get('snowbird_type'):
                    snowbird_events.append({
                        'id': event['id'],
                        'title': event['summary'],
                        'date': event['start'].get('date', event['start'].get('dateTime')),
                        'type': extended_props.get('snowbird_type'),
                        'state': extended_props.get('state'),
                        'reminder_type': extended_props.get('reminder_type')
                    })
            
            return snowbird_events
            
        except HttpError as e:
            logger.error(f"HTTP error retrieving events: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving events: {e}")
            return []
    
    def disconnect(self):
        """Disconnect from Google Calendar and clear credentials"""
        if 'google_calendar_credentials' in st.session_state:
            del st.session_state.google_calendar_credentials
        logger.info("Disconnected from Google Calendar")

# Global instance
calendar_sync = GoogleCalendarSync()
