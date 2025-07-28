
"""
Hawaiian Features - Da Kine implementation for Snowbird app
Adds authentic Hawaiian/pidgin elements and island vibes
"""

import streamlit as st
import random
from typing import Dict, List

class HawaiianFeatures:
    """Da kine Hawaiian features for the Snowbird app"""
    
    # Hawaiian/Pidgin greetings and expressions
    GREETINGS = [
        "Aloha brah! 🤙",
        "Howzit going, cuz? 🌺",
        "Shoots, bruddah! 🏄‍♂️",
        "Eh, wassup? 🌴",
        "Aloha kakahiaka! ☀️",
        "Good vibes, yeah? 🌊"
    ]
    
    RESPONSES = [
        "Rajah dat! 🤙",
        "Shoots, sounds good! 🏄‍♂️", 
        "Da kine, perfect! 🌺",
        "Chee hoo! Nice one! 🤙",
        "Solid, bruddah! 🌴",
        "Ono! Looking good! 🌊"
    ]
    
    SUCCESS_MESSAGES = [
        "Broke da mouth! Success! 🤙",
        "Chee hoo! All set! 🏄‍♂️",
        "Da kine working perfect! 🌺",
        "Rajah! Good to go! 🌴",
        "Shoots! All pau! ✅",
        "Aloha spirit activated! 🌊"
    ]
    
    # Island-themed financial terms
    FINANCIAL_PIDGIN = {
        "budget": "money kine",
        "expenses": "spending da cash",
        "savings": "saving da coins",
        "tax": "government kine",
        "residency": "where stay living",
        "property": "da house",
        "utilities": "light bill an dat",
        "insurance": "protection kine",
        "maintenance": "fix up da place"
    }
    
    # State nicknames Hawaiian style
    STATE_NICKNAMES = {
        "Arizona": "Da Desert Place 🌵",
        "Minnesota": "Da Cold Place ❄️",
        "California": "Da Mainland West 🏖️",
        "Florida": "Da Other Warm Place 🐊",
        "Hawaii": "Da Aina 🌺"
    }
    
    @staticmethod
    def get_random_greeting() -> str:
        """Get a random Hawaiian greeting"""
        return random.choice(HawaiianFeatures.GREETINGS)
    
    @staticmethod
    def get_success_message() -> str:
        """Get a random success message"""
        return random.choice(HawaiianFeatures.SUCCESS_MESSAGES)
    
    @staticmethod
    def get_response() -> str:
        """Get a random positive response"""
        return random.choice(HawaiianFeatures.RESPONSES)
    
    @staticmethod
    def translate_to_pidgin(text: str) -> str:
        """Translate financial terms to Hawaiian pidgin"""
        for english, pidgin in HawaiianFeatures.FINANCIAL_PIDGIN.items():
            text = text.replace(english, pidgin)
        return text
    
    @staticmethod
    def get_state_nickname(state: str) -> str:
        """Get Hawaiian-style nickname for state"""
        return HawaiianFeatures.STATE_NICKNAMES.get(state, f"Da {state} Place 🏝️")
    
    @staticmethod
    def render_island_vibes_banner():
        """Render island vibes banner"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #fff200 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;
                    box-shadow: 0 4px 15px rgba(255,107,53,0.3);">
            <h3 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🌺 Island Vibes Mode Active 🤙
            </h3>
            <p style="color: #fff3cd; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Living da snowbird life with aloha spirit! 🏄‍♂️🌴
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_pidgin_translator():
        """Render pidgin translator widget"""
        with st.expander("🗣️ Pidgin Translator - Da Kine Helper", expanded=False):
            st.markdown("**Translate your financial terms to Hawaiian pidgin:**")
            
            english_text = st.text_input(
                "Enter English text:",
                placeholder="Enter budget, expenses, tax residency, etc."
            )
            
            if english_text:
                pidgin_text = HawaiianFeatures.translate_to_pidgin(english_text)
                st.success(f"**Pidgin:** {pidgin_text}")
    
    @staticmethod
    def render_surf_report_style_metrics(metric_name: str, value: str, delta: str = ""):
        """Render metrics in surf report style"""
        wave_emoji = "🌊" if "tax" in metric_name.lower() else "🏄‍♂️"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%); 
                    padding: 1.5rem; border-radius: 12px; text-align: center; margin: 0.5rem 0;
                    box-shadow: 0 4px 15px rgba(0,188,212,0.3);">
            <div style="color: white; font-size: 0.9rem; margin-bottom: 0.5rem;">
                {wave_emoji} {metric_name}
            </div>
            <div style="color: white; font-size: 2rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                {value}
            </div>
            {f'<div style="color: #b2ebf2; font-size: 0.8rem; margin-top: 0.5rem;">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

def enable_hawaiian_mode():
    """Enable Hawaiian/pidgin mode for the app"""
    if 'hawaiian_mode' not in st.session_state:
        st.session_state.hawaiian_mode = False
    
    # Toggle button in sidebar
    with st.sidebar:
        st.markdown("---")
        hawaiian_mode = st.toggle(
            "🌺 Island Vibes Mode",
            value=st.session_state.hawaiian_mode,
            help="Enable Hawaiian pidgin and island styling"
        )
        st.session_state.hawaiian_mode = hawaiian_mode
        
        if hawaiian_mode:
            st.success("Aloha! 🤙 Island mode active!")
            st.markdown("**Da Kine Features:**")
            st.write("🗣️ Pidgin translations")
            st.write("🌺 Island-style greetings")
            st.write("🏄‍♂️ Surf report metrics")
            st.write("🌴 Hawaiian nicknames")

def render_hawaiian_greeting():
    """Render Hawaiian greeting if mode is enabled"""
    if st.session_state.get('hawaiian_mode', False):
        greeting = HawaiianFeatures.get_random_greeting()
        st.success(greeting)

def render_island_success(message: str):
    """Render success message with island flavor"""
    if st.session_state.get('hawaiian_mode', False):
        island_message = HawaiianFeatures.get_success_message()
        st.success(f"{island_message} {message}")
    else:
        st.success(message)

def get_hawaiian_state_name(state: str) -> str:
    """Get Hawaiian-style state name if mode enabled"""
    if st.session_state.get('hawaiian_mode', False):
        return HawaiianFeatures.get_state_nickname(state)
    return state
