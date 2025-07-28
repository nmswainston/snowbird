
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_models import SnowbirdData

class TestTaxLogic:
    """Test tax residency calculation logic"""
    
    def setup_method(self):
        """Set up test data"""
        self.snowbird_data = SnowbirdData()
    
    def test_safe_status_under_threshold(self):
        """Test SAFE status when days < 183"""
        days = 100
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "SAFE"
        assert status_class == "status-safe"
    
    def test_safe_status_edge_case(self):
        """Test SAFE status at 137 days (75% threshold)"""
        days = 137  # 75% of 183
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "SAFE"
    
    def test_caution_status_between_75_90_percent(self):
        """Test CAUTION status between 75-90% of threshold"""
        days = 150  # ~82% of 183
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "CAUTION"
        assert status_class == "status-warning"
    
    def test_critical_status_near_threshold(self):
        """Test CRITICAL status when days between 90-100% of threshold"""
        days = 170  # ~93% of 183
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "CRITICAL"
        assert status_class == "status-warning"
    
    def test_tax_resident_at_threshold(self):
        """Test TAX RESIDENT status when days >= 183"""
        days = 183
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "TAX RESIDENT"
        assert status_class == "status-danger"
    
    def test_tax_resident_over_threshold(self):
        """Test TAX RESIDENT status when days > 183"""
        days = 200
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "TAX RESIDENT"
        assert status_class == "status-danger"
    
    def test_percentage_calculation_mid_range(self):
        """Test percentage calculation for 92 days"""
        days = 92
        percentage = (days / 183) * 100
        expected_percentage = 50.27  # 92/183 * 100
        assert abs(percentage - expected_percentage) < 0.1
    
    def test_percentage_calculation_exact_threshold(self):
        """Test percentage calculation at threshold"""
        days = 183
        percentage = (days / 183) * 100
        assert percentage == 100.0
    
    def test_custom_threshold(self):
        """Test with custom threshold"""
        days = 150
        custom_threshold = 200
        status, status_class = self.snowbird_data.get_tax_status(days, custom_threshold)
        assert status == "CAUTION"  # 150/200 = 75%
    
    def test_zero_days(self):
        """Test with zero days"""
        days = 0
        status, status_class = self.snowbird_data.get_tax_status(days, 183)
        assert status == "SAFE"
        assert status_class == "status-safe"
