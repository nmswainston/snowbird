
import streamlit as st
from utils.currency import convert_currency, apply_inflation_adjustment, format_currency, get_exchange_rates
from utils.logging_config import data_logger
import datetime
from typing import Dict, Any, Union


def convert_budget_value(amount: float, apply_inflation: bool = None, target_currency: str = None) -> float:
    """
    Convert a budget amount based on current currency and inflation settings.
    
    Args:
        amount (float): Original amount in USD
        apply_inflation (bool, optional): Whether to apply inflation. Uses session state if None.
        target_currency (str, optional): Target currency. Uses session state if None.
        
    Returns:
        float: Converted and adjusted amount
    """
    if apply_inflation is None:
        apply_inflation = st.session_state.get('inflation_enabled', False)
    
    if target_currency is None:
        target_currency = st.session_state.get('primary_currency', 'USD')
    
    try:
        # Step 1: Convert currency if needed
        converted_amount = amount
        if target_currency != 'USD':
            exchange_rates = get_exchange_rates('USD')
            converted_amount = convert_currency(amount, 'USD', target_currency, exchange_rates)
        
        # Step 2: Apply inflation adjustment if enabled
        if apply_inflation:
            inflation_rate = st.session_state.get('inflation_rate', 0.03)
            # Apply inflation for current year progress (partial year adjustment)
            from utils.currency import get_current_year_progress
            year_progress = get_current_year_progress()
            converted_amount = apply_inflation_adjustment(converted_amount, year_progress, inflation_rate)
        
        data_logger.debug(f"Converted budget: {amount} USD -> {converted_amount} {target_currency}")
        return converted_amount
        
    except Exception as e:
        data_logger.error(f"Budget conversion error: {e}")
        return amount  # Return original amount if conversion fails


def convert_budget_dict(budget_dict: Dict[str, Union[int, float]], 
                       apply_inflation: bool = None, 
                       target_currency: str = None) -> Dict[str, float]:
    """
    Convert all values in a budget dictionary.
    
    Args:
        budget_dict (Dict[str, Union[int, float]]): Budget dictionary with category: amount pairs
        apply_inflation (bool, optional): Whether to apply inflation
        target_currency (str, optional): Target currency
        
    Returns:
        Dict[str, float]: Converted budget dictionary
    """
    converted_budget = {}
    
    for category, amount in budget_dict.items():
        converted_budget[category] = convert_budget_value(
            float(amount), 
            apply_inflation, 
            target_currency
        )
    
    return converted_budget


def format_budget_value(amount: float, show_currency: bool = True, target_currency: str = None) -> str:
    """
    Format a budget value with appropriate currency formatting.
    
    Args:
        amount (float): Amount to format
        show_currency (bool): Whether to show currency symbol
        target_currency (str, optional): Currency code. Uses session state if None.
        
    Returns:
        str: Formatted currency string
    """
    if target_currency is None:
        target_currency = st.session_state.get('primary_currency', 'USD')
    
    return format_currency(amount, target_currency, show_currency)


def display_budget_comparison(original_amount: float, category: str = "Budget Item") -> None:
    """
    Display a comparison showing original vs converted budget amounts.
    
    Args:
        original_amount (float): Original amount in USD
        category (str): Category name for display
    """
    target_currency = st.session_state.get('primary_currency', 'USD')
    inflation_enabled = st.session_state.get('inflation_enabled', False)
    
    # Calculate converted amount
    converted_amount = convert_budget_value(original_amount)
    
    # Display comparison if currency or inflation is applied
    if target_currency != 'USD' or inflation_enabled:
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(f"Original ({category})")
            st.write(f"💵 ${original_amount:,.2f} USD")
        
        with col2:
            adjustments = []
            if target_currency != 'USD':
                adjustments.append(f"→ {target_currency}")
            if inflation_enabled:
                rate = st.session_state.get('inflation_rate_percent', 3.0)
                adjustments.append(f"+ {rate:.1f}% inflation")
            
            st.caption(f"Adjusted ({' '.join(adjustments)})")
            st.write(f"💰 {format_budget_value(converted_amount)}")
            
            # Show percentage change
            if original_amount > 0:
                change_percent = ((converted_amount - original_amount) / original_amount) * 100
                if abs(change_percent) > 0.1:  # Only show if meaningful change
                    st.caption(f"📈 {change_percent:+.1f}% change")


def get_conversion_status() -> Dict[str, Any]:
    """
    Get current conversion settings status for display.
    
    Returns:
        Dict[str, Any]: Status information about current conversion settings
    """
    target_currency = st.session_state.get('primary_currency', 'USD')
    inflation_enabled = st.session_state.get('inflation_enabled', False)
    inflation_rate = st.session_state.get('inflation_rate_percent', 3.0)
    
    status = {
        'currency_conversion_active': target_currency != 'USD',
        'inflation_adjustment_active': inflation_enabled,
        'target_currency': target_currency,
        'inflation_rate_percent': inflation_rate,
        'has_adjustments': target_currency != 'USD' or inflation_enabled
    }
    
    return status


def display_conversion_banner() -> None:
    """
    Display a banner showing current conversion settings.
    """
    status = get_conversion_status()
    
    if status['has_adjustments']:
        banner_parts = []
        
        if status['currency_conversion_active']:
            banner_parts.append(f"💱 Currency: {status['target_currency']}")
        
        if status['inflation_adjustment_active']:
            banner_parts.append(f"📈 Inflation: {status['inflation_rate_percent']:.1f}%/year")
        
        banner_text = " | ".join(banner_parts)
        
        st.info(f"🔧 **Active Adjustments:** {banner_text}")
