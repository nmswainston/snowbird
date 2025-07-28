
"""
In-app onboarding system for Snowbird Financial Assistant.

This module provides a guided tour for first-time users, introducing them
to key features and helping them get started with the application.
"""

import streamlit as st
from typing import Dict, List, Any
import time


# Onboarding steps configuration
ONBOARDING_STEPS = [
    {
        "title": "Welcome to Snowbird! ❄️🏖️",
        "body": """
        **Your Seasonal Financial Assistant**
        
        Snowbird helps you track days in each state, manage budgets across multiple homes, 
        and get AI-powered financial advice—all while staying compliant with tax regulations.
        
        Perfect for snowbirds splitting time between warm and cold climates!
        """,
        "icon": "home",
        "features": [
            "📍 Track your location daily",
            "⚠️ Monitor tax residency risk", 
            "💰 Manage dual-home budgets",
            "🤖 Get AI financial advice"
        ],
        "action_hint": "Click 'Next' to start your tour!"
    },
    {
        "title": "Step 1: Log Your First Day 📅",
        "body": """
        **Start Tracking Your Location**
        
        After this tour, go to the **📅 Day Tracker** tab and log where you are today. 
        This is crucial for tax residency tracking!
        
        Snowbird monitors your progress toward the 183-day threshold and alerts you 
        when you're getting close to becoming a tax resident.
        """,
        "icon": "map-pin",
        "features": [
            "🏡 Click 'Day Tracker' tab",
            "📍 Select your current state",
            "✅ Click 'Log Day'",
            "📊 Watch your progress update"
        ],
        "action_hint": "💡 Try it: After this tour, click the 'Day Tracker' tab and log your first day!"
    },
    {
        "title": "Step 2: Check Your Progress 📊",
        "body": """
        **Monitor Your Tax Residency Status**
        
        The **📊 Dashboard** shows your current residency progress with visual charts 
        and risk assessments. Check this regularly to stay compliant!
        
        You'll see days remaining before hitting the 183-day threshold for each state.
        """,
        "icon": "bar-chart-3",
        "features": [
            "📊 View your Dashboard",
            "🏜️ See Arizona days logged",
            "❄️ See Minnesota days logged",
            "⚠️ Check risk status"
        ],
        "action_hint": "💡 Try it: The Dashboard tab shows your real-time residency status!"
    },
    {
        "title": "Step 3: Ask Snowbird AI 🤖",
        "body": """
        **Get Personalized Financial Advice**
        
        Visit the **🤖 AI Assistant** tab to ask questions about tax residency, 
        budgeting, or financial planning. Try asking about your specific situation!
        
        Example questions: "How close am I to the tax threshold?" or "Tips for managing dual-home expenses?"
        """,
        "icon": "brain",
        "features": [
            "🤖 Click 'AI Assistant' tab",
            "💬 Type your question",
            "📝 Get personalized advice",
            "👍👎 Rate the response"
        ],
        "action_hint": "💡 Try it: Ask the AI about tax residency strategies for snowbirds!"
    },
    {
        "title": "You're All Set! 🎉",
        "body": """
        **Ready to Manage Your Seasonal Finances**
        
        You now know how to:
        ✅ Log your daily location
        ✅ Monitor your tax residency progress
        ✅ Get AI-powered financial advice
        
        **Pro Tips:**
        • Check your dashboard weekly
        • Set up budget tracking in the Budgets tab
        • Use Settings to customize notifications
        """,
        "icon": "check-circle",
        "features": [
            "🚀 Start logging your days",
            "📱 Bookmark this app",
            "🔔 Set up notifications",
            "❓ Use Help if you need guidance"
        ],
        "action_hint": "🎯 Click 'Get Started!' to begin using Snowbird!"
    }
]

def initialize_onboarding():
    """
    Initialize onboarding state in Streamlit session.
    
    Sets up the necessary session state variables for tracking
    onboarding progress and user completion status.
    """
    if 'onboarded' not in st.session_state:
        st.session_state.onboarded = False
    
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    
    if 'show_onboarding' not in st.session_state:
        st.session_state.show_onboarding = False


def should_show_onboarding() -> bool:
    """
    Determine if onboarding should be displayed.
    
    Returns:
        bool: True if onboarding should be shown, False otherwise.
    """
    initialize_onboarding()
    
    # Show onboarding if user hasn't completed it and hasn't explicitly dismissed it
    return not st.session_state.onboarded and not st.session_state.get('onboarding_dismissed', False)


def render_onboarding_carousel():
    """
    Render the interactive onboarding carousel.
    
    Displays a step-by-step introduction to Snowbird's features
    with navigation controls and progress tracking.
    """
    if not should_show_onboarding():
        return
    
    # Create a modal-style container
    st.markdown("""
    <style>
    .onboarding-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .onboarding-modal {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        max-width: 700px;
        width: 90%;
        max-height: 85vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 2px solid #12BDF2;
    }
    
    .onboarding-header {
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .onboarding-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .onboarding-progress {
        background: #e2e8f0;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
    }
    
    .onboarding-progress-fill {
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .feature-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 0.75rem;
        margin: 1.5rem 0;
    }
    
    .feature-item {
        background: #f8fafc;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        font-size: 0.9rem;
    }
    
    .onboarding-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .step-indicator {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .action-hint {
        background: linear-gradient(90deg, #12BDF2, #06b6d4);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        font-weight: 600;
        text-align: center;
        border-left: 4px solid #0891b2;
    }
    
    .onboarding-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: none;
        border: none;
        font-size: 1.5rem;
        color: #64748b;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get current step
    current_step = st.session_state.onboarding_step
    step_data = ONBOARDING_STEPS[current_step]
    total_steps = len(ONBOARDING_STEPS)
    progress_percent = ((current_step + 1) / total_steps) * 100
    
    # Create columns for modal layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Modal container
        st.markdown(f"""
        <div class="onboarding-modal">
            <div class="onboarding-header">
                <div class="onboarding-title">
                    <i data-lucide="{step_data['icon']}" style="margin-right: 0.5rem;"></i>
                    {step_data['title']}
                </div>
                <div class="onboarding-progress">
                    <div class="onboarding-progress-fill" style="width: {progress_percent}%;"></div>
                </div>
                <div class="step-indicator">Step {current_step + 1} of {total_steps}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Close button
        col_close1, col_close2 = st.columns([6, 1])
        with col_close2:
            if st.button("✕", key="onboarding_close", help="Close tour"):
                st.session_state.onboarded = True
                st.session_state.onboarding_dismissed = True
                st.rerun()
        
        # Step content
        st.markdown(step_data['body'])
        
        # Features list
        if 'features' in step_data:
            st.markdown('<div class="feature-list">', unsafe_allow_html=True)
            for feature in step_data['features']:
                st.markdown(f'<div class="feature-item">{feature}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Action hint
        if 'action_hint' in step_data:
            st.markdown(f'<div class="action-hint">{step_data["action_hint"]}</div>', unsafe_allow_html=True)
        
        # Navigation
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        
        with col_nav1:
            if current_step > 0:
                if st.button("← Previous", key="onboarding_prev"):
                    st.session_state.onboarding_step -= 1
                    st.rerun()
        
        with col_nav2:
            if st.button("Skip Tour", key="onboarding_skip", help="Skip the onboarding tour"):
                st.session_state.onboarded = True
                st.session_state.onboarding_dismissed = True
                st.rerun()
        
        with col_nav3:
            if current_step < total_steps - 1:
                if st.button("Next →", key="onboarding_next", type="primary"):
                    st.session_state.onboarding_step += 1
                    st.rerun()
            else:
                if st.button("Get Started! 🚀", key="onboarding_finish", type="primary"):
                    st.session_state.onboarded = True
                    st.balloons()  # Celebration effect
                    st.rerun()


def render_onboarding_trigger():
    """
    Render a button to restart the onboarding tour.
    
    This can be placed in the sidebar or help section for users
    who want to review the onboarding content again.
    """
    if st.button("🎯 Take Tour Again", help="Restart the onboarding tour"):
        st.session_state.onboarded = False
        st.session_state.onboarding_step = 0
        st.session_state.onboarding_dismissed = False
        st.rerun()


def check_onboarding_completion() -> bool:
    """
    Check if the user has completed onboarding.
    
    Returns:
        bool: True if onboarding is complete, False otherwise.
    """
    initialize_onboarding()
    return st.session_state.onboarded


def mark_onboarding_complete():
    """
    Mark onboarding as complete.
    
    This can be called programmatically if certain conditions are met,
    such as the user logging their first day or setting up their profile.
    """
    st.session_state.onboarded = True


def get_onboarding_analytics() -> Dict[str, Any]:
    """
    Get analytics data about onboarding completion.
    
    Returns:
        Dict[str, Any]: Analytics data including completion status and step progress.
    """
    initialize_onboarding()
    
    return {
        'onboarding_complete': st.session_state.onboarded,
        'current_step': st.session_state.onboarding_step,
        'total_steps': len(ONBOARDING_STEPS),
        'completion_percentage': (st.session_state.onboarding_step / len(ONBOARDING_STEPS)) * 100,
        'dismissed': st.session_state.get('onboarding_dismissed', False)
    }


# Integration helper for analytics
def track_onboarding_event(event_type: str, step_number: int = None):
    """
    Track onboarding events for analytics.
    
    Args:
        event_type (str): Type of event ('start', 'step_complete', 'skip', 'finish')
        step_number (int, optional): Current step number for step-specific events
    """
    try:
        from components.analytics import track_user_action
        
        event_data = {
            'event_type': event_type,
            'total_steps': len(ONBOARDING_STEPS)
        }
        
        if step_number is not None:
            event_data['step_number'] = step_number
            event_data['step_title'] = ONBOARDING_STEPS[step_number]['title']
        
        track_user_action(f'onboarding_{event_type}', event_data)
    except ImportError:
        # Analytics not available, continue silently
        pass


if __name__ == "__main__":
    # Demo/testing functionality
    st.set_page_config(page_title="Onboarding Demo", layout="wide")
    st.title("Snowbird Onboarding Demo")
    
    # Force show onboarding for demo
    st.session_state.onboarded = False
    st.session_state.onboarding_dismissed = False
    
    render_onboarding_carousel()
    
    # Show current state
    st.sidebar.write("**Onboarding State:**")
    st.sidebar.json(get_onboarding_analytics())
