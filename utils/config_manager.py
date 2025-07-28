
"""
Configuration management utilities for the Snowbird app.
Provides helper functions for working with the Pydantic configuration.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from config import config, AppConfig

def reload_config() -> AppConfig:
    """Reload configuration from environment variables"""
    global config
    config = AppConfig()
    return config

def update_config_from_dict(updates: Dict[str, Any]) -> None:
    """Update configuration values from dictionary"""
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)

def get_config_summary() -> Dict[str, Any]:
    """Get a summary of current configuration (safe for logging)"""
    return {
        'app_name': config.app_name,
        'app_version': config.app_version,
        'environment': config.environment,
        'debug': config.debug,
        'server_host': config.server_host,
        'server_port': config.server_port,
        'tax_threshold': config.tax_threshold,
        'features_enabled': config.get_feature_flags(),
        'has_openai_key': bool(config.openai_api_key),
        'has_email_config': bool(config.smtp_username and config.smtp_password),
        'has_gmail_config': bool(config.gmail_credentials_file),
    }

def validate_required_config() -> Dict[str, bool]:
    """Validate that required configuration is present"""
    validation = {
        'basic_config': True,  # Always valid with defaults
        'ai_features': bool(config.openai_api_key) if config.enable_ai_features else True,
        'email_notifications': bool(config.smtp_username and config.smtp_password) if config.enable_notifications else True,
        'gmail_integration': bool(config.gmail_credentials_file) if config.enable_gmail_integration else True,
    }
    return validation

def export_config_to_file(filepath: str, include_secrets: bool = False) -> None:
    """Export current configuration to a JSON file"""
    config_dict = config.dict()
    
    if not include_secrets:
        # Remove sensitive information
        sensitive_keys = ['openai_api_key', 'smtp_password', 'secret_key']
        for key in sensitive_keys:
            if key in config_dict:
                config_dict[key] = '***HIDDEN***' if config_dict[key] else ''
    
    with open(filepath, 'w') as f:
        json.dump(config_dict, f, indent=2, default=str)

def load_config_from_env_file(env_file_path: str) -> AppConfig:
    """Load configuration from a specific .env file"""
    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")
    
    from dotenv import load_dotenv
    load_dotenv(env_file_path, override=True)
    
    return AppConfig()

def create_default_env_file(filepath: str = ".env") -> None:
    """Create a default .env file with current configuration"""
    env_content = f"""# Snowbird Financial Assistant - Environment Variables
# Generated from current configuration

# API Keys
OPENAI_API_KEY={config.openai_api_key or ''}
GMAIL_CREDENTIALS_FILE={config.gmail_credentials_file or ''}

# Email Settings
SMTP_SERVER={config.smtp_server}
SMTP_PORT={config.smtp_port}
SMTP_USERNAME={config.smtp_username or ''}
SMTP_PASSWORD={config.smtp_password or ''}
NOTIFICATION_EMAIL={config.notification_email or ''}

# Application Settings
ENVIRONMENT={config.environment}
DEBUG={str(config.debug).lower()}
TAX_THRESHOLD={config.tax_threshold}
MAX_SEARCH_RESULTS={config.max_search_results}

# Server Configuration
SERVER_HOST={config.server_host}
SERVER_PORT={config.server_port}

# Feature Flags
ENABLE_GMAIL_INTEGRATION={str(config.enable_gmail_integration).lower()}
ENABLE_AI_FEATURES={str(config.enable_ai_features).lower()}
ENABLE_NOTIFICATIONS={str(config.enable_notifications).lower()}
ENABLE_AUTO_LOGGING={str(config.enable_auto_logging).lower()}

# Security
SECRET_KEY={config.secret_key}

# Notification Settings
DAILY_REMINDER_TIME={config.daily_reminder_time}

# Cache Settings
CACHE_TTL={config.cache_ttl}
"""
    
    with open(filepath, 'w') as f:
        f.write(env_content)

def get_config_for_component(component_name: str) -> Dict[str, Any]:
    """Get configuration specific to a component"""
    component_configs = {
        'streamlit': config.get_streamlit_config(),
        'email': config.get_email_config(),
        'features': config.get_feature_flags(),
        'api_keys': config.get_api_keys(),
    }
    
    return component_configs.get(component_name, {})

class ConfigValidator:
    """Configuration validator class"""
    
    @staticmethod
    def validate_openai_key(api_key: str) -> bool:
        """Validate OpenAI API key format"""
        return api_key.startswith('sk-') and len(api_key) > 20
    
    @staticmethod
    def validate_email_config(smtp_username: str, smtp_password: str, smtp_server: str, smtp_port: int) -> bool:
        """Validate email configuration"""
        return all([
            '@' in smtp_username,
            len(smtp_password) > 0,
            '.' in smtp_server,
            1000 <= smtp_port <= 65535
        ])
    
    @staticmethod
    def validate_gmail_credentials_file(filepath: Optional[str]) -> bool:
        """Validate Gmail credentials file exists and is valid JSON"""
        if not filepath:
            return False
        
        try:
            if not os.path.exists(filepath):
                return False
            
            with open(filepath, 'r') as f:
                credentials = json.load(f)
                # Basic validation for OAuth2 credentials structure
                return 'client_id' in str(credentials) or 'installed' in credentials
        except (json.JSONDecodeError, IOError):
            return False
    
    @classmethod
    def validate_all(cls) -> Dict[str, Any]:
        """Run all validation checks"""
        return {
            'openai_key_valid': cls.validate_openai_key(config.openai_api_key) if config.openai_api_key else None,
            'email_config_valid': cls.validate_email_config(
                config.smtp_username, config.smtp_password, 
                config.smtp_server, config.smtp_port
            ) if config.enable_notifications else None,
            'gmail_credentials_valid': cls.validate_gmail_credentials_file(
                config.gmail_credentials_file
            ) if config.enable_gmail_integration else None,
            'environment_valid': config.environment in ['development', 'staging', 'production'],
            'tax_threshold_valid': 1 <= config.tax_threshold <= 365,
            'server_port_valid': 1000 <= config.server_port <= 65535,
        }

validator = ConfigValidator()
