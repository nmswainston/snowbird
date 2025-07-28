
"""
Standard Features for Snowbird app
Provides regular English expressions and messaging
"""

import streamlit as st
import random
from typing import Dict, List


class StandardFeatures:
    """Standard features for the Snowbird app"""

    # Standard greetings and expressions
    GREETINGS = [
        "Hello there! 👋",
        "How's it going? 😊",
        "Good to see you! 👍",
        "Hey, what's up? 🙂",
        "Good morning! ☀️",
        "Hope you're having a great day! 😊"
    ]

    RESPONSES = [
        "Sounds great! 👍",
        "Perfect, looks good! ✅", 
        "Excellent choice! 🎯",
        "Nice work! 👏",
        "Looking good! 📈",
        "That's wonderful! 🌟"
    ]

    SUCCESS_MESSAGES = [
        "Excellent! Success! ✅",
        "Awesome! All set! 🎉",
        "Working perfectly! 👍",
        "Great! Good to go! 🚀",
        "Perfect! All done! ✅",
        "Success achieved! 🎯"
    ]

    # Standard financial terms
    FINANCIAL_TERMS = {
        "budget": "budget",
        "expenses": "expenses",
        "savings": "savings",
        "tax": "tax",
        "residency": "residency",
        "property": "property",
        "utilities": "utilities",
        "insurance": "insurance",
        "maintenance": "maintenance"
    }

    # Standard state references
    STATE_REFERENCES = {
        "Arizona": "Arizona 🌵",
        "Minnesota": "Minnesota ❄️",
        "California": "California 🏖️",
        "Florida": "Florida 🌴",
        "Hawaii": "Hawaii 🌺"
    }

    @staticmethod
    def get_random_greeting() -> str:
        """Get a random standard greeting"""
        return random.choice(StandardFeatures.GREETINGS)

    @staticmethod
    def get_success_message() -> str:
        """Get a random success message"""
        return random.choice(StandardFeatures.SUCCESS_MESSAGES)

    @staticmethod
    def get_response() -> str:
        """Get a random positive response"""
        return random.choice(StandardFeatures.RESPONSES)

    @staticmethod
    def get_financial_term(term: str) -> str:
        """Get standard financial term"""
        return StandardFeatures.FINANCIAL_TERMS.get(term, term)

    @staticmethod
    def get_state_reference(state: str) -> str:
        """Get standard state reference"""
        return StandardFeatures.STATE_REFERENCES.get(state, f"{state} 🏠")

    @staticmethod
    def render_welcome_banner():
        """Render standard welcome banner"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;
                    box-shadow: 0 4px 15px rgba(14,165,233,0.3);">
            <h3 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🏠 Snowbird Financial Assistant
            </h3>
            <p style="color: #dbeafe; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Managing your seasonal residence finances made easy
            </p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_financial_terms():
        """Render financial terms reference"""
        with st.expander("📚 Financial Terms Reference", expanded=False):
            st.markdown("**Common terms used in the app:**")

            for english_term, definition in StandardFeatures.FINANCIAL_TERMS.items():
                st.write(f"• **{english_term.title()}**: {definition}")


def enable_enhanced_features():
    """Enable enhanced features for the app"""
    if 'enhanced_mode' not in st.session_state:
        st.session_state.enhanced_mode = False

    # Toggle button in sidebar
    with st.sidebar:
        st.markdown("---")
        enhanced_mode = st.toggle(
            "✨ Enhanced Features",
            value=st.session_state.enhanced_mode,
            help="Enable additional features and enhanced styling"
        )
        st.session_state.enhanced_mode = enhanced_mode

        if enhanced_mode:
            st.success("Enhanced features active! ✨")
            st.markdown("**Available Features:**")
            st.write("💬 Enhanced greetings")
            st.write("📊 Advanced metrics")
            st.write("🎯 Smart suggestions")
            st.write("🏠 Property insights")


def render_standard_greeting():
    """Render standard greeting"""
    greeting = StandardFeatures.get_random_greeting()
    st.success(greeting)


def render_success_message(message: str):
    """Render success message"""
    success_message = StandardFeatures.get_success_message()
    st.success(f"{success_message} {message}")


def get_state_display_name(state: str) -> str:
    """Get display name for state"""
    return StandardFeatures.get_state_reference(state)
