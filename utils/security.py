
"""
Security utilities for protecting user data in the Snowbird Financial Assistant.
"""
import hashlib
import secrets
import base64
import json
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import streamlit as st
from utils.logging_config import data_logger
from utils.error_handling import handle_errors

class DataEncryption:
    """Handle encryption/decryption of sensitive data"""
    
    def __init__(self):
        self.key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key from secure storage"""
        if 'encryption_key' not in st.session_state:
            # Use a combination of session ID and secret key
            password = st.secrets.get("SECRET_KEY", "default-key").encode()
            salt = hashlib.sha256(st.session_state.get('session_id', 'default').encode()).digest()[:16]
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            st.session_state.encryption_key = key
        
        return st.session_state.encryption_key
    
    @handle_errors(show_error=False, return_none_on_error=True)
    def encrypt_data(self, data: Any) -> Optional[str]:
        """Encrypt sensitive data"""
        try:
            json_data = json.dumps(data, default=str)
            encrypted = self.fernet.encrypt(json_data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            data_logger.error(f"Encryption failed: {e}")
            return None
    
    @handle_errors(show_error=False, return_none_on_error=True)
    def decrypt_data(self, encrypted_data: str) -> Optional[Any]:
        """Decrypt sensitive data"""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(decoded)
            return json.loads(decrypted.decode())
        except Exception as e:
            data_logger.error(f"Decryption failed: {e}")
            return None

class SessionSecurity:
    """Manage secure sessions and user data"""
    
    @staticmethod
    def initialize_secure_session():
        """Initialize secure session with unique ID"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = secrets.token_urlsafe(32)
        
        if 'session_timeout' not in st.session_state:
            import datetime
            # 8 hour session timeout
            st.session_state.session_timeout = datetime.datetime.now() + datetime.timedelta(hours=8)
    
    @staticmethod
    def check_session_validity() -> bool:
        """Check if current session is still valid"""
        if 'session_timeout' not in st.session_state:
            return False
        
        import datetime
        return datetime.datetime.now() < st.session_state.session_timeout
    
    @staticmethod
    def refresh_session():
        """Refresh session timeout"""
        import datetime
        st.session_state.session_timeout = datetime.datetime.now() + datetime.timedelta(hours=8)
    
    @staticmethod
    def clear_sensitive_data():
        """Clear all sensitive data from session"""
        sensitive_keys = [
            'gmail_creds', 'access_token', 'gmail_suggestions', 
            'gmail_emails', 'encryption_key', 'user_profile'
        ]
        
        for key in sensitive_keys:
            if key in st.session_state:
                del st.session_state[key]

class DataPrivacy:
    """Handle data privacy and anonymization"""
    
    @staticmethod
    def hash_email(email: str) -> str:
        """Create a privacy-preserving hash of email address"""
        return hashlib.sha256(email.encode()).hexdigest()[:16]
    
    @staticmethod
    def anonymize_location_data(location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove personally identifiable information from location data"""
        anonymized = location_data.copy()
        
        # Remove precise coordinates, keep only general area
        if 'latitude' in anonymized and 'longitude' in anonymized:
            # Round to ~1 mile precision
            anonymized['latitude'] = round(anonymized['latitude'], 2)
            anonymized['longitude'] = round(anonymized['longitude'], 2)
        
        # Remove IP address if present
        anonymized.pop('ip_address', None)
        anonymized.pop('user_agent', None)
        
        return anonymized
    
    @staticmethod
    def sanitize_email_content(email_content: str) -> str:
        """Remove sensitive information from email content"""
        import re
        
        # Remove credit card numbers
        email_content = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD-REDACTED]', email_content)
        
        # Remove SSN patterns
        email_content = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]', email_content)
        
        # Remove phone numbers
        email_content = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE-REDACTED]', email_content)
        
        return email_content

class AuditLogger:
    """Log security-relevant events for compliance"""
    
    @staticmethod
    def log_data_access(action: str, data_type: str, user_id: str = None):
        """Log data access events"""
        data_logger.info(f"Data access: {action}", extra={
            'event_type': 'data_access',
            'action': action,
            'data_type': data_type,
            'user_id': user_id or 'anonymous',
            'timestamp': str(datetime.datetime.now()),
            'session_id': st.session_state.get('session_id', 'unknown')
        })
    
    @staticmethod
    def log_gmail_access(email_count: int, user_email: str = None):
        """Log Gmail API access"""
        data_logger.info(f"Gmail accessed: {email_count} emails processed", extra={
            'event_type': 'gmail_access',
            'email_count': email_count,
            'user_email': DataPrivacy.hash_email(user_email) if user_email else 'unknown',
            'timestamp': str(datetime.datetime.now())
        })
    
    @staticmethod
    def log_location_tracking(location: str, method: str):
        """Log location tracking events"""
        data_logger.info(f"Location tracked: {location} via {method}", extra={
            'event_type': 'location_tracking',
            'location': location,
            'method': method,
            'timestamp': str(datetime.datetime.now())
        })

def get_privacy_notice() -> str:
    """Return privacy notice text"""
    return """
    **🔒 Your Privacy & Security**
    
    • **Local Processing**: Your data is processed locally in your session
    • **No Data Storage**: We don't store your personal information on our servers
    • **Encrypted Sessions**: All sensitive data is encrypted in your browser session
    • **Gmail Security**: OAuth2 ensures we never see your Gmail password
    • **Audit Logs**: Security events are logged for your protection
    • **Session Timeout**: Your session automatically expires after 8 hours
    • **Data Anonymization**: Location data is anonymized when possible
    
    Your financial and personal information remains private and secure.
    """
