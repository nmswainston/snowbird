
import streamlit as st
import datetime
import requests
from typing import Dict, Optional, Tuple
from utils.data_models import SnowbirdData
from utils.logging_config import data_logger
from utils.gmail_parser import GmailTravelParser
from utils.error_handling import APIError, ErrorDisplay
from utils.security import AuditLogger, DataPrivacy

class AutoLocationTracker:
    """Automatic location tracking for audit trails"""
    
    def __init__(self):
        self.snowbird_data = SnowbirdData()
    
    def get_browser_location(self):
        """Get location from browser geolocation API"""
        # This uses Streamlit's HTML/JS capabilities
        location_html = '''
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                document.getElementById("location-result").innerHTML = "Geolocation not supported";
            }
        }
        
        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            document.getElementById("location-result").innerHTML = 
                `Latitude: ${lat}, Longitude: ${lon}`;
            
            // Send to Streamlit (this would need proper integration)
            window.parent.postMessage({
                type: 'location',
                lat: lat,
                lon: lon,
                accuracy: position.coords.accuracy,
                timestamp: new Date().toISOString()
            }, '*');
        }
        
        function showError(error) {
            let message = "";
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    message = "Location access denied by user";
                    break;
                case error.POSITION_UNAVAILABLE:
                    message = "Location information unavailable";
                    break;
                case error.TIMEOUT:
                    message = "Location request timed out";
                    break;
                default:
                    message = "Unknown location error";
                    break;
            }
            document.getElementById("location-result").innerHTML = message;
        }
        </script>
        
        <div>
            <button onclick="getLocation()" style="padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Get Current Location
            </button>
            <div id="location-result" style="margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
                Click button to get location
            </div>
        </div>
        '''
        return location_html
    
    def determine_state_from_coords(self, latitude: float, longitude: float) -> Optional[str]:
        """Determine state from GPS coordinates"""
        # Arizona approximate bounds
        arizona_bounds = {
            'lat_min': 31.3, 'lat_max': 37.0,
            'lon_min': -114.8, 'lon_max': -109.0
        }
        
        # Minnesota approximate bounds  
        minnesota_bounds = {
            'lat_min': 43.5, 'lat_max': 49.4,
            'lon_min': -97.2, 'lon_max': -89.5
        }
        
        if (arizona_bounds['lat_min'] <= latitude <= arizona_bounds['lat_max'] and 
            arizona_bounds['lon_min'] <= longitude <= arizona_bounds['lon_max']):
            return "Arizona"
        elif (minnesota_bounds['lat_min'] <= latitude <= minnesota_bounds['lat_max'] and 
              minnesota_bounds['lon_min'] <= longitude <= minnesota_bounds['lon_max']):
            return "Minnesota"
        else:
            return None
    
    def get_ip_location(self) -> Optional[Dict]:
        """Get approximate location from IP address"""
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        'latitude': data['lat'],
                        'longitude': data['lon'],
                        'city': data['city'],
                        'region': data['regionName'],
                        'country': data['country'],
                        'accuracy': 'city'  # IP-based is city-level accurate
                    }
        except Exception as e:
            data_logger.error(f"Failed to get IP location: {e}")
        return None
    
    def create_audit_log_entry(self, location_data: Dict, detection_method: str) -> Dict:
        """Create comprehensive audit log entry"""
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'date': datetime.date.today().isoformat(),
            'detection_method': detection_method,
            'location_data': location_data,
            'confidence': self._calculate_confidence(location_data, detection_method),
            'audit_trail': True,
            'user_confirmed': False
        }
    
    def _calculate_confidence(self, location_data: Dict, method: str) -> str:
        """Calculate confidence level of location detection"""
        if method == 'gps':
            accuracy = location_data.get('accuracy', 1000)
            if accuracy < 100:
                return 'high'
            elif accuracy < 1000:
                return 'medium'
            else:
                return 'low'
        elif method == 'ip':
            return 'medium'
        else:
            return 'low'

def render_auto_tracker():
    """Render automatic location tracking interface"""
    tracker = AutoLocationTracker()
    gmail_parser = GmailTravelParser()
    
    st.markdown('**<i data-lucide="map" class="icon"></i>Automatic Location Tracking**', unsafe_allow_html=True)
    
    # Gmail Integration Section
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="mail" class="icon"></i>Gmail Travel Analysis**', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        gmail_enabled = st.toggle("Enable Gmail Integration", value=False)
        if gmail_enabled:
            days_back = st.slider("Analyze emails from last N days:", 7, 90, 30)
    
    with col2:
        if gmail_enabled and st.button("🔍 Analyze Travel Emails"):
            with st.spinner("Analyzing your emails for travel information..."):
                try:
                    travel_emails = gmail_parser.search_travel_emails(days_back=days_back)
                    
                    if travel_emails:
                        suggestions = gmail_parser.suggest_location_logs(travel_emails)
                        st.session_state.gmail_suggestions = suggestions
                        st.session_state.gmail_emails = travel_emails
                        st.success(f"📧 Found {len(travel_emails)} travel-related emails with {len(suggestions)} location suggestions")
                    else:
                        st.info("📭 No travel-related emails found in the specified period")
                        
                except APIError as e:
                    ErrorDisplay.api_error(e, "Gmail")
                except Exception as e:
                    st.error(f"❌ Error analyzing emails: {str(e)}")
    
    # Show Gmail suggestions if available
    if gmail_enabled and 'gmail_suggestions' in st.session_state:
        st.markdown("**📋 Travel Suggestions from Emails:**")
        
        suggestions = st.session_state.gmail_suggestions
        if suggestions:
            for i, suggestion in enumerate(suggestions[:10]):  # Show top 10
                with st.expander(f"📅 {suggestion['date']} - {suggestion['location']} ({suggestion['confidence']} confidence)"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Source:** {suggestion['source_email']}")
                        st.write(f"**Travel Type:** {suggestion['travel_type']}")
                        st.write(f"**Confidence:** {suggestion['confidence']}")
                    
                    with col2:
                        if st.button(f"Log this day", key=f"gmail_log_{i}"):
                            success, message = tracker.snowbird_data.add_day_log(
                                suggestion['location'],
                                suggestion['date'],
                                auto_logged=True
                            )
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.warning(message)
        else:
            st.info("No location suggestions found in analyzed emails")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # GPS Location Tracking Section
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="map-pin" class="icon"></i>GPS Location Tracking**', unsafe_allow_html=True)
    
    # Auto-tracking settings
    col1, col2 = st.columns(2)
    
    with col1:
        auto_track_enabled = st.toggle("Enable Auto-Tracking", value=False)
        if auto_track_enabled:
            st.session_state.auto_tracking = True
            frequency = st.selectbox("Check frequency:", ["Once daily", "Twice daily", "Manual only"])
    
    with col2:
        if st.button("Get Current Location"):
            with st.spinner("Getting location..."):
                # Try IP-based location first (more reliable in web apps)
                ip_location = tracker.get_ip_location()
                
                if ip_location:
                    detected_state = tracker.determine_state_from_coords(
                        ip_location['latitude'], 
                        ip_location['longitude']
                    )
                    
                    st.success(f"📍 Detected: {ip_location['city']}, {ip_location['region']}")
                    
                    if detected_state:
                        st.info(f"🏠 Likely in: **{detected_state}**")
                        
                        # Create audit log
                        audit_entry = tracker.create_audit_log_entry(ip_location, 'ip')
                        
                        if 'auto_logs' not in st.session_state:
                            st.session_state.auto_logs = []
                        st.session_state.auto_logs.append(audit_entry)
                        
                        # Option to confirm and log
                        if st.button(f"Confirm & Log Day in {detected_state}"):
                            success, message = tracker.snowbird_data.add_day_log(
                                detected_state, 
                                auto_logged=True
                            )
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.warning(message)
                    else:
                        st.warning("⚠️ Location not recognized as Arizona or Minnesota")
                else:
                    st.error("❌ Could not determine location")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Audit Trail Section
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('**<i data-lucide="shield-check" class="icon"></i>Location Audit Trail**', unsafe_allow_html=True)
    
    if 'auto_logs' in st.session_state and st.session_state.auto_logs:
        st.write("**Recent Auto-Detections:**")
        
        for i, log in enumerate(reversed(st.session_state.auto_logs[-10:])):
            with st.expander(f"📅 {log['date']} - {log['detection_method'].upper()} Detection"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Method:** {log['detection_method']}")
                    st.write(f"**Confidence:** {log['confidence']}")
                    st.write(f"**Confirmed:** {'✅' if log['user_confirmed'] else '❌'}")
                
                with col2:
                    if 'city' in log['location_data']:
                        st.write(f"**Location:** {log['location_data']['city']}, {log['location_data']['region']}")
                    st.write(f"**Coordinates:** {log['location_data']['latitude']:.4f}, {log['location_data']['longitude']:.4f}")
                
                # Raw data for audit purposes
                with st.expander("Raw Audit Data"):
                    st.json(log)
    else:
        st.info("No automatic location detections yet. Enable auto-tracking or manually request location.")
    
    st.markdown('</div>', unsafe_allow_html=True)
