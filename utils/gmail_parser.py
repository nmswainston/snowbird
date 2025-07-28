
"""
Gmail integration for automatic travel detection and location logging.
"""
import re
import datetime
from typing import List, Dict, Optional, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from utils.auth import authenticate_gmail
from utils.logging_config import data_logger
from utils.error_handling import APIError
from utils.security import DataEncryption, DataPrivacy, AuditLogger
import streamlit as st

class GmailTravelParser:
    """Parse Gmail for travel-related emails and extract location data"""
    
    def __init__(self):
        self.travel_keywords = [
            'flight', 'airline', 'boarding pass', 'confirmation',
            'hotel', 'reservation', 'booking', 'check-in',
            'rental car', 'car rental', 'itinerary',
            'departure', 'arrival', 'terminal'
        ]
        
        self.location_patterns = {
            'Arizona': [
                r'PHX|Phoenix|Scottsdale|Tempe|Mesa|Chandler|Glendale|Peoria|Surprise|Arizona|AZ',
                r'Sky Harbor|Phoenix Sky Harbor'
            ],
            'Minnesota': [
                r'MSP|Minneapolis|St\.?\s*Paul|Saint Paul|Bloomington|Minnesota|MN',
                r'Mall of America|Twin Cities'
            ]
        }
    
    def authenticate_and_build_service(self):
        """Authenticate and build Gmail service"""
        try:
            creds = authenticate_gmail()
            if not creds:
                return None
            
            service = build('gmail', 'v1', credentials=creds)
            return service
        except Exception as e:
            data_logger.error(f"Gmail authentication failed: {e}")
            raise APIError(f"Failed to authenticate with Gmail: {e}")
    
    def search_travel_emails(self, days_back: int = 30, max_results: int = 50) -> List[Dict]:
        """Search for travel-related emails in the last N days"""
        service = self.authenticate_and_build_service()
        if not service:
            return []
        
        try:
            # Calculate date range
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=days_back)
            
            # Build search query
            query_terms = []
            query_terms.append(f'after:{start_date.strftime("%Y/%m/%d")}')
            query_terms.append(f'before:{end_date.strftime("%Y/%m/%d")}')
            
            # Add travel-related keywords
            keyword_query = ' OR '.join(self.travel_keywords)
            query_terms.append(f'({keyword_query})')
            
            query = ' '.join(query_terms)
            
            # Execute search
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            travel_emails = []
            
            for message in messages:
                email_data = self.get_email_details(service, message['id'])
                if email_data:
                    travel_emails.append(email_data)
            
            # Log Gmail access for audit purposes
            AuditLogger.log_gmail_access(len(travel_emails))
            
            return travel_emails
            
        except Exception as e:
            data_logger.error(f"Failed to search travel emails: {e}")
            raise APIError(f"Failed to search emails: {e}")
    
    def get_email_details(self, service, message_id: str) -> Optional[Dict]:
        """Get detailed email content and metadata"""
        try:
            message = service.users().messages().get(userId='me', id=message_id).execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = self.extract_email_body(message['payload'])
            
            # Sanitize email content for privacy
            body = DataPrivacy.sanitize_email_content(body)
            subject = DataPrivacy.sanitize_email_content(subject)
            
            # Parse for travel information
            travel_info = self.parse_travel_information(subject, body, sender)
            
            if travel_info:
                return {
                    'id': message_id,
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body_snippet': message.get('snippet', ''),
                    'travel_info': travel_info
                }
            
            return None
            
        except Exception as e:
            data_logger.error(f"Failed to get email details for {message_id}: {e}")
            return None
    
    def extract_email_body(self, payload) -> str:
        """Extract text body from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += self.decode_base64(data)
                elif part['mimeType'] == 'text/html':
                    # Fallback to HTML if no plain text
                    if not body:
                        data = part['body']['data']
                        body += self.decode_base64(data)
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = self.decode_base64(data)
        
        return body
    
    def decode_base64(self, data: str) -> str:
        """Decode base64 email content"""
        import base64
        try:
            return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception:
            return ""
    
    def parse_travel_information(self, subject: str, body: str, sender: str) -> Optional[Dict]:
        """Parse email content for travel information"""
        content = f"{subject} {body}".lower()
        
        # Detect locations
        detected_locations = []
        for state, patterns in self.location_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_locations.append(state)
                    break
        
        # Extract dates
        dates = self.extract_dates(content)
        
        # Determine travel type
        travel_type = self.determine_travel_type(subject, body, sender)
        
        if detected_locations and dates:
            return {
                'locations': list(set(detected_locations)),
                'dates': dates,
                'travel_type': travel_type,
                'confidence': self.calculate_confidence(detected_locations, dates, travel_type),
                'sender_domain': sender.split('@')[-1] if '@' in sender else sender
            }
        
        return None
    
    def extract_dates(self, content: str) -> List[str]:
        """Extract potential travel dates from email content"""
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{4}-\d{2}-\d{2}\b',      # YYYY-MM-DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b'     # DD Month YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates.extend(matches)
        
        return dates[:5]  # Limit to 5 dates to avoid noise
    
    def determine_travel_type(self, subject: str, body: str, sender: str) -> str:
        """Determine the type of travel from email content"""
        content = f"{subject} {body}".lower()
        
        if any(word in content for word in ['flight', 'airline', 'boarding', 'departure']):
            return 'flight'
        elif any(word in content for word in ['hotel', 'reservation', 'check-in', 'accommodation']):
            return 'hotel'
        elif any(word in content for word in ['car rental', 'rental car', 'vehicle']):
            return 'car_rental'
        elif any(word in content for word in ['train', 'rail', 'amtrak']):
            return 'train'
        else:
            return 'general'
    
    def calculate_confidence(self, locations: List[str], dates: List[str], travel_type: str) -> str:
        """Calculate confidence level of travel detection"""
        score = 0
        
        # Location confidence
        if len(locations) == 1:
            score += 3
        elif len(locations) > 1:
            score += 2
        
        # Date confidence
        if len(dates) >= 2:
            score += 3
        elif len(dates) == 1:
            score += 2
        
        # Travel type confidence
        if travel_type in ['flight', 'hotel']:
            score += 2
        elif travel_type != 'general':
            score += 1
        
        if score >= 6:
            return 'high'
        elif score >= 4:
            return 'medium'
        else:
            return 'low'
    
    def suggest_location_logs(self, travel_emails: List[Dict]) -> List[Dict]:
        """Generate location log suggestions from travel emails"""
        suggestions = []
        
        for email in travel_emails:
            travel_info = email.get('travel_info', {})
            locations = travel_info.get('locations', [])
            dates = travel_info.get('dates', [])
            
            for location in locations:
                for date_str in dates:
                    try:
                        # Parse and normalize date
                        parsed_date = self.parse_date_string(date_str)
                        if parsed_date:
                            suggestions.append({
                                'date': parsed_date.isoformat(),
                                'location': location,
                                'source_email': email['subject'][:50],
                                'confidence': travel_info.get('confidence', 'low'),
                                'travel_type': travel_info.get('travel_type', 'general'),
                                'email_id': email['id']
                            })
                    except Exception:
                        continue
        
        # Remove duplicates and sort by date
        unique_suggestions = []
        seen = set()
        
        for suggestion in suggestions:
            key = (suggestion['date'], suggestion['location'])
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(suggestion)
        
        return sorted(unique_suggestions, key=lambda x: x['date'], reverse=True)
    
    def parse_date_string(self, date_str: str) -> Optional[datetime.date]:
        """Parse various date string formats"""
        date_formats = [
            '%m/%d/%Y', '%Y-%m-%d', '%B %d, %Y', '%b %d, %Y',
            '%d %B %Y', '%d %b %Y', '%m-%d-%Y', '%d/%m/%Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        return None
