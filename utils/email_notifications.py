
import smtplib
import schedule
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
from typing import Dict, Optional
import streamlit as st
from utils.config import settings
from utils.logging_config import logger
from utils.data_models import SnowbirdData

class EmailNotificationService:
    """Service for sending daily email summaries to users"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.snowbird_data = SnowbirdData()
        
    def send_daily_summary(self, user_email: str) -> bool:
        """
        Send daily summary email to user with their residency status
        
        Args:
            user_email: User's email address
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Get user's current residency data
            states_data = st.session_state.get('states', {'Arizona': 0, 'Minnesota': 0})
            tax_threshold = st.session_state.get('tax_threshold', 183)
            
            # Calculate percentages
            az_days = states_data.get('Arizona', 0)
            mn_days = states_data.get('Minnesota', 0)
            
            az_percentage = (az_days / tax_threshold) * 100
            mn_percentage = (mn_days / tax_threshold) * 100
            
            # Get tax status for each state
            az_status, az_severity = self.snowbird_data.get_tax_status(az_days, tax_threshold)
            mn_status, mn_severity = self.snowbird_data.get_tax_status(mn_days, tax_threshold)
            
            # Build email content
            subject = f"Snowbird Daily Summary - {datetime.now().strftime('%B %d, %Y')}"
            
            email_body = self._build_email_body(
                az_days, mn_days, az_percentage, mn_percentage,
                az_status, mn_status, tax_threshold
            )
            
            # Send email
            return self._send_email(user_email, subject, email_body)
            
        except Exception as e:
            logger.error(f"Failed to send daily summary email: {e}")
            return False
    
    def _build_email_body(
        self, az_days: int, mn_days: int, az_percent: float, mn_percent: float,
        az_status: str, mn_status: str, threshold: int
    ) -> str:
        """Build HTML email body with residency summary"""
        
        # Determine status colors
        az_color = self._get_status_color(az_status)
        mn_color = self._get_status_color(mn_status)
        
        days_remaining_az = max(0, threshold - az_days)
        days_remaining_mn = max(0, threshold - mn_days)
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px; color: #333;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 10px;">
                    🏠 Snowbird Daily Summary
                </h2>
                
                <p>Hello! Here's your daily residency status update:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #495057; margin-top: 0;">📊 Current Status</h3>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                        <div style="flex: 1; min-width: 250px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid {az_color};">
                            <h4 style="margin: 0 0 10px 0; color: {az_color};">🌵 Arizona</h4>
                            <p style="margin: 5px 0; font-size: 16px;"><strong>{az_days} days</strong> spent this year</p>
                            <p style="margin: 5px 0; color: {az_color};"><strong>{az_percent:.1f}%</strong> of {threshold}-day threshold</p>
                            <p style="margin: 5px 0; color: {az_color}; font-weight: bold;">Status: {az_status}</p>
                            <p style="margin: 5px 0; font-size: 14px; color: #666;">
                                {days_remaining_az} days remaining before tax residency
                            </p>
                        </div>
                        
                        <div style="flex: 1; min-width: 250px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid {mn_color};">
                            <h4 style="margin: 0 0 10px 0; color: {mn_color};">❄️ Minnesota</h4>
                            <p style="margin: 5px 0; font-size: 16px;"><strong>{mn_days} days</strong> spent this year</p>
                            <p style="margin: 5px 0; color: {mn_color};"><strong>{mn_percent:.1f}%</strong> of {threshold}-day threshold</p>
                            <p style="margin: 5px 0; color: {mn_color}; font-weight: bold;">Status: {mn_status}</p>
                            <p style="margin: 5px 0; font-size: 14px; color: #666;">
                                {days_remaining_mn} days remaining before tax residency
                            </p>
                        </div>
                    </div>
                </div>
                
                <div style="background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #2E86AB; margin-top: 0;">💡 Quick Tips</h4>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Keep tracking your daily locations to stay compliant</li>
                        <li>Plan your travel schedule to avoid exceeding thresholds</li>
                        <li>Review your budget and cash flow regularly</li>
                    </ul>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; text-align: center;">
                    <p>This is an automated email from your Snowbird Financial Assistant.</p>
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def _get_status_color(self, status: str) -> str:
        """Get color code based on tax status"""
        status_colors = {
            'SAFE': '#28a745',
            'CAUTION': '#ffc107', 
            'CRITICAL': '#fd7e14',
            'TAX RESIDENT': '#dc3545'
        }
        return status_colors.get(status, '#6c757d')
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email using SMTP configuration
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: HTML email body
            
        Returns:
            bool: True if sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Daily summary email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

class EmailScheduler:
    """Scheduler for daily email notifications"""
    
    def __init__(self):
        self.email_service = EmailNotificationService()
        self.is_running = False
        self.scheduler_thread = None
        
    def start_scheduler(self):
        """
        Start the email scheduler in a background thread
        
        Schedule daily emails to be sent at 9:00 AM based on DAILY_REMINDER_TIME setting
        """
        if self.is_running:
            logger.warning("Email scheduler is already running")
            return
            
        # Get daily reminder time from settings (default: 09:00)
        reminder_time = getattr(settings, 'DAILY_REMINDER_TIME', '09:00')
        
        # Schedule daily email task
        schedule.every().day.at(reminder_time).do(self._send_daily_emails)
        
        # Start scheduler in background thread
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info(f"Email scheduler started - daily emails at {reminder_time}")
    
    def stop_scheduler(self):
        """Stop the email scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("Email scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop in background thread"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _send_daily_emails(self):
        """
        Send daily summary emails to all users who have opted in
        
        This function reads user email preferences from session state or database
        and sends daily summaries to users who have email notifications enabled
        """
        try:
            # Get user email from session state
            user_email = st.session_state.get('user_email', '')
            email_notifications_enabled = st.session_state.get('email_notifications', False)
            
            if user_email and email_notifications_enabled:
                success = self.email_service.send_daily_summary(user_email)
                if success:
                    logger.info(f"Daily summary sent to {user_email}")
                else:
                    logger.error(f"Failed to send daily summary to {user_email}")
            else:
                logger.debug("No email configured or notifications disabled")
                
        except Exception as e:
            logger.error(f"Error in daily email task: {e}")

# Global scheduler instance
email_scheduler = EmailScheduler()

def initialize_email_scheduler():
    """Initialize the email scheduler when the app starts"""
    try:
        # Only start scheduler if SMTP settings are configured
        if (settings.SMTP_USERNAME and settings.SMTP_PASSWORD and 
            settings.SMTP_SERVER and settings.SMTP_PORT):
            email_scheduler.start_scheduler()
            logger.info("Email notification system initialized")
        else:
            logger.info("Email scheduler not started - SMTP settings not configured")
    except Exception as e:
        logger.error(f"Failed to initialize email scheduler: {e}")

def send_test_email(email: str) -> bool:
    """Send a test email to verify configuration"""
    service = EmailNotificationService()
    return service.send_daily_summary(email)
