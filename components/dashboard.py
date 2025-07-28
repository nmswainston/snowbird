import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_dashboard():
    """Render the enhanced premium dashboard with configurable widgets"""
    
    # Initialize default widget configuration if not present
    if 'widgets' not in st.session_state:
        st.session_state.widgets = {
            "quick_location_logger": True,
            "key_metrics": True,
            "tax_progress": True,
            "quick_insights": True,
            "status_overview": True,
            "state_breakdown": True,
            "financial_summary": True,
            "ai_tips": False,
            "expense_sparkline": False,
            "reminders": False
        }
    
    st.markdown('<div class="winter-card fade-in">', unsafe_allow_html=True)

    # Premium header section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem; padding: 2rem; background: var(--surface-gradient); border-radius: 16px; border: 1px solid var(--border-light);">
        <h2 style="color: var(--primary); font-weight: 700; font-size: 1.5rem; margin-bottom: 0.75rem; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            <i data-lucide="dashboard" class="icon-large"></i>
            Financial Command Center
        </h2>
        <p style="color: var(--text-secondary); font-size: 1rem; opacity: 0.9;">Your complete snowbird lifestyle overview</p>
    </div>
    """, unsafe_allow_html=True)

    # Widget: Quick Location Logger - render only if enabled
    if st.session_state.widgets.get("quick_location_logger", True):
        with st.container():
            # Add light-blue border styling to the container
            st.markdown("""
            <div style="border: 2px solid #e3f2fd; border-radius: 12px; padding: 2rem; margin-bottom: 2.5rem; background: linear-gradient(135deg, #f8fdff 0%, #e3f2fd 100%);">
            """, unsafe_allow_html=True)

            # Mini-label above the controls
            st.markdown("**Log your location quickly:**")
            st.markdown("<br>", unsafe_allow_html=True)

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

    # Widget: Key Metrics Overview - render only if enabled
    if st.session_state.widgets.get("key_metrics", True):
        st.markdown("""
        <div style="margin: 3rem 0 2.5rem 0;">
            <h3 style="
                color: var(--primary, #0891B2);
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 2rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            ">
                📊 Key Metrics Overview
            </h3>
        </div>
        """, unsafe_allow_html=True)

    # Create responsive grid layout with enhanced spacing
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")

    # Get current data for metrics
    az_days = st.session_state.states.get("Arizona", 0)
    mn_days = st.session_state.states.get("Minnesota", 0)
    threshold = st.session_state.tax_threshold

    # Calculate remaining days for primary state (highest count)
    primary_state = "Arizona" if az_days >= mn_days else "Minnesota"
    primary_days = max(az_days, mn_days)
    days_remaining = max(0, threshold - primary_days)

    with col1:
        # Arizona days metric with enhanced desert theme
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 20%, #fb923c 100%); 
            padding: 1.75rem; 
            border-radius: 20px; 
            margin-bottom: 1.5rem; 
            border: 1px solid rgba(251, 146, 60, 0.2);
            box-shadow: 0 8px 32px rgba(251, 146, 60, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 48px rgba(251, 146, 60, 0.25), 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(251, 146, 60, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
        """, unsafe_allow_html=True)
        st.metric(
            label="🏜️ Days in Arizona",
            value=az_days,
            delta=f"{threshold - az_days} until threshold" if az_days < threshold else "⚠️ Over threshold"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Minnesota days metric with enhanced winter theme
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f0f9ff 0%, #bae6fd 20%, #0ea5e9 100%); 
            padding: 1.75rem; 
            border-radius: 20px; 
            margin-bottom: 1.5rem; 
            border: 1px solid rgba(14, 165, 233, 0.2);
            box-shadow: 0 8px 32px rgba(14, 165, 233, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 48px rgba(14, 165, 233, 0.25), 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(14, 165, 233, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
        """, unsafe_allow_html=True)
        st.metric(
            label="❄️ Days in Minnesota",
            value=mn_days,
            delta=f"{threshold - mn_days} until threshold" if mn_days < threshold else "⚠️ Over threshold"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Tax threshold progress with enhanced styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fefce8 0%, #fde047 20%, #eab308 100%); 
            padding: 1.75rem; 
            border-radius: 20px; 
            margin-bottom: 1.5rem; 
            border: 1px solid rgba(234, 179, 8, 0.2);
            box-shadow: 0 8px 32px rgba(234, 179, 8, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 48px rgba(234, 179, 8, 0.25), 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(234, 179, 8, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
        """, unsafe_allow_html=True)

        # Calculate percentage of 183-day allowance used
        pct = min(primary_days / 183, 1.0)
        percentage_used = pct * 100

        # Display the progress section with enhanced label
        st.markdown("**⚠️ Tax Threshold Progress**")

        # Enhanced progress container
        with st.container():
            # Progress bar showing percentage toward 183-day threshold
            st.progress(pct, text=f"Days logged: {primary_days}/183")

            # Enhanced caption with better typography
            st.caption(f"You've used {percentage_used:.1f}% of your 183-day allowance")

            # Enhanced tooltip button
            if st.button("ℹ️", key="threshold_tooltip", help=f"Days remaining: {days_remaining} | Primary state: {primary_state}"):
                st.info(f"Exact details: {days_remaining} days remaining until threshold in {primary_state}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Add spacing between sections
    if st.session_state.widgets.get("key_metrics", True):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br><br>", unsafe_allow_html=True)

    # Widget: Tax Residency Progress - render only if enabled
    if st.session_state.widgets.get("tax_progress", True):
        st.markdown("### 📈 Tax Residency Progress")
        st.markdown("<br>", unsafe_allow_html=True)

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

    # Add spacing after tax progress widget
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")

    # Widget: Quick Insights - render only if enabled
    if st.session_state.widgets.get("quick_insights", True):
        st.markdown("""
        <div style="margin: 3.5rem 0 2.5rem 0;">
            <h3 style="
                color: var(--primary, #0891B2);
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 2rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            ">
                ✨ Quick Insights
            </h3>
        </div>
        """, unsafe_allow_html=True)

    insight_col1, insight_col2, insight_col3 = st.columns([1, 1, 1], gap="large")

    with insight_col1:
        # Tax optimization score with enhanced green theme
        tax_score = max(0, min(100, 100 - (progress_percentage * 100)))
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 20%, #22c55e 100%); 
            padding: 2rem; 
            border-radius: 20px; 
            text-align: center;
            border: 1px solid rgba(34, 197, 94, 0.2);
            box-shadow: 0 8px 32px rgba(34, 197, 94, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-6px) scale(1.02)'; this.style.boxShadow='0 16px 48px rgba(34, 197, 94, 0.25), 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(34, 197, 94, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 1rem; color: rgba(22, 101, 52, 0.9);">🎯 Tax Optimization</div>
            <div style="color: #166534; margin: 1rem 0; font-size: 2.5rem; font-weight: 800; line-height: 1;">{tax_score:.0f}%</div>
            <div style="color: rgba(22, 101, 52, 0.8); font-size: 0.9rem; font-weight: 500;">Compliance Score</div>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        # Days available with enhanced blue theme
        total_logged = sum(st.session_state.states.values())
        days_available = 365 - total_logged
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #eff6ff 0%, #bfdbfe 20%, #3b82f6 100%); 
            padding: 2rem; 
            border-radius: 20px; 
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.2);
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-6px) scale(1.02)'; this.style.boxShadow='0 16px 48px rgba(59, 130, 246, 0.25), 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 1rem; color: rgba(29, 78, 216, 0.9);">📅 Days Available</div>
            <div style="color: #1d4ed8; margin: 1rem 0; font-size: 2.5rem; font-weight: 800; line-height: 1;">{days_available}</div>
            <div style="color: rgba(29, 78, 216, 0.8); font-size: 0.9rem; font-weight: 500;">Remaining in Year</div>
        </div>
        """, unsafe_allow_html=True)

    with insight_col3:
        # Enhanced recommendation with dynamic theming
        if days_remaining < 30:
            recommendation = "Plan location change"
            rec_color = "#dc2626"
            bg_gradient = "linear-gradient(135deg, #fef2f2 0%, #fecaca 20%, #ef4444 100%)"
            border_color = "rgba(239, 68, 68, 0.2)"
            shadow_color = "rgba(239, 68, 68, 0.15)"
        elif days_remaining < 60:
            recommendation = "Monitor closely"
            rec_color = "#d97706"
            bg_gradient = "linear-gradient(135deg, #fffbeb 0%, #fed7aa 20%, #f59e0b 100%)"
            border_color = "rgba(245, 158, 11, 0.2)"
            shadow_color = "rgba(245, 158, 11, 0.15)"
        else:
            recommendation = "Continue current plan"
            rec_color = "#059669"
            bg_gradient = "linear-gradient(135deg, #ecfdf5 0%, #a7f3d0 20%, #10b981 100%)"
            border_color = "rgba(16, 185, 129, 0.2)"
            shadow_color = "rgba(16, 185, 129, 0.15)"

        st.markdown(f"""
        <div style="
            background: {bg_gradient}; 
            padding: 2rem; 
            border-radius: 20px; 
            text-align: center;
            border: 1px solid {border_color};
            box-shadow: 0 8px 32px {shadow_color}, 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-6px) scale(1.02)'; this.style.boxShadow='0 16px 48px {shadow_color.replace('0.15', '0.25')}, 0 4px 16px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px {shadow_color}, 0 2px 8px rgba(0, 0, 0, 0.1)';">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
            "></div>
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 1rem; color: rgba(0, 0, 0, 0.8);">🔮 Recommendation</div>
            <div style="color: {rec_color}; margin: 1rem 0; font-size: 1.1rem; font-weight: 700; line-height: 1.2;">{recommendation}</div>
            <div style="color: rgba(0, 0, 0, 0.7); font-size: 0.9rem; font-weight: 500;">{days_remaining} days buffer</div>
        </div>
        """, unsafe_allow_html=True)

    # Widget: AI Tips - render only if enabled (new optional widget)
    if st.session_state.widgets.get("ai_tips", False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h3><i data-lucide="bot" class="icon"></i>🤖 AI Tips</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI Tips placeholder content
        tip_col1, tip_col2 = st.columns(2)
        
        with tip_col1:
            st.info("💡 **Planning Tip**: Consider your travel schedule when approaching the 183-day threshold.")
        
        with tip_col2:
            st.info("💰 **Budget Tip**: Track seasonal expenses to optimize your dual-state budgeting.")

    # Widget: Expense Sparkline - render only if enabled (new optional widget)
    if st.session_state.widgets.get("expense_sparkline", False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h3><i data-lucide="trending-up" class="icon"></i>📈 Expense Trends</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Expense sparkline placeholder
        import numpy as np
        sample_data = np.random.randint(1000, 5000, 12)
        st.line_chart(sample_data)
        st.caption("Monthly expense trends across all properties")

    # Widget: Reminders - render only if enabled (new optional widget)
    if st.session_state.widgets.get("reminders", False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h3><i data-lucide="bell" class="icon"></i>🔔 Reminders</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Reminders placeholder content
        st.warning("⚠️ **Upcoming**: Tax threshold check recommended in 30 days")
        st.info("📅 **Reminder**: Review quarterly budget allocations")

    st.markdown('</div>', unsafe_allow_html=True)

    snowbird_data = SnowbirdData()

    # Add more spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Widget: Detailed Status Overview - render only if enabled
    if st.session_state.widgets.get("status_overview", True):
        st.markdown('<h3><i data-lucide="bar-chart-3" class="icon"></i>📋 Detailed Status Overview</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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

    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing after metrics

        # Add spacing
        st.markdown("---")
        st.markdown("<br><br>", unsafe_allow_html=True)

    # Widget: State-by-State Breakdown - render only if enabled
    if st.session_state.widgets.get("state_breakdown", True):
        st.markdown('<h3><i data-lucide="map-pin" class="icon"></i>🗺️ State-by-State Breakdown</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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

        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing between states

        # Add spacing after state breakdown
        st.markdown("---")
        st.markdown("<br><br>", unsafe_allow_html=True)

    # Widget: Financial Summary - render only if enabled
    if st.session_state.widgets.get("financial_summary", True):
        st.markdown('<h3><i data-lucide="dollar-sign" class="icon"></i>💰 Financial Summary</h3>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Financial metrics in responsive grid
    fin_col1, fin_col2 = st.columns(2)

    with fin_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 1.5rem; border-radius: 12px;">
        """, unsafe_allow_html=True)
        st.markdown('**🏠 Monthly Home Budgets**')
        st.write("")

        # Calculate total budget across all properties
        total_all_budgets = 0
        for state, budget in st.session_state.home_budgets.items():
            total_budget = sum(budget.values())
            total_all_budgets += total_budget
            state_icon = "🌵" if "Arizona" in state else "❄️"
            st.metric(f"{state_icon} {state}", f"${total_budget:,}", delta="per month")

        st.write("---")

        # Enhanced header with pie chart icon and larger font
        st.markdown("<h3>📊 Combined Monthly Spend</h3>", unsafe_allow_html=True)

        # Clear metric display with bold formatting and no delta
        st.metric(
            label="Combined Monthly Spend", 
            value=f"${total_all_budgets:,}", 
            delta=None
        )

        # Additional context label for clarity
        st.caption("All properties combined")

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

        # Add final spacing for financial summary
        st.markdown("<br><br>", unsafe_allow_html=True)
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

# Sidebar navigation update
with st.sidebar:
    st.markdown("### 🏠 Snowbird Assistant")

    # Navigation
    selected_page = st.selectbox(
        "Navigate to:",
        ["Dashboard", "Day Tracker", "Budget Manager", "Reports", "Settings", "Email Notifications"]
    )

# Page rendering logic with email notification integration
if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "Day Tracker":
    st.title("🗓️ Day Tracker")
    st.info("Day Tracker page - Coming soon!")
elif selected_page == "Budget Manager":
    st.title("💰 Budget Manager")
    st.info("Budget Manager page - Coming soon!")
elif selected_page == "Reports":
    st.title("📊 Reports")
    st.info("Reports page - Coming soon!")
elif selected_page == "Settings":
    st.title("⚙️ Settings")
    st.info("Settings page - Coming soon!")

elif selected_page == "Email Notifications":
    st.title("📧 Email Notifications")
    # from components.email_settings import render_email_settings #Importing here to avoid circular dependency
    # render_email_settings()
    st.info("Email Notifications - Coming soon!")