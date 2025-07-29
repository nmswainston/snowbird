
"""
Authentication UI components for the Snowbird app.
Provides login, registration, and profile management interfaces.
"""

import streamlit as st
from typing import Dict, Any
from utils.firebase_auth import get_firebase_auth
from utils.firebase_database import get_firebase_database
from utils.logger import logger
from components.loading_states import show_loading, show_success, show_error

def render_login_form():
    """Render the login form"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_submitted = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Create Account", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
    
    if login_submitted:
        if email and password:
            with st.spinner("Logging in..."):
                auth = get_firebase_auth()
                result = auth.login_user(email, password)
                
                if result["success"]:
                    # Update last login in database
                    db = get_firebase_database()
                    db.update_last_login(result["user"]["uid"])
                    
                    show_success("✅ Login successful!")
                    st.rerun()
                else:
                    show_error(f"❌ Login failed: {result.get('error', 'Unknown error')}")
        else:
            show_error("Please enter both email and password")

def render_registration_form():
    """Render the registration form"""
    st.markdown("### 📝 Create Your Account")
    
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        display_name = st.text_input("Display Name (Optional)", placeholder="Your Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            register_submitted = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
    
    if register_submitted:
        if not email or not password:
            st.error("Please enter both email and password")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            with st.spinner("Creating account..."):
                auth = get_firebase_auth()
                result = auth.register_user(email, password, display_name)
                
                if result["success"]:
                    # Create user profile in database
                    db = get_firebase_database()
                    db.create_user_profile(
                        result["user"]["uid"], 
                        email, 
                        display_name or email.split('@')[0]
                    )
                    
                    show_success("✅ Account created successfully!")
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    show_error(f"❌ Registration failed: {result.get('error', 'Unknown error')}")

def render_auth_page():
    """Render the main authentication page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>❄️ Welcome to Snowbird Financial Assistant 🏖️</h1>
        <p style="font-size: 1.2rem; color: #64748B;">
            Your seasonal lifestyle deserves smart financial management
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show registration or login form
    if st.session_state.get('show_register', False):
        render_registration_form()
    else:
        render_login_form()
    
    # Add some helpful information
    with st.expander("ℹ️ About Snowbird Financial Assistant"):
        st.markdown("""
        **Features:**
        - 📍 Track your days in different states for tax residency
        - 💰 Manage budgets for multiple homes
        - 🤖 Get AI-powered financial advice
        - 📊 Generate tax residency reports
        - 🔄 Automatic location detection via Gmail
        - 🎨 Customizable themes and preferences
        
        **Privacy & Security:**
        - Your data is securely stored and encrypted
        - Only you have access to your financial information
        - No data is shared with third parties
        """)

def render_user_profile():
    """Render user profile management"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if not user:
        return
    
    st.markdown("### 👤 User Profile")
    
    # Get user profile from database
    db = get_firebase_database()
    profile = db.get_user_profile(user['uid'])
    
    if profile:
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Email", value=profile.get('email', ''), disabled=True)
            new_display_name = st.text_input("Display Name", value=profile.get('display_name', ''))
        
        with col2:
            st.text_input("Member Since", value=profile.get('created_at', '').strftime('%B %d, %Y') if profile.get('created_at') else '', disabled=True)
            st.text_input("Last Login", value=profile.get('last_login', '').strftime('%B %d, %Y at %I:%M %p') if profile.get('last_login') else '', disabled=True)
        
        # Preferences
        st.markdown("**Preferences:**")
        preferences = profile.get('preferences', {})
        
        col1, col2 = st.columns(2)
        with col1:
            notifications = st.checkbox("Enable Notifications", value=preferences.get('notifications', True))
        with col2:
            auto_tracking = st.checkbox("Auto Location Tracking", value=preferences.get('auto_tracking', False))
        
        # Update profile button
        if st.button("Update Profile"):
            update_data = {
                'display_name': new_display_name,
                'preferences': {
                    'notifications': notifications,
                    'auto_tracking': auto_tracking,
                    'theme': preferences.get('theme', 'default')
                }
            }
            
            if db.update_user_profile(user['uid'], update_data):
                st.success("✅ Profile updated successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to update profile")

def render_logout_button():
    """Render logout button in sidebar"""
    auth = get_firebase_auth()
    user = auth.get_current_user()
    
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 {user.get('email', 'User')}**")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth.logout_user()
            st.rerun()

def check_authentication():
    """Check if user is authenticated and handle accordingly"""
    auth = get_firebase_auth()
    
    if not auth.is_authenticated():
        render_auth_page()
        st.stop()
    
    # Refresh token if needed
    auth.refresh_token()
    
    return auth.get_current_user()
