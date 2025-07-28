
"""
Feature Flags Manager for Snowbird Financial Assistant.

This module provides runtime feature toggling capabilities without requiring
application redeployment. Features can be enabled/disabled via configuration
files or environment variables.
"""

import json
import os
import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FeatureFlags:
    """
    Feature flags manager for controlling application features.
    
    Features can be controlled via:
    1. feature_flags.json file (primary)
    2. Environment variables (override)
    3. Streamlit secrets (override)
    4. Session state (temporary override)
    """
    
    _instance = None
    _flags = None
    _file_path = "feature_flags.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._flags is None:
            self.reload_flags()
    
    def reload_flags(self) -> None:
        """Reload feature flags from all sources"""
        try:
            # Start with defaults
            self._flags = self._get_default_flags()
            
            # Load from file
            file_flags = self._load_from_file()
            if file_flags:
                self._flags.update(file_flags)
            
            # Override with environment variables
            env_flags = self._load_from_env()
            self._flags.update(env_flags)
            
            # Override with Streamlit secrets
            secrets_flags = self._load_from_secrets()
            self._flags.update(secrets_flags)
            
            # Override with session state (temporary)
            session_flags = self._load_from_session()
            self._flags.update(session_flags)
            
            logger.info(f"Feature flags loaded: {len(self._flags)} flags active")
            
        except Exception as e:
            logger.error(f"Error loading feature flags: {e}")
            self._flags = self._get_default_flags()
    
    def _get_default_flags(self) -> Dict[str, bool]:
        """Get default feature flags if no configuration is available"""
        return {
            "residency_tracker": True,
            "dual_home_budgets": True,
            "seasonal_cash_flow": True,
            "ai_assistant": True,
            "reports_export": False,
            "onboarding_carousel": True,
            "pwa_support": True,
            "analytics": True,
            "auth": True,
            "admin_dashboard": True,
            "theme_customization": True,
            "auto_tracker": False,
            "gmail_integration": False,
            "notifications": False
        }
    
    def _load_from_file(self) -> Optional[Dict[str, bool]]:
        """Load feature flags from JSON file"""
        try:
            if os.path.exists(self._file_path):
                with open(self._file_path, 'r') as f:
                    flags = json.load(f)
                    # Convert string values to boolean
                    return {k: self._to_bool(v) for k, v in flags.items()}
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load feature flags from file: {e}")
        return None
    
    def _load_from_env(self) -> Dict[str, bool]:
        """Load feature flags from environment variables (FF_ prefix)"""
        flags = {}
        for key, value in os.environ.items():
            if key.startswith('FF_'):
                flag_name = key[3:].lower()  # Remove FF_ prefix
                flags[flag_name] = self._to_bool(value)
        return flags
    
    def _load_from_secrets(self) -> Dict[str, bool]:
        """Load feature flags from Streamlit secrets"""
        flags = {}
        try:
            if hasattr(st, 'secrets') and 'feature_flags' in st.secrets:
                secrets_flags = st.secrets['feature_flags']
                flags = {k: self._to_bool(v) for k, v in secrets_flags.items()}
        except Exception as e:
            logger.debug(f"No feature flags in secrets: {e}")
        return flags
    
    def _load_from_session(self) -> Dict[str, bool]:
        """Load temporary feature flag overrides from session state"""
        flags = {}
        try:
            if 'feature_flag_overrides' in st.session_state:
                flags = st.session_state.feature_flag_overrides
        except Exception:
            pass
        return flags
    
    def _to_bool(self, value: Any) -> bool:
        """Convert various value types to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
        return bool(value)
    
    def is_enabled(self, flag_name: str) -> bool:
        """
        Check if a feature flag is enabled.
        
        Args:
            flag_name (str): Name of the feature flag
            
        Returns:
            bool: True if feature is enabled, False otherwise
        """
        if self._flags is None:
            self.reload_flags()
        
        return self._flags.get(flag_name, False)
    
    def enable_flag(self, flag_name: str, temporary: bool = False) -> None:
        """
        Enable a feature flag.
        
        Args:
            flag_name (str): Name of the feature flag
            temporary (bool): If True, only enable for current session
        """
        if temporary:
            if 'feature_flag_overrides' not in st.session_state:
                st.session_state.feature_flag_overrides = {}
            st.session_state.feature_flag_overrides[flag_name] = True
        else:
            self._flags[flag_name] = True
            self._save_to_file()
    
    def disable_flag(self, flag_name: str, temporary: bool = False) -> None:
        """
        Disable a feature flag.
        
        Args:
            flag_name (str): Name of the feature flag
            temporary (bool): If True, only disable for current session
        """
        if temporary:
            if 'feature_flag_overrides' not in st.session_state:
                st.session_state.feature_flag_overrides = {}
            st.session_state.feature_flag_overrides[flag_name] = False
        else:
            self._flags[flag_name] = False
            self._save_to_file()
    
    def toggle_flag(self, flag_name: str, temporary: bool = False) -> bool:
        """
        Toggle a feature flag.
        
        Args:
            flag_name (str): Name of the feature flag
            temporary (bool): If True, only toggle for current session
            
        Returns:
            bool: New state of the flag
        """
        current_state = self.is_enabled(flag_name)
        new_state = not current_state
        
        if temporary:
            if 'feature_flag_overrides' not in st.session_state:
                st.session_state.feature_flag_overrides = {}
            st.session_state.feature_flag_overrides[flag_name] = new_state
        else:
            self._flags[flag_name] = new_state
            self._save_to_file()
        
        return new_state
    
    def _save_to_file(self) -> None:
        """Save current feature flags to JSON file"""
        try:
            # Only save non-session flags
            file_flags = {k: v for k, v in self._flags.items()}
            
            # Remove session overrides from file save
            if 'feature_flag_overrides' in st.session_state:
                for key in st.session_state.feature_flag_overrides:
                    if key in file_flags:
                        # Restore original value by reloading from file
                        original_flags = self._load_from_file() or {}
                        if key in original_flags:
                            file_flags[key] = original_flags[key]
            
            with open(self._file_path, 'w') as f:
                json.dump(file_flags, f, indent=2, sort_keys=True)
                
        except Exception as e:
            logger.error(f"Error saving feature flags: {e}")
    
    def get_all_flags(self) -> Dict[str, bool]:
        """Get all current feature flags"""
        if self._flags is None:
            self.reload_flags()
        return self._flags.copy()
    
    def get_flag_source(self, flag_name: str) -> str:
        """Get the source of a feature flag value"""
        # Check session override first
        if ('feature_flag_overrides' in st.session_state and 
            flag_name in st.session_state.feature_flag_overrides):
            return "session"
        
        # Check secrets
        try:
            if (hasattr(st, 'secrets') and 'feature_flags' in st.secrets and
                flag_name in st.secrets['feature_flags']):
                return "secrets"
        except Exception:
            pass
        
        # Check environment
        env_key = f"FF_{flag_name.upper()}"
        if env_key in os.environ:
            return "environment"
        
        # Check file
        file_flags = self._load_from_file()
        if file_flags and flag_name in file_flags:
            return "file"
        
        return "default"
    
    def clear_session_overrides(self) -> None:
        """Clear all session-based feature flag overrides"""
        if 'feature_flag_overrides' in st.session_state:
            del st.session_state.feature_flag_overrides
        self.reload_flags()


# Global instance
feature_flags = FeatureFlags()

# Convenience functions
def is_feature_enabled(flag_name: str) -> bool:
    """Check if a feature is enabled"""
    return feature_flags.is_enabled(flag_name)

def enable_feature(flag_name: str, temporary: bool = False) -> None:
    """Enable a feature"""
    feature_flags.enable_flag(flag_name, temporary)

def disable_feature(flag_name: str, temporary: bool = False) -> None:
    """Disable a feature"""
    feature_flags.disable_flag(flag_name, temporary)

def toggle_feature(flag_name: str, temporary: bool = False) -> bool:
    """Toggle a feature"""
    return feature_flags.toggle_flag(flag_name, temporary)

def require_feature(flag_name: str):
    """Decorator to require a feature flag to be enabled"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_feature_enabled(flag_name):
                st.warning(f"Feature '{flag_name}' is currently disabled.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def feature_gate(flag_name: str, enabled_content=None, disabled_content=None):
    """
    Context manager for feature gating content.
    
    Usage:
        with feature_gate("my_feature"):
            st.write("This only shows if my_feature is enabled")
    """
    class FeatureGate:
        def __init__(self, flag_name: str, enabled_content=None, disabled_content=None):
            self.flag_name = flag_name
            self.enabled_content = enabled_content
            self.disabled_content = disabled_content
            self.is_enabled = is_feature_enabled(flag_name)
        
        def __enter__(self):
            return self.is_enabled
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if not self.is_enabled and self.disabled_content:
                if callable(self.disabled_content):
                    self.disabled_content()
                else:
                    st.info(self.disabled_content)
    
    return FeatureGate(flag_name, enabled_content, disabled_content)
