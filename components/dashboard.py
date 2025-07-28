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

    # Combined Quick Location Logging Card
    with st.container():
        # Add light-blue border styling to the container
        st.markdown("""
        <div style="border: 2px solid #e3f2fd; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; background: linear-gradient(135deg, #f8fdff 0%, #e3f2fd 100%);">
        """, unsafe_allow_html=True)
        
        # Mini-label above the controls
        st.markdown("**Log your location quickly:**")
        st.write("")  # Add small spacing
        
        # Create horizontal layout for location picker and button
        # On mobile, these will stack vertically due to Streamlit's responsive design
        location_col, button_col = st.columns([2, 1])
        
        with location_col:
            # Location dropdown picker
            current_location = st.selectbox(
                "Select your current location:", 
                list(st.session_state.states.keys()),
                key="quick_location_picker",
                label_visibility="collapsed"  # Hide label since we have the mini-label above
            )
        
        with button_col:
            # Log Today button - matches the current quick action functionality
            if st.button("📍 Log Today", type="primary", use_container_width=True, key="quick_log_button"):
                # Import the data model for logging functionality
                from utils.data_models import SnowbirdData
                snowbird_data = SnowbirdData()
                # Log the selected location for today's date
                import datetime
                success, message = snowbird_data.add_day_log(current_location, datetime.date.today().isoformat())
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.warning(message)
        
        # Close the styled container div
        st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced key metrics section with st.metric components
    st.markdown("### 📊 Key Metrics Overview")
    st.write("")  # Add spacing

    # Create responsive grid layout (3 columns on desktop, adapts to mobile)
    col1, col2, col3 = st.columns(3)

    # Get current data for metrics
    az_days = st.session_state.states.get("Arizona", 0)
    mn_days = st.session_state.states.get("Minnesota", 0)
    threshold = st.session_state.tax_threshold

    # Calculate remaining days for primary state (highest count)
    primary_state = "Arizona" if az_days >= mn_days else "Minnesota"
    primary_days = max(az_days, mn_days)
    days_remaining = max(0, threshold - primary_days)

    with col1:
        # Arizona days metric with desert emoji
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        st.metric(
            label="🏜️ Days in Arizona",
            value=az_days,
            delta=f"{threshold - az_days} until threshold" if az_days < threshold else "⚠️ Over threshold"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Minnesota days metric with snow emoji
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        st.metric(
            label="❄️ Days in Minnesota",
            value=mn_days,
            delta=f"{threshold - mn_days} until threshold" if mn_days < threshold else "⚠️ Over threshold"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Tax threshold progress visualization with progress bar
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        
        # Calculate percentage of 183-day allowance used
        pct = min(primary_days / 183, 1.0)
        percentage_used = pct * 100
        
        # Display the progress section with label
        st.markdown("**⚠️ Tax Threshold Progress**")
        
        # Add tooltip with the raw number for reference
        with st.container():
            # Progress bar showing percentage toward 183-day threshold
            st.progress(pct, text=f"Days logged: {primary_days}/183")
            
            # Small label showing percentage used
            st.caption(f"You've used {percentage_used:.1f}% of your 183-day allowance")
            
            # Tooltip showing the exact days remaining (hidden behind hover)
            if st.button("ℹ️", key="threshold_tooltip", help=f"Days remaining: {days_remaining} | Primary state: {primary_state}"):
                st.info(f"Exact details: {days_remaining} days remaining until threshold in {primary_state}")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Add spacing between sections
    st.write("")
    st.markdown("---")
    st.write("")

    # Tax residency progress section
    st.markdown("### 📈 Tax Residency Progress")
    st.write("")

    # Calculate progress percentage for primary state
    progress_percentage = min(primary_days / threshold, 1.0) if threshold > 0 else 0

    # Color coding for progress bar
    if progress_percentage < 0.7:
        progress_color = "🟢 Safe Zone"
        bar_color = "#4CAF50"
    elif progress_percentage < 0.9:
        progress_color = "🟡 Monitor Closely"
        bar_color = "#FF9800"
    else:
        progress_color = "🔴 High Risk"
        bar_color = "#F44336"

    # Create progress bar with custom styling
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="margin-bottom: 1rem; color: #333;">
            🎯 Progress Toward 183-Day Threshold in {primary_state}
        </h4>
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>{primary_days}</strong> of <strong>{threshold}</strong> days 
            ({progress_percentage*100:.1f}%) - Status: <strong>{progress_color}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(progress_percentage, text=f"{primary_days}/{threshold} days in {primary_state}")

    # Add spacing
    st.write("")
    st.markdown("---")

    # Additional insights section with improved layout
    st.markdown("### ✨ Quick Insights")
    st.write("")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        # Tax optimization score
        tax_score = max(0, min(100, 100 - (progress_percentage * 100)))
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center;">
        """, unsafe_allow_html=True)
        st.markdown(f"**🎯 Tax Optimization**")
        st.markdown(f"<h2 style='color: #2e7d32; margin: 0.5rem 0;'>{tax_score:.0f}%</h2>", unsafe_allow_html=True)
        st.markdown("Compliance Score")
        st.markdown("</div>", unsafe_allow_html=True)

    with insight_col2:
        # Days available
        total_logged = sum(st.session_state.states.values())
        days_available = 365 - total_logged
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center;">
        """, unsafe_allow_html=True)
        st.markdown(f"**📅 Days Available**")
        st.markdown(f"<h2 style='color: #1976d2; margin: 0.5rem 0;'>{days_available}</h2>", unsafe_allow_html=True)
        st.markdown("Remaining in Year")
        st.markdown("</div>", unsafe_allow_html=True)

    with insight_col3:
        # Next recommendation
        if days_remaining < 30:
            recommendation = "Plan location change"
            rec_color = "#f57c00"
        elif days_remaining < 60:
            recommendation = "Monitor closely"
            rec_color = "#fbc02d"
        else:
            recommendation = "Continue current plan"
            rec_color = "#388e3c"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center;">
        """, unsafe_allow_html=True)
        st.markdown(f"**🔮 Recommendation**")
        st.markdown(f"<h3 style='color: {rec_color}; margin: 0.5rem 0; font-size: 1rem;'>{recommendation}</h3>", unsafe_allow_html=True)
        st.markdown(f"{days_remaining} days buffer")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    snowbird_data = SnowbirdData()

    # Add more spacing
    st.write("")
    st.markdown("---")
    st.write("")

    # Enhanced status overview section
    st.markdown('<h3><i data-lucide="bar-chart-3" class="icon"></i>📋 Detailed Status Overview</h3>', unsafe_allow_html=True)
    st.write("")

    # Create metrics in a responsive grid
    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        total_days = sum(st.session_state.states.values())
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                    padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        st.metric("📊 Total Days Logged", total_days, delta=f"Out of 365 days")
        st.markdown("</div>", unsafe_allow_html=True)

    with status_col2:
        days_left = (365 - total_days) if total_days < 365 else 0
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                    padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        st.metric("📅 Days Remaining in Year", days_left, delta=f"{(days_left/365)*100:.1f}% of year left")
        st.markdown("</div>", unsafe_allow_html=True)

    with status_col3:
        threshold = st.session_state.tax_threshold
        closest_to_threshold = max(st.session_state.states.values()) if st.session_state.states.values() else 0
        risk_level = "🔴 High" if closest_to_threshold >= threshold * 0.9 else "🟡 Medium" if closest_to_threshold >= threshold * 0.75 else "🟢 Low"
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                    padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0;">
        """, unsafe_allow_html=True)
        st.metric("⚠️ Tax Risk Level", risk_level, delta=f"{closest_to_threshold} days in primary state")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # Add spacing after metrics

    # Add spacing
    st.markdown("---")
    st.write("")

    # Enhanced state residency status section
    st.markdown('<h3><i data-lucide="map-pin" class="icon"></i>🗺️ State-by-State Breakdown</h3>', unsafe_allow_html=True)
    st.write("")

    for state, days in st.session_state.states.items():
        status_text, status_class = snowbird_data.get_tax_status(days, st.session_state.tax_threshold)
        progress = min(days / st.session_state.tax_threshold, 1.0)
        days_remaining = max(0, st.session_state.tax_threshold - days)

        # Enhanced state card with better styling
        state_icon = "🌵" if "Arizona" in state else "❄️" if "Minnesota" in state else "🏠"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; 
                    border-left: 4px solid {'#4CAF50' if status_text == 'SAFE' else '#FF9800' if status_text in ['CAUTION', 'CRITICAL'] else '#F44336'};">
            <h4 style="margin-bottom: 1rem; color: #333;">
                {state_icon} {state}
            </h4>
        </div>
        """, unsafe_allow_html=True)

        # Two-column layout for state details
        state_col1, state_col2 = st.columns([2, 1])

        with state_col1:
            # Progress bar with enhanced styling
            st.progress(progress, text=f"{days} of {st.session_state.tax_threshold} days ({progress*100:.1f}%)")

            # Status message with appropriate styling
            if status_text == "SAFE":
                st.success(f"✅ **{status_text}** - {days_remaining} days remaining until threshold")
            elif status_text in ["CAUTION", "CRITICAL"]:
                st.warning(f"⚠️ **{status_text}** - Only {days_remaining} days remaining!")
            else:
                st.error(f"🚨 **{status_text}** - Tax residency established")

        with state_col2:
            # Enhanced metric display
            delta_text = f"+{days_remaining} safe days" if days_remaining > 0 else "Over threshold!"
            delta_color = "normal" if days_remaining > 0 else "inverse"
            st.metric(
                "Days Logged", 
                days, 
                delta=delta_text,
                delta_color=delta_color
            )

        st.write("")  # Add spacing between states

    # Add spacing
    st.markdown("---")
    st.write("")

    # Enhanced financial overview section
    st.markdown('<h3><i data-lucide="dollar-sign" class="icon"></i>💰 Financial Summary</h3>', unsafe_allow_html=True)
    st.write("")

    # Financial metrics in responsive grid
    fin_col1, fin_col2 = st.columns(2)

    with fin_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 1.5rem; border-radius: 12px;">
        """, unsafe_allow_html=True)
        st.markdown('**🏠 Monthly Home Budgets**')
        st.write("")

        total_all_budgets = 0
        for state, budget in st.session_state.home_budgets.items():
            total_budget = sum(budget.values())
            total_all_budgets += total_budget
            state_icon = "🌵" if "Arizona" in state else "❄️"
            st.metric(f"{state_icon} {state}", f"${total_budget:,}", delta="per month")

        st.write("---")
        st.metric("**📊 Total Monthly Budget**", f"${total_all_budgets:,}", delta="All properties")
        st.markdown("</div>", unsafe_allow_html=True)

    with fin_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    padding: 1.5rem; border-radius: 12px;">
        """, unsafe_allow_html=True)
        st.markdown('**📅 Seasonal Expenses**')
        st.write("")

        total_seasonal = sum(st.session_state.seasonal_cash_flow.values())
        for category, amount in st.session_state.seasonal_cash_flow.items():
            # Add emojis for different expense categories
            if "Travel" in category:
                emoji = "✈️"
            elif "Healthcare" in category:
                emoji = "🏥"
            elif "Insurance" in category:
                emoji = "🛡️"
            else:
                emoji = "💸"
            st.metric(f"{emoji} {category}", f"${amount:,}", delta="per month")

        st.write("---")
        st.metric("**📊 Total Seasonal**", f"${total_seasonal:,}", delta="per month")
        st.markdown("</div>", unsafe_allow_html=True)

    # Add final spacing
    st.write("")
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