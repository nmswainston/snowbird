
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import re

class DataValidator:
    """Comprehensive data validation for Snowbird app"""
    
    @staticmethod
    def validate_state_name(state: str) -> bool:
        """Validate US state name"""
        valid_states = {
            'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
            'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho',
            'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
            'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
            'mississippi', 'missouri', 'montana', 'nebraska', 'nevada',
            'new hampshire', 'new jersey', 'new mexico', 'new york',
            'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon',
            'pennsylvania', 'rhode island', 'south carolina', 'south dakota',
            'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
            'west virginia', 'wisconsin', 'wyoming', 'district of columbia'
        }
        return state.lower().strip() in valid_states
    
    @staticmethod
    def validate_day_count(days: int, max_days: int = 365) -> bool:
        """Validate day count is reasonable"""
        return 0 <= days <= max_days
    
    @staticmethod
    def validate_budget_amount(amount: float) -> bool:
        """Validate budget amount is reasonable"""
        return 0 <= amount <= 1000000  # Up to $1M
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """Validate date range is logical"""
        return start_date <= end_date <= date.today()
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()[:1000]  # Limit length

# Global validator instance
validator = DataValidator()
