
import streamlit as st
import datetime

def show_page():
    st.markdown('<h2 class="section-header">📍 Location Tracking & Day Counter</h2>', unsafe_allow_html=True)
    
    # Location detection section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 Smart Location Detection")
        location_html = """
        <div id="location-info" style="text-align: center;">
            <p style="margin-bottom: 1rem;">Click the button below to detect your current location:</p>
            <button onclick="getLocation()" style="padding: 12px 24px; background: linear-gradient(135deg, #12BDF2 0%, #0891D1 100%); color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                📍 Detect My Location
            </button>
            <div id="location-result" style="margin-top: 15px; padding: 10px; background: rgba(18, 189, 242, 0.1); border-radius: 8px; min-height: 40px; border: 1px solid rgba(18, 189, 242, 0.3);"></div>
        </div>
        
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
                document.getElementById("location-result").innerHTML = "🔍 Detecting location...";
            } else {
                document.getElementById("location-result").innerHTML = "❌ Geolocation is not supported by this browser.";
            }
        }
        
        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            let detectedState = "Unknown";
            if (lat >= 31.0 && lat <= 37.0 && lon >= -114.8 && lon <= -109.0) {
                detectedState = "Arizona";
            } else if (lat >= 43.5 && lat <= 49.4 && lon >= -97.2 && lon <= -89.5) {
                detectedState = "Minnesota";
            }
            
            document.getElementById("location-result").innerHTML = 
                `<strong>📍 Location detected: ${detectedState}</strong><br>
                 🌍 Coordinates: ${lat.toFixed(4)}, ${lon.toFixed(4)}<br>
                 <small>💡 Tip: Use the manual logging below to record your day!</small>`;
        }
        
        function showError(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    document.getElementById("location-result").innerHTML = "❌ Location access denied by user.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    document.getElementById("location-result").innerHTML = "❌ Location information is unavailable.";
                    break;
                case error.TIMEOUT:
                    document.getElementById("location-result").innerHTML = "❌ Location request timed out.";
                    break;
                default:
                    document.getElementById("location-result").innerHTML = "❌ An unknown error occurred.";
                    break;
            }
        }
        </script>
        """
        st.components.v1.html(location_html, height=200)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("📱 Quick Stats")
        today = datetime.date.today()
        st.write(f"📅 Today: {today.strftime('%B %d, %Y')}")
        
        # Show current streak
        if st.session_state.day_log:
            recent_logs = [log for log in st.session_state.day_log if log['date'] >= (today - datetime.timedelta(days=7)).isoformat()]
            if recent_logs:
                last_state = recent_logs[-1]['state']
                consecutive_days = 1
                for i in range(len(recent_logs) - 2, -1, -1):
                    if recent_logs[i]['state'] == last_state:
                        consecutive_days += 1
                    else:
                        break
                st.markdown(f'<div class="metric-card"><h4>🔥 Current Streak</h4><h2>{consecutive_days} days in {last_state}</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Manual day logging
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("📝 Manual Day Logging")
    state_options = list(st.session_state.states.keys())
    location = st.radio("🏠 Where are you today?", state_options)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(f"✅ Log Today in {location}", type="primary"):
            today_str = datetime.date.today().isoformat()
            existing_log = next((log for log in st.session_state.day_log if log['date'] == today_str), None)
            if existing_log:
                st.warning(f"Already logged today in {existing_log['state']}!")
            else:
                st.session_state.states[location] += 1
                st.session_state.day_log.append({
                    'date': today_str,
                    'state': location,
                    'method': 'manual',
                    'timestamp': datetime.datetime.now().isoformat()
                })
                st.success(f"✅ Logged today in {location}!")
                st.rerun()

    with col2:
        if st.button(f"➖ Remove Today") and st.session_state.states[location] > 0:
            today_str = datetime.date.today().isoformat()
            st.session_state.day_log = [log for log in st.session_state.day_log if log['date'] != today_str]
            st.session_state.states[location] -= 1
            st.success(f"➖ Removed today from {location}!")
            st.rerun()

    with col3:
        custom_date = st.date_input("📅 Custom date:", value=datetime.date.today(), key="custom_date")
        if st.button("📅 Log Custom"):
            custom_date_str = custom_date.isoformat()
            existing_log = next((log for log in st.session_state.day_log if log['date'] == custom_date_str), None)
            if existing_log:
                st.warning(f"Date {custom_date} already logged in {existing_log['state']}!")
            else:
                st.session_state.states[location] += 1
                st.session_state.day_log.append({
                    'date': custom_date_str,
                    'state': location,
                    'method': 'custom',
                    'timestamp': datetime.datetime.now().isoformat()
                })
                st.success(f"✅ Logged {custom_date} in {location}!")
                st.rerun()

    with col4:
        manual_days = st.number_input(f"🔢 Set {location} total:", 
                                     min_value=0, max_value=365,
                                     value=st.session_state.states[location],
                                     key=f"manual_{location}")
        if st.button("💾 Update"):
            st.session_state.states[location] = manual_days
            st.success(f"Updated {location} to {manual_days} days!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity log
    st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
    st.subheader("📋 Recent Activity Log")
    if st.session_state.day_log:
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:10]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.write(f"📅 {date_obj.strftime('%b %d, %Y')} - 🏠 {log['state']} ({log['method']})")
    else:
        st.write("🔍 No activity logged yet. Start by logging your current location!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Smart nudges
    def check_nudges():
        today = datetime.date.today()
        today_str = today.isoformat()
        
        if st.session_state.last_nudge_date == today_str:
            return
        
        for state, days in st.session_state.states.items():
            threshold = st.session_state.tax_threshold
            
            if days >= threshold - 7 and days < threshold:
                days_left = threshold - days
                st.warning(f"⚠️ **Gentle Reminder**: You're {days_left} days away from tax residency in {state}! ({days}/{threshold} days)")
                st.session_state.last_nudge_date = today_str
            elif days >= threshold - 3 and days < threshold:
                days_left = threshold - days
                st.error(f"🚨 **Close Call**: Only {days_left} days until tax residency in {state}! ({days}/{threshold} days)")
                st.session_state.last_nudge_date = today_str
            elif days >= threshold:
                st.error(f"🔴 **Tax Alert**: You are now considered a tax resident of {state}! ({days}/{threshold} days)")

    check_nudges()
