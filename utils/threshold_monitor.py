
"""
Tax threshold monitoring and calendar reminder system.
"""

import streamlit as st
import datetime
from typing import Dict, List
from utils.google_calendar import calendar_sync
from utils.logging_config import logger

class ThresholdMonitor:
    """Monitor tax residency thresholds and create calendar reminders"""
    
    def __init__(self):
        self.tax_threshold = 183  # Default threshold
        
    def check_thresholds(self) -> List[Dict]:
        """
        Check current state day counts against thresholds.
        
        Returns:
            List of threshold warnings with details
        """
        from utils.data_models import SnowbirdData
        warnings = []
        snowbird_data = SnowbirdData()
        
        # Get current state counts
        states = st.session_state.get('states', {})
        
        for state, days in states.items():
            # Get state-specific threshold
            threshold = snowbird_data.state_tax_thresholds.get(state, snowbird_data.tax_threshold)
            remaining_days = threshold - days
            percentage = (days / threshold) * 100
            
            # Create warnings based on proximity to threshold
            if remaining_days <= 0:
                warnings.append({
                    'state': state,
                    'type': 'exceeded',
                    'severity': 'critical',
                    'days': days,
                    'remaining': remaining_days,
                    'percentage': percentage,
                    'message': f"⚠️ CRITICAL: You've exceeded the {threshold}-day threshold in {state}!"
                })
            elif remaining_days <= 14:
                warnings.append({
                    'state': state,
                    'type': 'critical',
                    'severity': 'critical',
                    'days': days,
                    'remaining': remaining_days,
                    'percentage': percentage,
                    'message': f"🚨 CRITICAL: Only {remaining_days} days remaining in {state} before tax residency!"
                })
            elif remaining_days <= 30:
                warnings.append({
                    'state': state,
                    'type': 'warning',
                    'severity': 'warning',
                    'days': days,
                    'remaining': remaining_days,
                    'percentage': percentage,
                    'message': f"⚠️ WARNING: {remaining_days} days remaining in {state} before tax residency"
                })
            elif percentage >= 60:
                warnings.append({
                    'state': state,
                    'type': 'caution',
                    'severity': 'caution',
                    'days': days,
                    'remaining': remaining_days,
                    'percentage': percentage,
                    'message': f"⚡ CAUTION: You've used {percentage:.1f}% of your {state} days"
                })
        
        return warnings
    
    def create_threshold_reminders(self, warnings: List[Dict]) -> int:
        """
        Create Google Calendar reminders for threshold warnings.
        
        Args:
            warnings: List of threshold warnings
            
        Returns:
            Number of reminders created successfully
        """
        if not calendar_sync.is_authenticated():
            return 0
        
        created_count = 0
        today = datetime.date.today()
        
        for warning in warnings:
            try:
                # Create reminder based on severity
                if warning['severity'] == 'critical':
                    # Create immediate reminder for critical warnings
                    reminder_date = today + datetime.timedelta(days=1)
                    title = f"URGENT: {warning['state']} Tax Residency Alert"
                    description = (
                        f"{warning['message']}\n\n"
                        f"Current days in {warning['state']}: {warning['days']}\n"
                        f"Days remaining: {warning['remaining']}\n"
                        f"Threshold: {st.session_state.get('tax_threshold', 183)} days\n\n"
                        f"Action needed: Consider relocating or consulting tax advisor."
                    )
                elif warning['severity'] == 'warning':
                    # Create reminder for 7 days from now
                    reminder_date = today + datetime.timedelta(days=7)
                    title = f"{warning['state']} Tax Residency Warning"
                    description = (
                        f"{warning['message']}\n\n"
                        f"Current days: {warning['days']}\n"
                        f"Days remaining: {warning['remaining']}\n\n"
                        f"Plan your remaining time in {warning['state']} carefully."
                    )
                else:
                    # Create monthly reminder for caution level
                    reminder_date = today + datetime.timedelta(days=30)
                    title = f"{warning['state']} Tax Residency Monitor"
                    description = (
                        f"{warning['message']}\n\n"
                        f"Keep tracking your days in {warning['state']} to stay compliant."
                    )
                
                # Create the calendar event
                if calendar_sync.create_reminder_event(
                    title=title,
                    description=description,
                    due_date=reminder_date,
                    reminder_type="threshold"
                ):
                    created_count += 1
                    logger.info(f"Created threshold reminder for {warning['state']}")
                    
            except Exception as e:
                logger.error(f"Error creating threshold reminder: {e}")
        
        return created_count
    
    def schedule_monthly_check(self):
        """
        Create a monthly calendar reminder to check tax residency status.
        """
        if not calendar_sync.is_authenticated():
            return False
        
        try:
            # Schedule for first day of next month
            today = datetime.date.today()
            next_month = today.replace(day=1) + datetime.timedelta(days=32)
            next_month = next_month.replace(day=1)
            
            title = "Monthly Tax Residency Review"
            description = (
                "Time for your monthly Snowbird tax residency review!\n\n"
                "Tasks:\n"
                "• Review day counts for each state\n"
                "• Update any missing location logs\n"
                "• Plan upcoming travel based on threshold status\n"
                "• Review and adjust budgets if needed\n\n"
                "Open your Snowbird app to view detailed status."
            )
            
            return calendar_sync.create_reminder_event(
                title=title,
                description=description,
                due_date=next_month,
                reminder_type="tax"
            )
            
        except Exception as e:
            logger.error(f"Error scheduling monthly check: {e}")
            return False

# Global instance
threshold_monitor = ThresholdMonitor()
