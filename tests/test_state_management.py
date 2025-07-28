
import pytest
import sys
import os
import datetime
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_models import SnowbirdData

class TestStateManagement:
    """Test state tracking and management utilities"""
    
    def setup_method(self):
        """Set up test data"""
        self.snowbird_data = SnowbirdData()
    
    @patch('streamlit.session_state')
    def test_log_day_increments_correct_state(self, mock_session_state):
        """Test that logging a day increments the correct state count"""
        # Mock session state
        mock_session_state.states = {"Arizona": 5, "Minnesota": 10}
        mock_session_state.day_log = []
        
        # Test logging Arizona
        success, message = self.snowbird_data.add_day_log("Arizona", "2024-01-15")
        
        assert success is True
        assert "Arizona" in message
        assert len(mock_session_state.day_log) == 1
        assert mock_session_state.day_log[0]['state'] == "Arizona"
        assert mock_session_state.day_log[0]['date'] == "2024-01-15"
        assert mock_session_state.states["Arizona"] == 6
    
    @patch('streamlit.session_state')
    def test_log_day_minnesota(self, mock_session_state):
        """Test logging a day in Minnesota"""
        mock_session_state.states = {"Arizona": 5, "Minnesota": 10}
        mock_session_state.day_log = []
        
        success, message = self.snowbird_data.add_day_log("Minnesota", "2024-01-16")
        
        assert success is True
        assert "Minnesota" in message
        assert mock_session_state.states["Minnesota"] == 11
        assert mock_session_state.states["Arizona"] == 5  # Should remain unchanged
    
    @patch('streamlit.session_state')
    def test_initial_state_is_zero(self, mock_session_state):
        """Test that initial state counts are zero"""
        mock_session_state.states = {"Arizona": 0, "Minnesota": 0}
        mock_session_state.day_log = []
        
        assert mock_session_state.states["Arizona"] == 0
        assert mock_session_state.states["Minnesota"] == 0
        assert len(mock_session_state.day_log) == 0
    
    @patch('streamlit.session_state')
    def test_duplicate_date_logging_fails(self, mock_session_state):
        """Test that logging the same date twice fails"""
        mock_session_state.states = {"Arizona": 0, "Minnesota": 0}
        mock_session_state.day_log = [
            {'date': '2024-01-15', 'state': 'Arizona', 'timestamp': '2024-01-15T10:00:00'}
        ]
        
        success, message = self.snowbird_data.add_day_log("Minnesota", "2024-01-15")
        
        assert success is False
        assert "Already logged" in message
        assert "Arizona" in message  # Should mention the existing state
    
    @patch('streamlit.session_state')
    def test_auto_logged_flag(self, mock_session_state):
        """Test auto-logged flag is properly set"""
        mock_session_state.states = {"Arizona": 0, "Minnesota": 0}
        mock_session_state.day_log = []
        
        success, message = self.snowbird_data.add_day_log("Arizona", "2024-01-15", auto_logged=True)
        
        assert success is True
        assert "(auto)" in message
        assert mock_session_state.day_log[0]['auto_logged'] is True
    
    @patch('streamlit.session_state')
    def test_default_date_is_today(self, mock_session_state):
        """Test that default date is today when none provided"""
        mock_session_state.states = {"Arizona": 0, "Minnesota": 0}
        mock_session_state.day_log = []
        
        today = datetime.date.today().isoformat()
        
        success, message = self.snowbird_data.add_day_log("Arizona")
        
        assert success is True
        assert mock_session_state.day_log[0]['date'] == today
    
    def test_generate_report_data_structure(self):
        """Test report data generation structure"""
        with patch('streamlit.session_state') as mock_session_state:
            mock_session_state.states = {"Arizona": 50, "Minnesota": 30}
            mock_session_state.day_log = [
                {'date': '2024-01-15', 'state': 'Arizona'},
                {'date': '2024-02-10', 'state': 'Minnesota'},
                {'date': '2024-01-20', 'state': 'Arizona'}
            ]
            mock_session_state.tax_threshold = 183
            
            report_data = self.snowbird_data.generate_report_data()
            
            assert 'year' in report_data
            assert 'total_days' in report_data
            assert 'monthly_breakdown' in report_data
            assert 'threshold' in report_data
            assert 'generated_date' in report_data
            
            assert report_data['total_days'] == {"Arizona": 50, "Minnesota": 30}
            assert report_data['threshold'] == 183
    
    def test_generate_report_monthly_breakdown(self):
        """Test monthly breakdown in report data"""
        with patch('streamlit.session_state') as mock_session_state:
            mock_session_state.states = {"Arizona": 3, "Minnesota": 2}
            mock_session_state.day_log = [
                {'date': '2024-01-15', 'state': 'Arizona'},
                {'date': '2024-01-20', 'state': 'Arizona'},
                {'date': '2024-02-10', 'state': 'Minnesota'},
                {'date': '2024-02-15', 'state': 'Minnesota'},
                {'date': '2024-01-25', 'state': 'Arizona'}
            ]
            mock_session_state.tax_threshold = 183
            
            report_data = self.snowbird_data.generate_report_data()
            
            monthly = report_data['monthly_breakdown']
            assert '2024-01' in monthly
            assert '2024-02' in monthly
            assert monthly['2024-01']['Arizona'] == 3
            assert monthly['2024-02']['Minnesota'] == 2
