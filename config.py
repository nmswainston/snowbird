import os
from typing import Dict, Any, List, Optional
from pydantic import BaseSettings, Field, validator, EmailStr
from pydantic_settings import BaseSettings as PydanticBaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig(PydanticBaseSettings):
    """
    Application configuration using Pydantic BaseSettings.
    Automatically loads from environment variables and validates types.
    """

    # API Keys
    openai_api_key: Optional[str] = Field(
        default="",
        description="OpenAI API key for AI features",
        env="OPENAI_API_KEY"
    )

    # Gmail API Configuration
    gmail_scopes: List[str] = Field(
        default=['https://www.googleapis.com/auth/gmail.readonly'],
        description="Gmail API scopes"
    )

    gmail_credentials_file: Optional[str] = Field(
        default=None,
        description="Path to Gmail credentials JSON file",
        env="GMAIL_CREDENTIALS_FILE"
    )

    # Email Settings
    smtp_server: str = Field(
        default="smtp.gmail.com",
        description="SMTP server for sending emails",
        env="SMTP_SERVER"
    )

    smtp_port: int = Field(
        default=587,
        description="SMTP server port",
        env="SMTP_PORT"
    )

    smtp_username: Optional[str] = Field(
        default="",
        description="SMTP username",
        env="SMTP_USERNAME"
    )

    smtp_password: Optional[str] = Field(
        default="",
        description="SMTP password",
        env="SMTP_PASSWORD"
    )

    # App Settings
    tax_threshold: int = Field(
        default=183,
        ge=1,
        le=365,
        description="Tax residency threshold in days",
        env="TAX_THRESHOLD"
    )

    max_search_results: int = Field(
        default=50,
        ge=10,
        le=500,
        description="Maximum Gmail search results",
        env="MAX_SEARCH_RESULTS"
    )

    # Application Settings
    app_name: str = Field(
        default="Snowbird Financial Assistant",
        description="Application name"
    )

    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )

    environment: str = Field(
        default="development",
        description="Application environment",
        env="ENVIRONMENT"
    )

    debug: bool = Field(
        default=False,
        description="Debug mode",
        env="DEBUG"
    )

    # Server Settings
    server_host: str = Field(
        default="0.0.0.0",
        description="Server host",
        env="SERVER_HOST"
    )

    server_port: int = Field(
        default=5000,
        ge=1000,
        le=65535,
        description="Server port",
        env="SERVER_PORT"
    )

    # Feature Flags
    enable_gmail_integration: bool = Field(
        default=True,
        description="Enable Gmail integration features",
        env="ENABLE_GMAIL_INTEGRATION"
    )

    enable_ai_features: bool = Field(
        default=True,
        description="Enable AI-powered features",
        env="ENABLE_AI_FEATURES"
    )

    enable_notifications: bool = Field(
        default=True,
        description="Enable notification system",
        env="ENABLE_NOTIFICATIONS"
    )

    enable_auto_logging: bool = Field(
        default=False,
        description="Enable automatic location logging",
        env="ENABLE_AUTO_LOGGING"
    )

    # Security Settings
    secret_key: str = Field(
        default="snowbird-secret-key-change-in-production",
        description="Secret key for security features",
        env="SECRET_KEY"
    )

    # Notification Settings
    notification_email: Optional[EmailStr] = Field(
        default=None,
        description="Default notification email address",
        env="NOTIFICATION_EMAIL"
    )

    daily_reminder_time: str = Field(
        default="09:00",
        description="Daily reminder time (HH:MM format)",
        env="DAILY_REMINDER_TIME"
    )

    # Database Settings (for future use)
    database_url: Optional[str] = Field(
        default=None,
        description="Database connection URL",
        env="DATABASE_URL"
    )

    # Cache Settings
    cache_ttl: int = Field(
        default=3600,
        ge=60,
        description="Cache TTL in seconds",
        env="CACHE_TTL"
    )

    # Error Monitoring Settings
    sentry_dsn: Optional[str] = Field(
        default=None,
        description="Sentry DSN for error tracking",
        env="SENTRY_DSN"
    )

    log_level: str = Field(
        default="INFO",
        description="Logging level",
        env="LOG_LEVEL"
    )

    enable_performance_monitoring: bool = Field(
        default=True,
        description="Enable performance monitoring",
        env="ENABLE_PERFORMANCE_MONITORING"
    )

    error_notification_email: Optional[EmailStr] = Field(
        default=None,
        description="Email for critical error notifications",
        env="ERROR_NOTIFICATION_EMAIL"
    )

    @validator('environment')
    def validate_environment(cls, v):
        allowed_envs = ['development', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'Environment must be one of: {allowed_envs}')
        return v

    @validator('daily_reminder_time')
    def validate_time_format(cls, v):
        try:
            hours, minutes = map(int, v.split(':'))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError('Invalid time format')
            return v
        except (ValueError, IndexError):
            raise ValueError('Time must be in HH:MM format (24-hour)')

    @validator('openai_api_key')
    def validate_openai_key(cls, v, values):
        if values.get('enable_ai_features', True) and not v:
            # Don't raise error, just warn - let app handle gracefully
            pass
        return v

    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit-specific configuration"""
        return {
            'server.port': self.server_port,
            'server.address': self.server_host,
            'browser.gatherUsageStats': False,
            'theme.base': 'light',
            'theme.primaryColor': '#12BDF2',
            'theme.backgroundColor': '#FFFFFF',
            'theme.secondaryBackgroundColor': '#F0F4F8',
            'theme.textColor': '#1E293B'
        }

    def get_email_config(self) -> Dict[str, Any]:
        """Get email configuration"""
        return {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'smtp_username': self.smtp_username,
            'smtp_password': self.smtp_password,
            'enabled': bool(self.smtp_username and self.smtp_password)
        }

    def get_feature_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return {
            'gmail_integration': self.enable_gmail_integration,
            'ai_features': self.enable_ai_features and bool(self.openai_api_key),
            'notifications': self.enable_notifications,
            'auto_logging': self.enable_auto_logging,
        }

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == "development"

    def get_api_keys(self) -> Dict[str, Optional[str]]:
        """Get all API keys (excluding passwords)"""
        return {
            'openai': self.openai_api_key,
            'gmail_credentials_file': self.gmail_credentials_file,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        extra = "ignore"  # Ignore extra environment variables

# Global configuration instance
config = AppConfig()

# Legacy compatibility - keep old interface working
class Config:
    """Legacy Config class for backward compatibility"""

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary (legacy method)"""
        return {
            'openai_api_key': config.openai_api_key,
            'gmail_scopes': config.gmail_scopes,
            'smtp_server': config.smtp_server,
            'smtp_port': config.smtp_port,
            'smtp_username': config.smtp_username,
            'smtp_password': config.smtp_password,
            'tax_threshold': config.tax_threshold,
            'max_search_results': config.max_search_results,
            'enable_gmail': config.enable_gmail_integration,
            'enable_ai': config.enable_ai_features,
            'enable_notifications': config.enable_notifications
        }

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production (legacy method)"""
        return config.is_production()

# Export commonly used attributes for easy access
OPENAI_API_KEY = config.openai_api_key
TAX_THRESHOLD = config.tax_threshold
ENABLE_AI_FEATURES = config.enable_ai_features
ENABLE_GMAIL_INTEGRATION = config.enable_gmail_integration
ENABLE_NOTIFICATIONS = config.enable_notifications