
import pytest
import sys
import os
import json
from unittest.mock import patch, mock_open

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_flags import feature_flags, is_feature_enabled, enable_feature, disable_feature


class TestFeatureFlags:
    """Test suite for the feature flags system"""
    
    def test_default_flags(self):
        """Test that default flags are set correctly"""
        assert feature_flags.is_enabled("residency_tracker") is True
        assert feature_flags.is_enabled("dual_home_budgets") is True
        assert feature_flags.is_enabled("seasonal_cash_flow") is True
        assert feature_flags.is_enabled("ai_assistant") is True
        assert feature_flags.is_enabled("reports_export") is False
        assert feature_flags.is_enabled("auto_tracker") is False
    
    def test_convenience_functions(self):
        """Test convenience functions work correctly"""
        assert is_feature_enabled("residency_tracker") is True
        assert is_feature_enabled("reports_export") is False
        assert is_feature_enabled("nonexistent_flag") is False
    
    def test_enable_disable_features(self):
        """Test enabling and disabling features"""
        # Test enabling a disabled feature
        original_state = is_feature_enabled("reports_export")
        enable_feature("reports_export", temporary=True)
        assert is_feature_enabled("reports_export") is True
        
        # Test disabling an enabled feature
        disable_feature("residency_tracker", temporary=True)
        assert is_feature_enabled("residency_tracker") is False
        
        # Clean up session overrides
        feature_flags.clear_session_overrides()
        assert is_feature_enabled("reports_export") == original_state
    
    def test_flag_sources(self):
        """Test that flag sources are detected correctly"""
        # Default source
        assert feature_flags.get_flag_source("residency_tracker") in ["file", "default"]
        
        # Test with environment variable
        with patch.dict(os.environ, {"FF_TEST_FLAG": "true"}):
            feature_flags.reload_flags()
            assert feature_flags.get_flag_source("test_flag") == "environment"
    
    def test_file_loading(self):
        """Test loading flags from file"""
        mock_file_content = json.dumps({
            "test_feature": True,
            "another_feature": False
        })
        
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            with patch("os.path.exists", return_value=True):
                feature_flags.reload_flags()
                assert feature_flags.is_enabled("test_feature") is True
                assert feature_flags.is_enabled("another_feature") is False
    
    def test_invalid_file_handling(self):
        """Test graceful handling of invalid JSON files"""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with patch("os.path.exists", return_value=True):
                # Should not raise an exception and fall back to defaults
                feature_flags.reload_flags()
                assert feature_flags.is_enabled("residency_tracker") is True
    
    def test_get_all_flags(self):
        """Test getting all flags"""
        all_flags = feature_flags.get_all_flags()
        assert isinstance(all_flags, dict)
        assert "residency_tracker" in all_flags
        assert "reports_export" in all_flags
    
    def test_session_overrides(self):
        """Test session-based temporary overrides"""
        # Enable a feature temporarily
        enable_feature("reports_export", temporary=True)
        assert is_feature_enabled("reports_export") is True
        assert feature_flags.get_flag_source("reports_export") == "session"
        
        # Clear session overrides
        feature_flags.clear_session_overrides()
        assert is_feature_enabled("reports_export") is False


if __name__ == "__main__":
    pytest.main([__file__])
