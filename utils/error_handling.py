
"""
Error handling utilities for the Snowbird Financial Assistant.
Provides decorators and context managers for robust error handling.
"""

import functools
import time
import traceback
import sys
from typing import Callable, Any, Optional, Dict, Union
from contextlib import contextmanager

import streamlit as st
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from utils.logging_config import log_error, log_performance

class SnowbirdError(Exception):
    """Base exception class for Snowbird application errors"""
    pass

class ConfigurationError(SnowbirdError):
    """Raised when there's a configuration issue"""
    pass

class DataValidationError(SnowbirdError):
    """Raised when data validation fails"""
    pass

class APIError(SnowbirdError):
    """Raised when external API calls fail"""
    pass

class EmailError(SnowbirdError):
    """Raised when email operations fail"""
    pass

def handle_errors(
    show_error: bool = True,
    fallback_message: str = "An error occurred. Please try again.",
    log_error_details: bool = True,
    return_none_on_error: bool = False
):
    """
    Decorator for handling errors in Streamlit functions.
    
    Args:
        show_error: Whether to show error message in Streamlit UI
        fallback_message: Message to show to user if error occurs
        log_error_details: Whether to log full error details
        return_none_on_error: Whether to return None on error instead of raising
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                
                # Log performance
                duration = time.time() - start_time
                if duration > 1.0:  # Only log slow operations
                    log_performance(func.__name__, duration, {
                        'args_count': len(args),
                        'kwargs_keys': list(kwargs.keys())
                    })
                
                return result
                
            except Exception as e:
                if log_error_details:
                    log_error(e, {
                        'function': func.__name__,
                        'args': str(args)[:200] if args else None,
                        'kwargs': str(kwargs)[:200] if kwargs else None
                    })
                
                if show_error:
                    if isinstance(e, SnowbirdError):
                        st.error(f"❌ {str(e)}")
                    elif isinstance(e, (ConnectionError, TimeoutError)):
                        st.error("🌐 Connection issue. Please check your internet connection and try again.")
                    elif isinstance(e, PermissionError):
                        st.error("🔒 Permission denied. Please check your API keys and permissions.")
                    else:
                        st.error(f"⚠️ {fallback_message}")
                        if st.session_state.get('debug_mode', False):
                            st.exception(e)
                
                if return_none_on_error:
                    return None
                else:
                    raise
        
        return wrapper
    return decorator

def safe_operation(operation_name: str = "Operation"):
    """
    Decorator for operations that should not crash the app.
    Shows user-friendly error messages and logs details.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{operation_name} failed: {str(e)}", 
                           function=func.__name__, 
                           error=str(e),
                           traceback=traceback.format_exc())
                
                st.error(f"❌ {operation_name} failed. The error has been logged.")
                if st.session_state.get('debug_mode', False):
                    with st.expander("Debug Information"):
                        st.code(traceback.format_exc())
                
                return None
        return wrapper
    return decorator

@contextmanager
def error_boundary(operation_name: str = "Operation", show_spinner: bool = True):
    """
    Context manager for error handling with optional spinner.
    
    Usage:
        with error_boundary("Loading data", show_spinner=True):
            # risky operation
            data = load_data()
    """
    spinner_context = st.spinner(f"{operation_name}...") if show_spinner else None
    
    try:
        if spinner_context:
            spinner_context.__enter__()
        
        start_time = time.time()
        yield
        
        # Log successful operations that take a while
        duration = time.time() - start_time
        if duration > 2.0:
            logger.info(f"{operation_name} completed successfully in {duration:.2f}s")
            
    except Exception as e:
        log_error(e, {'operation': operation_name})
        
        if isinstance(e, SnowbirdError):
            st.error(f"❌ {operation_name} failed: {str(e)}")
        else:
            st.error(f"❌ {operation_name} failed unexpectedly. Please try again.")
            if st.session_state.get('debug_mode', False):
                st.exception(e)
        
        raise
    
    finally:
        if spinner_context:
            spinner_context.__exit__(None, None, None)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
def retry_on_failure(func: Callable, *args, **kwargs):
    """
    Retry a function on network-related failures.
    """
    return func(*args, **kwargs)

def validate_data(data: Any, validation_rules: Dict[str, Any], operation_name: str = "Data validation") -> bool:
    """
    Validate data against rules and raise DataValidationError if invalid.
    
    Args:
        data: Data to validate
        validation_rules: Dictionary of validation rules
        operation_name: Name of the operation for error messages
    
    Returns:
        True if validation passes
    
    Raises:
        DataValidationError: If validation fails
    """
    try:
        if 'required_fields' in validation_rules:
            if isinstance(data, dict):
                for field in validation_rules['required_fields']:
                    if field not in data or data[field] is None:
                        raise DataValidationError(f"Required field '{field}' is missing or None")
        
        if 'type_check' in validation_rules:
            expected_type = validation_rules['type_check']
            if not isinstance(data, expected_type):
                raise DataValidationError(f"Expected type {expected_type.__name__}, got {type(data).__name__}")
        
        if 'min_length' in validation_rules:
            if hasattr(data, '__len__') and len(data) < validation_rules['min_length']:
                raise DataValidationError(f"Data length {len(data)} is below minimum {validation_rules['min_length']}")
        
        if 'max_length' in validation_rules:
            if hasattr(data, '__len__') and len(data) > validation_rules['max_length']:
                raise DataValidationError(f"Data length {len(data)} exceeds maximum {validation_rules['max_length']}")
        
        if 'range_check' in validation_rules:
            min_val, max_val = validation_rules['range_check']
            if isinstance(data, (int, float)) and not (min_val <= data <= max_val):
                raise DataValidationError(f"Value {data} is outside allowed range [{min_val}, {max_val}]")
        
        return True
        
    except Exception as e:
        log_error(e, {
            'operation': operation_name,
            'data_type': type(data).__name__,
            'validation_rules': validation_rules
        })
        raise

def graceful_degradation(fallback_value: Any = None, message: str = None):
    """
    Decorator for graceful degradation - return fallback value instead of crashing.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Function {func.__name__} failed, using fallback", 
                             error=str(e), fallback=fallback_value)
                
                if message:
                    st.warning(message)
                
                return fallback_value
        return wrapper
    return decorator

def get_error_context() -> Dict[str, Any]:
    """Get current application context for error reporting"""
    context = {
        'timestamp': time.time(),
        'session_state_keys': list(st.session_state.keys()) if hasattr(st, 'session_state') else [],
    }
    
    # Add user context if available
    if hasattr(st, 'session_state'):
        context.update({
            'user_email': st.session_state.get('user_email'),
            'states_logged': st.session_state.get('states', {}),
            'day_log_count': len(st.session_state.get('day_log', [])),
        })
    
    return context

def initialize_error_monitoring():
    """Initialize Sentry error monitoring if available"""
    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        sentry_dsn = os.getenv('SENTRY_DSN')
        if sentry_dsn:
            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[sentry_logging],
                traces_sample_rate=0.1,
                environment=os.getenv('ENVIRONMENT', 'development')
            )
            logger.info("Sentry error monitoring initialized")
    except ImportError:
        logger.info("Sentry not available, using local error logging")

def render_error_banner(error_type: str, message: str, show_details: bool = False):
    """Render user-friendly error banner"""
    error_configs = {
        'network': {
            'icon': '🌐',
            'title': 'Connection Issue',
            'color': 'orange',
            'suggestions': [
                'Check your internet connection',
                'Refresh the page',
                'Try again in a few moments'
            ]
        },
        'validation': {
            'icon': '⚠️',
            'title': 'Input Error',
            'color': 'yellow',
            'suggestions': [
                'Check your input data',
                'Ensure all required fields are filled',
                'Verify date formats and numbers'
            ]
        },
        'server': {
            'icon': '🔧',
            'title': 'Server Error',
            'color': 'red',
            'suggestions': [
                'This error has been automatically reported',
                'Please try refreshing the page',
                'Contact support if the issue persists'
            ]
        },
        'permission': {
            'icon': '🔒',
            'title': 'Permission Error',
            'color': 'red',
            'suggestions': [
                'Check your API keys and credentials',
                'Verify your account permissions',
                'Contact support for assistance'
            ]
        }
    }
    
    config = error_configs.get(error_type, error_configs['server'])
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(238, 90, 90, 0.3);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{config['icon']}</span>
            <strong style="font-size: 1.1rem;">{config['title']}</strong>
        </div>
        <p style="margin: 0.5rem 0;">{message}</p>
        <details style="margin-top: 1rem;">
            <summary style="cursor: pointer; font-weight: bold;">💡 What you can do:</summary>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                {''.join(f'<li>{suggestion}</li>' for suggestion in config['suggestions'])}
            </ul>
        </details>
    </div>
    """, unsafe_allow_html=True)

class ErrorDisplay:
    """Utility class for displaying different types of errors to users"""
    
    @staticmethod
    def configuration_error(error: ConfigurationError):
        st.error("⚙️ Configuration Error")
        st.write(f"**Issue:** {str(error)}")
        st.info("💡 **What you can do:**")
        st.write("1. Check your environment variables")
        st.write("2. Verify API keys are correctly set")
        st.write("3. Contact support if the issue persists")
    
    @staticmethod
    def api_error(error: APIError, service_name: str = "External service"):
        st.error(f"🌐 {service_name} Error")
        st.write(f"**Issue:** {str(error)}")
        st.info("💡 **What you can do:**")
        st.write("1. Check your internet connection")
        st.write("2. Verify your API keys")
        st.write("3. Try again in a few moments")
    
    @staticmethod
    def data_error(error: DataValidationError):
        st.error("📊 Data Validation Error")
        st.write(f"**Issue:** {str(error)}")
        st.info("💡 **What you can do:**")
        st.write("1. Check your input data")
        st.write("2. Ensure all required fields are filled")
        st.write("3. Contact support if you believe this is an error")
    
    @staticmethod
    def generic_error(error: Exception, show_details: bool = False):
        st.error("⚠️ Unexpected Error")
        st.write("An unexpected error occurred. The development team has been notified.")
        
        if show_details:
            with st.expander("Technical Details"):
                st.code(f"""
Error Type: {type(error).__name__}
Error Message: {str(error)}
Traceback:
{traceback.format_exc()}
                """)
