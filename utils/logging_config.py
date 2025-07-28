
"""
Logging configuration for the Snowbird Financial Assistant.
Provides structured logging with different levels and handlers.
"""

import os
import sys
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from loguru import logger
import structlog
import sentry_sdk
from sentry_sdk.integrations.streamlit import StreamlitIntegration

from config import config

class SnowbirdLogger:
    """
    Custom logger for the Snowbird application with structured logging.
    """
    
    def __init__(self):
        self.setup_logging()
        self.setup_sentry()
    
    def setup_logging(self):
        """Configure loguru logger with appropriate handlers"""
        
        # Remove default handler
        logger.remove()
        
        # Console handler for development
        if config.debug or config.environment == "development":
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level="DEBUG",
                colorize=True
            )
        else:
            logger.add(
                sys.stdout,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                level="INFO"
            )
        
        # File handler for all environments
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logger.add(
            log_dir / "snowbird_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation="1 day",
            retention="30 days",
            compression="zip"
        )
        
        # Error file handler
        logger.add(
            log_dir / "snowbird_errors_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="1 day",
            retention="90 days",
            compression="zip"
        )
        
        # Add custom handler for user actions
        logger.add(
            log_dir / "snowbird_user_actions_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {extra[user_id]} | {extra[action]} | {message}",
            level="INFO",
            filter=lambda record: "user_action" in record["extra"],
            rotation="1 day",
            retention="365 days"
        )
    
    def setup_sentry(self):
        """Setup Sentry for error tracking in production"""
        sentry_dsn = os.getenv("SENTRY_DSN")
        
        if sentry_dsn and config.is_production():
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[StreamlitIntegration()],
                traces_sample_rate=0.1,
                environment=config.environment,
                release=config.app_version,
                before_send=self._filter_sentry_events
            )
            logger.info("Sentry error tracking initialized")
    
    def _filter_sentry_events(self, event, hint):
        """Filter out sensitive information from Sentry events"""
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            # Don't send certain types of expected errors
            if exc_type in [KeyboardInterrupt, SystemExit]:
                return None
        
        # Remove sensitive data
        if 'extra' in event:
            sensitive_keys = ['api_key', 'password', 'token', 'secret']
            for key in sensitive_keys:
                if key in event['extra']:
                    event['extra'][key] = '[REDACTED]'
        
        return event
    
    def log_user_action(self, user_id: str, action: str, details: Dict[str, Any] = None):
        """Log user actions for analytics and debugging"""
        logger.bind(
            user_action=True,
            user_id=user_id,
            action=action
        ).info(f"User action: {action}", extra_data=details or {})
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with full context and traceback"""
        error_context = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        logger.error(
            f"Application error: {type(error).__name__}: {str(error)}",
            **error_context
        )
    
    def log_performance(self, operation: str, duration: float, context: Dict[str, Any] = None):
        """Log performance metrics"""
        logger.info(
            f"Performance: {operation} took {duration:.3f}s",
            operation=operation,
            duration=duration,
            context=context or {}
        )

# Global logger instance
app_logger = SnowbirdLogger()

# Convenience functions
def log_user_action(user_id: str, action: str, details: Dict[str, Any] = None):
    """Log user action"""
    app_logger.log_user_action(user_id, action, details)

def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log error with context"""
    app_logger.log_error_with_context(error, context)

def log_performance(operation: str, duration: float, context: Dict[str, Any] = None):
    """Log performance metric"""
    app_logger.log_performance(operation, duration, context)

# Structured logger for data operations
data_logger = structlog.get_logger("snowbird.data")
ui_logger = structlog.get_logger("snowbird.ui")
api_logger = structlog.get_logger("snowbird.api")
