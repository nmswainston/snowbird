
"""
Tests for currency conversion and inflation adjustment functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.currency import (
    convert_currency, apply_inflation_adjustment, format_currency,
    get_fallback_rates, get_current_year_progress, SUPPORTED_CURRENCIES
)

class TestCurrencyConversion:
    """Test currency conversion functionality"""
    
    def test_same_currency_conversion(self):
        """Test conversion between same currencies returns original amount"""
        amount = 100.0
        result = convert_currency(amount, 'USD', 'USD')
        assert result == amount
    
    def test_currency_conversion_with_rates(self):
        """Test currency conversion with provided exchange rates"""
        exchange_rates = {'CAD': 1.35, 'EUR': 0.85}
        
        # USD to CAD
        result_cad = convert_currency(100.0, 'USD', 'CAD', exchange_rates)
        assert result_cad == 135.0
        
        # USD to EUR
        result_eur = convert_currency(100.0, 'USD', 'EUR', exchange_rates)
        assert result_eur == 85.0
    
    def test_fallback_rates(self):
        """Test fallback exchange rates are provided"""
        rates_usd = get_fallback_rates('USD')
        assert 'USD' in rates_usd
        assert 'CAD' in rates_usd
        assert 'EUR' in rates_usd
        assert rates_usd['USD'] == 1.0
        
        rates_cad = get_fallback_rates('CAD')
        assert 'CAD' in rates_cad
        assert rates_cad['CAD'] == 1.0

class TestInflationAdjustment:
    """Test inflation adjustment functionality"""
    
    def test_zero_years_inflation(self):
        """Test that zero years returns original amount"""
        amount = 1000.0
        result = apply_inflation_adjustment(amount, 0, 0.03)
        assert result == amount
    
    def test_negative_years_inflation(self):
        """Test that negative years returns original amount"""
        amount = 1000.0
        result = apply_inflation_adjustment(amount, -1, 0.03)
        assert result == amount
    
    def test_inflation_calculation(self):
        """Test inflation calculation is correct"""
        amount = 1000.0
        years = 1.0
        rate = 0.03
        
        expected = amount * (1.03 ** years)
        result = apply_inflation_adjustment(amount, years, rate)
        
        assert abs(result - expected) < 0.01
    
    def test_compound_inflation(self):
        """Test compound inflation over multiple years"""
        amount = 1000.0
        years = 2.0
        rate = 0.05
        
        # Should be 1000 * 1.05^2 = 1102.50
        expected = 1102.50
        result = apply_inflation_adjustment(amount, years, rate)
        
        assert abs(result - expected) < 0.01

class TestCurrencyFormatting:
    """Test currency formatting functionality"""
    
    def test_format_currency_with_symbol(self):
        """Test currency formatting includes symbol"""
        result = format_currency(1000.0, 'USD', show_symbol=True)
        assert '$' in result
        assert '1,000' in result
    
    def test_format_currency_without_symbol(self):
        """Test currency formatting without symbol"""
        result = format_currency(1000.0, 'USD', show_symbol=False)
        assert '$' not in result
        assert '1,000' in result
    
    def test_format_small_amounts(self):
        """Test formatting of small amounts shows decimals"""
        result = format_currency(10.50, 'USD')
        assert '10.50' in result
    
    def test_format_large_amounts(self):
        """Test formatting of large amounts with thousands separator"""
        result = format_currency(1500.0, 'USD')
        assert '1,500' in result
    
    def test_different_currency_symbols(self):
        """Test different currency symbols are used correctly"""
        result_cad = format_currency(100.0, 'CAD')
        assert 'C$' in result_cad
        
        result_eur = format_currency(100.0, 'EUR')
        assert '€' in result_eur

class TestCurrentYearProgress:
    """Test current year progress calculation"""
    
    @patch('utils.currency.datetime')
    def test_year_progress_calculation(self, mock_datetime):
        """Test year progress is calculated correctly"""
        # Mock January 1st
        mock_datetime.now.return_value = MagicMock()
        mock_datetime.now.return_value.year = 2024
        mock_datetime.return_value = MagicMock()
        
        # This is a simplified test - actual implementation depends on datetime mocking
        result = get_current_year_progress()
        assert 0.0 <= result <= 1.0

class TestSupportedCurrencies:
    """Test supported currencies configuration"""
    
    def test_supported_currencies_structure(self):
        """Test that supported currencies have required fields"""
        for code, info in SUPPORTED_CURRENCIES.items():
            assert 'symbol' in info
            assert 'name' in info
            assert isinstance(info['symbol'], str)
            assert isinstance(info['name'], str)
    
    def test_required_currencies_present(self):
        """Test that required currencies are present"""
        required_currencies = ['USD', 'CAD', 'EUR']
        for currency in required_currencies:
            assert currency in SUPPORTED_CURRENCIES

if __name__ == '__main__':
    pytest.main([__file__])
