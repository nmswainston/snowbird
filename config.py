
import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Gmail API
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    # Email settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # App settings
    TAX_THRESHOLD_DEFAULT = 183
    MAX_SEARCH_RESULTS = 50
    
    # Feature flags
    ENABLE_GMAIL_INTEGRATION = True
    ENABLE_AI_FEATURES = True
    ENABLE_NOTIFICATIONS = True
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'openai_api_key': cls.OPENAI_API_KEY,
            'gmail_scopes': cls.GMAIL_SCOPES,
            'smtp_server': cls.SMTP_SERVER,
            'smtp_port': cls.SMTP_PORT,
            'smtp_username': cls.SMTP_USERNAME,
            'smtp_password': cls.SMTP_PASSWORD,
            'tax_threshold': cls.TAX_THRESHOLD_DEFAULT,
            'max_search_results': cls.MAX_SEARCH_RESULTS,
            'enable_gmail': cls.ENABLE_GMAIL_INTEGRATION,
            'enable_ai': cls.ENABLE_AI_FEATURES,
            'enable_notifications': cls.ENABLE_NOTIFICATIONS
        }
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return os.getenv("ENVIRONMENT", "development") == "production"
