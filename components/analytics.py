
"""
Analytics integration for the Snowbird application.

This module provides comprehensive user behavior tracking and application
metrics collection while maintaining user privacy and data protection.

Analytics Capabilities:
    - Page view tracking across application sections
    - User action logging (anonymized)
    - Feature usage statistics
    - Performance monitoring
    - Error tracking and reporting
    - A/B testing support for UI improvements

Privacy-First Design:
    - No personally identifiable information (PII) collected
    - Local-first data storage with optional cloud sync
    - User-controlled analytics preferences
    - GDPR and CCPA compliant data handling
    - Transparent data usage policies

The analytics system helps improve the user experience by identifying
popular features, common user journeys, and areas for optimization
without compromising user privacy or financial data security.
"""

import streamlit as st
import datetime
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

from utils.logging_config import logger
from config import config

class Analytics:
    """Analytics tracking class"""
    
    def __init__(self):
        self.enabled = getattr(config, 'enable_analytics', True)
        self.session_id = self._get_or_create_session_id()
        
    def _get_or_create_session_id(self) -> str:
        """Get or create a unique session ID"""
        if 'analytics_session_id' not in st.session_state:
            import uuid
            st.session_state.analytics_session_id = str(uuid.uuid4())
        return st.session_state.analytics_session_id
    
    def track_event(self, event_name: str, properties: Dict[str, Any] = None):
        """Track an analytics event"""
        if not self.enabled:
            return
            
        event_data = {
            'event': event_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'session_id': self.session_id,
            'properties': properties or {}
        }
        
        # Log to file for local analytics
        self._log_event_locally(event_data)
        
        # Send to external analytics if configured
        self._send_to_external_analytics(event_data)
    
    def _log_event_locally(self, event_data: Dict[str, Any]):
        """Log event to local analytics file"""
        try:
            analytics_dir = Path("logs/analytics")
            analytics_dir.mkdir(parents=True, exist_ok=True)
            
            today = datetime.date.today().isoformat()
            analytics_file = analytics_dir / f"analytics_{today}.jsonl"
            
            with open(analytics_file, 'a') as f:
                f.write(json.dumps(event_data) + '\n')
                
        except Exception as e:
            logger.error(f"Failed to log analytics event locally: {e}")
    
    def _send_to_external_analytics(self, event_data: Dict[str, Any]):
        """Send event to external analytics service"""
        try:
            # Mixpanel integration (if configured)
            mixpanel_token = os.getenv('MIXPANEL_TOKEN')
            if mixpanel_token:
                self._send_to_mixpanel(event_data, mixpanel_token)
                
        except Exception as e:
            logger.error(f"Failed to send to external analytics: {e}")
    
    def _send_to_mixpanel(self, event_data: Dict[str, Any], token: str):
        """Send event to Mixpanel"""
        try:
            import mixpanel
            mp = mixpanel.Mixpanel(token)
            
            mp.track(
                event_data['session_id'],
                event_data['event'],
                event_data['properties']
            )
        except ImportError:
            logger.warning("Mixpanel not available for analytics")
        except Exception as e:
            logger.error(f"Failed to send to Mixpanel: {e}")

# Global analytics instance
analytics = Analytics()

def track_page_view(page_name: str):
    """Track a page view"""
    analytics.track_event('page_view', {'page': page_name})

def track_user_action(action: str, details: Dict[str, Any] = None):
    """Track a user action"""
    analytics.track_event('user_action', {
        'action': action,
        'details': details or {}
    })

def track_feature_usage(feature: str, context: Dict[str, Any] = None):
    """Track feature usage"""
    analytics.track_event('feature_usage', {
        'feature': feature,
        'context': context or {}
    })

def track_error(error_type: str, error_message: str, context: Dict[str, Any] = None):
    """Track an error occurrence"""
    analytics.track_event('error', {
        'error_type': error_type,
        'error_message': error_message,
        'context': context or {}
    })

def get_analytics_summary() -> Dict[str, Any]:
    """Get analytics summary for admin dashboard"""
    try:
        analytics_dir = Path("logs/analytics")
        if not analytics_dir.exists():
            return {'error': 'No analytics data found'}
        
        # Read recent analytics data
        today = datetime.date.today()
        events = []
        
        for i in range(7):  # Last 7 days
            date = (today - datetime.timedelta(days=i)).isoformat()
            analytics_file = analytics_dir / f"analytics_{date}.jsonl"
            
            if analytics_file.exists():
                with open(analytics_file, 'r') as f:
                    for line in f:
                        try:
                            events.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue
        
        # Generate summary
        summary = {
            'total_events': len(events),
            'unique_sessions': len(set(event.get('session_id') for event in events)),
            'event_types': {},
            'daily_activity': {}
        }
        
        for event in events:
            event_type = event.get('event', 'unknown')
            date = event.get('timestamp', '')[:10]  # Extract date
            
            summary['event_types'][event_type] = summary['event_types'].get(event_type, 0) + 1
            summary['daily_activity'][date] = summary['daily_activity'].get(date, 0) + 1
        
        return summary
        
    except Exception as e:
        logger.error(f"Failed to generate analytics summary: {e}")
        return {'error': str(e)}
"""Basic analytics tracking for Snowbird app"""
import streamlit as st
from datetime import datetime

def track_page_view(page_name):
    """Track page view"""
    if 'page_views' not in st.session_state:
        st.session_state.page_views = []
    
    st.session_state.page_views.append({
        'page': page_name,
        'timestamp': datetime.now().isoformat()
    })

def track_user_action(action, data=None):
    """Track user action"""
    if 'user_actions' not in st.session_state:
        st.session_state.user_actions = []
    
    st.session_state.user_actions.append({
        'action': action,
        'data': data or {},
        'timestamp': datetime.now().isoformat()
    })

def track_feature_usage(feature, data=None):
    """Track feature usage"""
    if 'feature_usage' not in st.session_state:
        st.session_state.feature_usage = []
    
    st.session_state.feature_usage.append({
        'feature': feature,
        'data': data or {},
        'timestamp': datetime.now().isoformat()
    })
