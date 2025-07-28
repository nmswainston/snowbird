"""
Island Weather Widget - Da Kine Weather for Snowbirds
Adds tropical weather vibes to the app
"""

import streamlit as st
import random
from datetime import datetime

class IslandWeatherWidget:
    """Island-style weather and vibes widget"""

    WEATHER_VIBES = [
        {"condition": "🌞 Sunny Vibes", "vibe": "Perfect for da beach!", "color": "#ffeb3b"},
        {"condition": "🌊 Wave Action", "vibe": "Surf's up, bruddah!", "color": "#00bcd4"},
        {"condition": "🌺 Tropical Breeze", "vibe": "Aloha spirit flowing!", "color": "#e91e63"},
        {"condition": "🌴 Palm Tree Weather", "vibe": "Island time activated!", "color": "#4caf50"},
        {"condition": "🤙 Da Kine Perfect", "vibe": "Everything stay good!", "color": "#ff9800"},
        {"condition": "🏄‍♂️ Surf Report Good", "vibe": "Waves looking clean!", "color": "#3f51b5"}
    ]

    FINANCIAL_WEATHER = [
        {"status": "🌈 Budget Rainbow", "message": "Your finances stay colorful!", "advice": "Keep riding da wave!"},
        {"status": "⛅ Tax Cloud Passing", "message": "Small kine tax concerns", "advice": "No worries, just monitor"},
        {"status": "☀️ Savings Sunshine", "message": "Money growing like coconuts!", "advice": "Aloha to good planning!"},
        {"status": "🌊 Cash Flow Tide", "message": "Money flowing like da ocean", "advice": "Ride da current, brah!"}
    ]

    @staticmethod
    def render_island_weather():
        """Render island weather widget"""
        if not st.session_state.get('enhanced_mode', False):
            return

        st.markdown("### 🌺 Island Vibes Weather Report")

        # Random weather vibe
        weather = random.choice(IslandWeatherWidget.WEATHER_VIBES)
        financial = random.choice(IslandWeatherWidget.FINANCIAL_WEATHER)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {weather['color']}22 0%, {weather['color']}11 100%); 
                        padding: 1rem; border-radius: 12px; border-left: 4px solid {weather['color']};">
                <h4 style="margin: 0; color: #333;">{weather['condition']}</h4>
                <p style="margin: 0.5rem 0 0 0; color: #666;">{weather['vibe']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00bcd422 0%, #00bcd411 100%); 
                        padding: 1rem; border-radius: 12px; border-left: 4px solid #00bcd4;">
                <h4 style="margin: 0; color: #333;">{financial['status']}</h4>
                <p style="margin: 0.5rem 0 0 0; color: #666;">{financial['message']}</p>
                <small style="color: #888;">{financial['advice']}</small>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def render_tide_chart():
        """Render financial tide chart Hawaiian style"""
        if not st.session_state.get('enhanced_mode', False):
            return

        with st.expander("🌊 Financial Tide Chart - Da Kine Money Flow", expanded=False):
            st.markdown("**Your money flow like da ocean tides, bruddah!**")

            # Mock tide data based on budget
            budgets = st.session_state.get('home_budgets', {})
            if budgets:
                total_budget = sum(sum(budget.values()) for budget in budgets.values())

                # Create simple tide visualization
                tide_level = "🌊🌊🌊" if total_budget > 2000 else "🌊🌊" if total_budget > 1000 else "🌊"

                st.markdown(f"""
                **Current Tide Level:** {tide_level}

                **Financial Surf Report:**
                - High Tide: ${total_budget:,}/month flowing out
                - Best Time to Save: When expenses stay low
                - Wave Conditions: {"Solid" if total_budget < 3000 else "Big waves, watch out!"}

                **Local Knowledge:** 
                Keep your financial board waxed and ready for any conditions! 🏄‍♂️
                """)

def render_island_widgets():
    """Render all island-themed widgets"""
    IslandWeatherWidget.render_island_weather()
    IslandWeatherWidget.render_tide_chart()