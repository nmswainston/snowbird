
import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_dashboard():
    """Render the main dashboard tab"""
    snowbird_data = SnowbirdData()
    
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="bar-chart-3" class="icon"></i>Current Status Overview</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        total_days = sum(st.session_state.states.values())
        st.metric("Total Days Logged", total_days)

    with col2:
        days_left = (365 - total_days) if total_days < 365 else 0
        st.metric("Days Remaining in Year", days_left)

    with col3:
        threshold = st.session_state.tax_threshold
        closest_to_threshold = max(st.session_state.states.values())
        risk_level = "High" if closest_to_threshold >= threshold * 0.9 else "Medium" if closest_to_threshold >= threshold * 0.75 else "Low"
        st.metric("Tax Risk Level", risk_level)

    st.markdown('</div>', unsafe_allow_html=True)

    # State residency status
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="map-pin" class="icon"></i>State Residency Status</h3>', unsafe_allow_html=True)

    for state, days in st.session_state.states.items():
        status_text, status_class = snowbird_data.get_tax_status(days, st.session_state.tax_threshold)
        progress = min(days / st.session_state.tax_threshold, 1.0)
        days_remaining = max(0, st.session_state.tax_threshold - days)

        state_col1, state_col2 = st.columns([3, 1])
        with state_col1:
            state_icon = "🌵" if "Arizona" in state else "❄️" if "Minnesota" in state else "🏠"
            st.write(f"**{state_icon} {state}**")
            st.progress(progress, text=f"{days}/{st.session_state.tax_threshold} days ({progress*100:.1f}%)")
            
            if status_text == "SAFE":
                st.success(f"✅ {status_text} - {days_remaining} days remaining")
            elif status_text in ["CAUTION", "CRITICAL"]:
                st.warning(f"⚠️ {status_text} - {days_remaining} days remaining")
            else:
                st.error(f"🚨 {status_text} - Tax residency established")
        
        with state_col2:
            st.metric("Current Days", days, delta=f"+{days_remaining} safe" if days_remaining > 0 else "⚠️ Over limit")

    st.markdown('</div>', unsafe_allow_html=True)

    # Financial overview
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.markdown('<h3><i data-lucide="dollar-sign" class="icon"></i>Financial Overview</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('**<i data-lucide="home" class="icon"></i>Monthly Home Budgets**', unsafe_allow_html=True)
        for state, budget in st.session_state.home_budgets.items():
            total_budget = sum(budget.values())
            st.write(f"• {state}: ${total_budget:,}")

    with col2:
        st.markdown('**<i data-lucide="calendar" class="icon"></i>Seasonal Expenses**', unsafe_allow_html=True)
        total_seasonal = sum(st.session_state.seasonal_cash_flow.values())
        st.write(f"• Total Monthly: ${total_seasonal:,}")
        for category, amount in st.session_state.seasonal_cash_flow.items():
            st.write(f"  - {category}: ${amount}")

    st.markdown('</div>', unsafe_allow_html=True)
