
"""
Feature Flags Administration Interface for Snowbird Financial Assistant.

Provides a user-friendly interface for managing feature flags in real-time.
"""

import streamlit as st
import json
from utils.feature_flags import feature_flags, is_feature_enabled
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def render_feature_flags_admin():
    """Render the feature flags administration interface"""
    st.markdown("### 🚩 Feature Flags Management")
    
    # Reload button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Reload Flags"):
            feature_flags.reload_flags()
            st.success("Feature flags reloaded!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Session"):
            feature_flags.clear_session_overrides()
            st.success("Session overrides cleared!")
            st.rerun()
    
    with col3:
        st.info("💡 Changes are applied immediately. File changes persist across sessions.")
    
    # Get all flags
    all_flags = feature_flags.get_all_flags()
    
    # Categorize flags
    categories = {
        "Core Features": ["residency_tracker", "dual_home_budgets", "seasonal_cash_flow"],
        "AI & Automation": ["ai_assistant", "auto_tracker", "gmail_integration"],
        "User Experience": ["onboarding_carousel", "pwa_support", "theme_customization"],
        "Admin & Analytics": ["analytics", "admin_dashboard", "auth"],
        "Data & Reports": ["reports_export", "export_data", "import_data", "backup_restore"],
        "Integrations": ["notifications", "api_integrations"],
        "Advanced": ["multi_user", "advanced_analytics"]
    }
    
    # Display flags by category
    for category, flag_names in categories.items():
        with st.expander(f"📂 {category}", expanded=True):
            for flag_name in flag_names:
                if flag_name in all_flags:
                    render_flag_control(flag_name, all_flags[flag_name])
    
    # Other flags not in categories
    other_flags = {k: v for k, v in all_flags.items() 
                   if k not in [flag for flags in categories.values() for flag in flags]}
    
    if other_flags:
        with st.expander("📂 Other Flags", expanded=False):
            for flag_name, flag_value in other_flags.items():
                render_flag_control(flag_name, flag_value)
    
    # Bulk operations
    st.markdown("---")
    st.markdown("### 🔧 Bulk Operations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✅ Enable All Core"):
            for flag in categories["Core Features"]:
                feature_flags.enable_flag(flag)
            st.success("Core features enabled!")
            st.rerun()
    
    with col2:
        if st.button("🔒 Disable Advanced"):
            for flag in categories["Advanced"]:
                feature_flags.disable_flag(flag)
            st.success("Advanced features disabled!")
            st.rerun()
    
    with col3:
        if st.button("🚀 Production Mode"):
            production_flags = {
                "residency_tracker": True,
                "dual_home_budgets": True,
                "seasonal_cash_flow": True,
                "ai_assistant": True,
                "analytics": True,
                "auth": True,
                "pwa_support": True,
                "onboarding_carousel": True,
                "admin_dashboard": False,
                "auto_tracker": False,
                "gmail_integration": False,
                "notifications": False,
                "advanced_analytics": False
            }
            for flag, enabled in production_flags.items():
                if enabled:
                    feature_flags.enable_flag(flag)
                else:
                    feature_flags.disable_flag(flag)
            st.success("Production mode activated!")
            st.rerun()
    
    with col4:
        if st.button("🧪 Development Mode"):
            for flag in all_flags:
                feature_flags.enable_flag(flag)
            st.success("All features enabled for development!")
            st.rerun()
    
    # Export/Import configuration
    st.markdown("---")
    st.markdown("### 📤 Configuration Export/Import")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export Current Configuration**")
        config_json = json.dumps(all_flags, indent=2, sort_keys=True)
        st.download_button(
            label="📥 Download feature_flags.json",
            data=config_json,
            file_name="feature_flags.json",
            mime="application/json"
        )
    
    with col2:
        st.markdown("**Import Configuration**")
        uploaded_file = st.file_uploader(
            "Upload feature_flags.json",
            type="json",
            help="Upload a JSON file with feature flag configurations"
        )
        
        if uploaded_file is not None:
            try:
                new_flags = json.load(uploaded_file)
                
                if st.button("📤 Apply Imported Configuration"):
                    for flag_name, flag_value in new_flags.items():
                        if flag_value:
                            feature_flags.enable_flag(flag_name)
                        else:
                            feature_flags.disable_flag(flag_name)
                    
                    st.success(f"Imported {len(new_flags)} feature flags!")
                    st.rerun()
                
                # Preview
                st.markdown("**Preview:**")
                st.json(new_flags)
                
            except json.JSONDecodeError:
                st.error("Invalid JSON file format")
    
    # Environment Variables Guide
    with st.expander("📖 Environment Variables Guide", expanded=False):
        st.markdown("""
        **Using Environment Variables:**
        
        You can override feature flags using environment variables with the `FF_` prefix:
        
        ```bash
        FF_AI_ASSISTANT=true
        FF_ANALYTICS=false
        FF_ONBOARDING_CAROUSEL=true
        ```
        
        **Using Streamlit Secrets:**
        
        Add to your `.streamlit/secrets.toml`:
        
        ```toml
        [feature_flags]
        ai_assistant = true
        analytics = false
        onboarding_carousel = true
        ```
        
        **Priority Order:**
        1. Session overrides (temporary)
        2. Streamlit secrets
        3. Environment variables
        4. feature_flags.json file
        5. Default values
        """)

def render_flag_control(flag_name: str, current_value: bool):
    """Render a single feature flag control"""
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
    
    with col1:
        # Format flag name for display
        display_name = flag_name.replace('_', ' ').title()
        st.write(f"**{display_name}**")
        
        # Show current status
        status_color = "🟢" if current_value else "🔴"
        source = feature_flags.get_flag_source(flag_name)
        st.caption(f"{status_color} {source}")
    
    with col2:
        # Current state indicator
        if current_value:
            st.success("ON")
        else:
            st.error("OFF")
    
    with col3:
        # Toggle button
        if st.button("🔄", key=f"toggle_{flag_name}", help="Toggle flag"):
            new_state = feature_flags.toggle_flag(flag_name)
            st.rerun()
    
    with col4:
        # Temporary toggle
        if st.button("⏰", key=f"temp_{flag_name}", help="Temporary toggle"):
            feature_flags.toggle_flag(flag_name, temporary=True)
            st.rerun()
    
    with col5:
        # Flag description
        descriptions = {
            "residency_tracker": "Day tracking and tax residency monitoring",
            "dual_home_budgets": "Budget management for multiple homes",
            "seasonal_cash_flow": "Seasonal expense planning",
            "ai_assistant": "OpenAI-powered financial assistant",
            "reports_export": "PDF/Excel report generation",
            "onboarding_carousel": "First-time user tutorial",
            "pwa_support": "Progressive Web App features",
            "analytics": "User behavior tracking",
            "auth": "Firebase user authentication",
            "admin_dashboard": "Administrative interface",
            "theme_customization": "Custom themes and styling",
            "auto_tracker": "Automatic location detection",
            "gmail_integration": "Email-based travel detection",
            "notifications": "Email and push notifications"
        }
        
        description = descriptions.get(flag_name, "Custom feature flag")
        st.caption(description)

def render_feature_status_sidebar():
    """Render a compact feature status in the sidebar"""
    with st.sidebar:
        with st.expander("🚩 Feature Status", expanded=False):
            all_flags = feature_flags.get_all_flags()
            enabled_count = sum(all_flags.values())
            total_count = len(all_flags)
            
            st.metric("Features Enabled", f"{enabled_count}/{total_count}")
            
            # Show key features
            key_features = ["ai_assistant", "analytics", "auth", "pwa_support"]
            for feature in key_features:
                if feature in all_flags:
                    icon = "🟢" if all_flags[feature] else "🔴"
                    name = feature.replace('_', ' ').title()
                    st.write(f"{icon} {name}")
