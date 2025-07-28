
"""
Currency conversion and inflation adjustment utilities for Snowbird Financial Assistant.

This module provides functionality to:
- Fetch real-time exchange rates from exchangerate.host API
- Convert between different currencies
- Apply inflation adjustments to financial values
- Cache exchange rates for performance
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Supported currencies
SUPPORTED_CURRENCIES = {
    "USD": {"symbol": "$", "name": "US Dollar"},
    "CAD": {"symbol": "C$", "name": "Canadian Dollar"},
    "EUR": {"symbol": "€", "name": "Euro"}
}

# Default inflation rate (3% annually)
DEFAULT_INFLATION_RATE = 0.03

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_exchange_rates(base_currency: str = "USD") -> Dict[str, float]:
    """
    Fetch current exchange rates from exchangerate.host API.
    
    Args:
        base_currency (str): Base currency code (default: USD)
        
    Returns:
        Dict[str, float]: Dictionary of currency codes to exchange rates
    """
    try:
        # Use exchangerate.host free API
        url = f"https://api.exchangerate.host/latest?base={base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("success", False):
            rates = data.get("rates", {})
            # Ensure all supported currencies are included
            filtered_rates = {
                currency: rates.get(currency, 1.0) 
                for currency in SUPPORTED_CURRENCIES.keys()
            }
            logger.info(f"Successfully fetched exchange rates for {base_currency}")
            return filtered_rates
        else:
            logger.warning("Exchange rate API returned unsuccessful response")
            return get_fallback_rates(base_currency)
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch exchange rates: {e}")
        return get_fallback_rates(base_currency)
    except Exception as e:
        logger.error(f"Unexpected error fetching exchange rates: {e}")
        return get_fallback_rates(base_currency)

def get_fallback_rates(base_currency: str = "USD") -> Dict[str, float]:
    """
    Provide fallback exchange rates when API is unavailable.
    
    Args:
        base_currency (str): Base currency code
        
    Returns:
        Dict[str, float]: Fallback exchange rates
    """
    # Approximate rates as of 2024 (fallback only)
    fallback_rates = {
        "USD": {"USD": 1.0, "CAD": 1.35, "EUR": 0.85},
        "CAD": {"USD": 0.74, "CAD": 1.0, "EUR": 0.63},
        "EUR": {"USD": 1.18, "CAD": 1.59, "EUR": 1.0}
    }
    
    return fallback_rates.get(base_currency, {"USD": 1.0, "CAD": 1.35, "EUR": 0.85})

def convert_currency(amount: float, from_currency: str, to_currency: str, 
                    exchange_rates: Optional[Dict[str, float]] = None) -> float:
    """
    Convert an amount from one currency to another.
    
    Args:
        amount (float): Amount to convert
        from_currency (str): Source currency code
        to_currency (str): Target currency code
        exchange_rates (Dict[str, float], optional): Exchange rates dict
        
    Returns:
        float: Converted amount
    """
    if from_currency == to_currency:
        return amount
        
    if exchange_rates is None:
        exchange_rates = get_exchange_rates(from_currency)
    
    # Get the rate for target currency
    rate = exchange_rates.get(to_currency, 1.0)
    converted_amount = amount * rate
    
    logger.debug(f"Converted {amount} {from_currency} to {converted_amount:.2f} {to_currency}")
    return converted_amount

def apply_inflation_adjustment(amount: float, years: float, 
                             inflation_rate: float = DEFAULT_INFLATION_RATE) -> float:
    """
    Apply compound inflation adjustment to a monetary amount.
    
    Args:
        amount (float): Original amount
        years (float): Number of years to adjust for
        inflation_rate (float): Annual inflation rate (default: 3%)
        
    Returns:
        float: Inflation-adjusted amount
    """
    if years <= 0:
        return amount
        
    # Apply compound inflation: amount * (1 + rate)^years
    adjusted_amount = amount * ((1 + inflation_rate) ** years)
    
    logger.debug(f"Applied {inflation_rate*100:.1f}% inflation over {years} years: {amount:.2f} -> {adjusted_amount:.2f}")
    return adjusted_amount

def get_current_year_progress() -> float:
    """
    Calculate progress through current year for inflation calculations.
    
    Returns:
        float: Fraction of year completed (0.0 to 1.0)
    """
    today = datetime.now()
    year_start = datetime(today.year, 1, 1)
    year_end = datetime(today.year + 1, 1, 1)
    
    year_progress = (today - year_start) / (year_end - year_start)
    return min(max(year_progress, 0.0), 1.0)

def format_currency(amount: float, currency: str, show_symbol: bool = True) -> str:
    """
    Format a monetary amount with proper currency formatting.
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        show_symbol (bool): Whether to show currency symbol
        
    Returns:
        str: Formatted currency string
    """
    currency_info = SUPPORTED_CURRENCIES.get(currency, {"symbol": "$", "name": "USD"})
    symbol = currency_info["symbol"] if show_symbol else ""
    
    # Format with appropriate decimal places and thousands separator
    if abs(amount) >= 1000:
        formatted = f"{symbol}{amount:,.0f}"
    else:
        formatted = f"{symbol}{amount:.2f}"
    
    return formatted

def get_currency_conversion_info(base_currency: str, target_currency: str) -> Tuple[float, str]:
    """
    Get exchange rate and formatted rate info for display.
    
    Args:
        base_currency (str): Base currency code
        target_currency (str): Target currency code
        
    Returns:
        Tuple[float, str]: Exchange rate and formatted rate string
    """
    if base_currency == target_currency:
        return 1.0, f"1 {base_currency} = 1 {target_currency}"
    
    rates = get_exchange_rates(base_currency)
    rate = rates.get(target_currency, 1.0)
    
    rate_info = f"1 {base_currency} = {rate:.4f} {target_currency}"
    return rate, rate_info
