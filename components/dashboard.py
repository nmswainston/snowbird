import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_dashboard():
    """Render the enhanced premium dashboard"""
    st.markdown('<div class="winter-card fade-in">', unsafe_allow_html=True)

    # Premium header section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: var(--surface-gradient); border-radius: 16px; border: 1px solid var(--border-light);">
        <h2 style="color: var(--primary); font-weight: 700; font-size: 1.5rem; margin-bottom: 0.5rem; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            <i data-lucide="dashboard" class="icon-large"></i>
            Financial Command Center
        </h2>
        <p style="color: var(--text-secondary); font-size: 1rem; opacity: 0.9;">Your complete snowbird lifestyle overview</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced quick stats with premium styling
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Days This Year", "127", "↗️ +12 this month", "calendar")

    with col2:
        render_metric_card("Current Location", "Arizona", "✅ Safe for taxes", "map-pin")

    with col3:
        render_metric_card("Tax Status", "Compliant", "🛡️ 183-day rule", "shield-check")

    with col4:
        render_metric_card("Savings", "$2,847", "💰 +$240 this month", "dollar-sign")

    # Additional premium features section
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1.5rem; background: var(--overlay-light); backdrop-filter: blur(10px); border-radius: 16px; border: 1px solid var(--border-light);">
        <h3 style="color: var(--primary); font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center;">
            <i data-lucide="sparkles" class="icon" style="margin-right: 0.5rem;"></i>
            Premium Insights
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div style="padding: 1rem; background: var(--surface-gradient); border-radius: 12px; border: 1px solid var(--border-light);">
                <div style="color: var(--success); font-weight: 600; margin-bottom: 0.5rem;">
                    <i data-lucide="trending-up" class="icon"></i>Tax Optimization Score
                </div>
                <div style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700;">94% Excellent</div>
            </div>
            <div style="padding: 1rem; background: var(--surface-gradient); border-radius: 12px; border: 1px solid var(--border-light);">
                <div style="color: var(--info); font-weight: 600; margin-bottom: 0.5rem;">
                    <i data-lucide="clock" class="icon"></i>Remaining Days Available
                </div>
                <div style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700;">238 days</div>
            </div>
            <div style="padding: 1rem; background: var(--surface-gradient); border-radius: 12px; border: 1px solid var(--border-light);">
                <div style="color: var(--warning); font-weight: 600; margin-bottom: 0.5rem;">
                    <i data-lucide="alert-triangle" class="icon"></i>Next Recommendation
                </div>
                <div style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700;">Plan return trip</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

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
def render_metric_card(title, value, delta, icon):
    """Helper function to render a metric card with sleek styling"""
    st.markdown(f"""
    <div style="padding: 1rem; background: var(--surface-gradient); border-radius: 12px; border: 1px solid var(--border-light); transition: transform 0.3s ease-in-out; width: 100%; box-sizing: border-box;">
        <div style="color: var(--text-secondary); font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
            <i data-lucide="{icon}" class="icon" style="margin-right: 0.5rem;"></i>{title}
        </div>
        <div style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700;">{value}</div>
        <div style="color: var(--text-secondary); font-size: 0.875rem;">{delta}</div>
    </div>
    """, unsafe_allow_html=True)