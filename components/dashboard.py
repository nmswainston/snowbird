import streamlit as st
import datetime
from utils.data_models import SnowbirdData

def render_dashboard():
    """Render the enhanced premium dashboard with responsive metrics grid"""
    
    # Show loading skeleton while data loads with Hawaiian vibes
    if 'dashboard_loaded' not in st.session_state:
        from utils.hawaii_expressions import da_kine_loading
        st.markdown(f"### 🌊 {da_kine_loading()}")
        
        # Skeleton loading animation
        st.markdown("""
        <div style="animation: pulse 1.5s ease-in-out infinite alternate;">
            <div style="background: #f1f5f9; height: 120px; border-radius: 8px; margin: 1rem 0;"></div>
            <div style="background: #f1f5f9; height: 80px; border-radius: 8px; margin: 1rem 0;"></div>
            <div style="background: #f1f5f9; height: 60px; border-radius: 8px; margin: 1rem 0;"></div>
        </div>
        <style>
        @keyframes pulse {
            0% { opacity: 1; }
            100% { opacity: 0.4; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)  # Brief loading simulation
        st.session_state.dashboard_loaded = True
        st.rerun()
    
    # Main dashboard header with larger font and better spacing
    # Import Hawaiian expressions for da kine vibes
    from utils.hawaii_expressions import da_kine_time_vibe, da_kine_greeting
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1e3a8a; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">
            🏠 Snowbird Financial Dashboard
        </h1>
        <p style="color: #64748b; font-size: 1.2rem; margin-bottom: 0.5rem;">
            Your complete seasonal residence overview
        </p>
        <p style="color: #0ea5e9; font-size: 1rem; font-style: italic;">
            {da_kine_time_vibe()} Ready to track da kine! 🤙
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacing
    st.write("")
    
    # Smart notifications banner
    from components.smart_notifications import render_smart_notifications
    render_smart_notifications()
    
    st.markdown("---")
    
    # === PRIMARY METRICS SECTION ===
    # Responsive grid: 3 columns on desktop, 1 on mobile using st.columns
    st.markdown("### 📊 Key Residency Metrics")
    
    # Get current data from session state
    arizona_days = st.session_state.get('states', {}).get('Arizona', 0)
    minnesota_days = st.session_state.get('states', {}).get('Minnesota', 0)
    tax_threshold = st.session_state.get('tax_threshold', 183)
    
    # Calculate days remaining for the state closest to threshold
    max_days_state = 'Arizona' if arizona_days >= minnesota_days else 'Minnesota'
    max_days = max(arizona_days, minnesota_days)
    days_remaining = max(0, tax_threshold - max_days)
    
    # Responsive metrics grid - 3 columns on desktop
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Arizona days metric with background card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef7ff 0%, #e0f2fe 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; 
                    margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="🏜️ Days in Arizona",
            value=arizona_days,
            delta=f"{arizona_days - 0} this period" if arizona_days > 0 else "No days logged"
        )
    
    with col2:
        # Minnesota days metric with background card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef7ff 0%, #e0f2fe 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; 
                    margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="❄️ Days in Minnesota", 
            value=minnesota_days,
            delta=f"{minnesota_days - 0} this period" if minnesota_days > 0 else "No days logged"
        )
    
    with col3:
        # Tax threshold warning metric
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef7ff 0%, #e0f2fe 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; 
                    margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
        
        # Color code the warning based on days remaining
        if days_remaining <= 30:
            warning_color = "🚨"
            status = "Critical"
        elif days_remaining <= 60:
            warning_color = "⚠️"
            status = "Caution"
        else:
            warning_color = "✅"
            status = "Safe"
            
        st.metric(
            label=f"{warning_color} Days Until Tax Risk",
            value=days_remaining,
            delta=f"{status} - {max_days_state}" if max_days > 0 else "No risk yet"
        )
    
    # Add section separator
    st.markdown("---")
    
    # === PROGRESS BAR SECTION ===
    st.markdown("### 📈 Tax Residency Progress")
    
    # Calculate progress toward 183-day threshold for primary state
    progress_percent = min(max_days / tax_threshold, 1.0) if tax_threshold > 0 else 0
    
    # Display current state and progress
    st.markdown(f"""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <h4 style="margin: 0; color: #374151;">
            Primary State: <strong>{max_days_state}</strong> 
            ({max_days}/{tax_threshold} days = {progress_percent*100:.1f}%)
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar with color coding
    if progress_percent >= 0.9:
        progress_color = "#dc2626"  # Red for danger
    elif progress_percent >= 0.75:
        progress_color = "#f59e0b"  # Orange for caution  
    else:
        progress_color = "#059669"  # Green for safe
        
    # Custom styled progress bar
    st.markdown(f"""
    <div style="background: #e5e7eb; border-radius: 10px; height: 20px; margin: 1rem 0;">
        <div style="background: {progress_color}; height: 100%; width: {progress_percent*100}%; 
                    border-radius: 10px; transition: width 0.3s ease;">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show standard streamlit progress bar as backup
    st.progress(progress_percent, text=f"Progress toward {tax_threshold}-day tax threshold")
    
    # Add spacing
    st.write("")

    # === SECONDARY METRICS SECTION ===
    st.markdown("### 📋 Additional Insights")
    
    # Calculate additional metrics
    total_days = arizona_days + minnesota_days
    days_left_in_year = max(0, 365 - total_days)
    
    # Secondary metrics in responsive grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📅 Total Days Logged", 
            value=total_days,
            delta=f"Out of 365 days" if total_days > 0 else "Start logging!"
        )
    
    with col2:
        st.metric(
            label="⏰ Days Left in Year", 
            value=days_left_in_year,
            delta=f"{(days_left_in_year/365)*100:.1f}% remaining" if days_left_in_year > 0 else "Year complete"
        )
    
    with col3:
        # Risk level calculation
        closest_to_threshold = max_days
        if closest_to_threshold >= tax_threshold * 0.9:
            risk_level = "🚨 High"
            risk_color = "#dc2626"
        elif closest_to_threshold >= tax_threshold * 0.75:
            risk_level = "⚠️ Medium" 
            risk_color = "#f59e0b"
        else:
            risk_level = "✅ Low"
            risk_color = "#059669"
            
        st.metric(
            label="🛡️ Tax Risk Level", 
            value=risk_level.split(" ", 1)[1],  # Remove emoji from value
            delta=f"{closest_to_threshold}/{tax_threshold} days"
        )
    
    # Add section separator
    st.markdown("---")
    
    # === TRENDS ANALYSIS SECTION ===
    with st.expander("📈 View Detailed Trends & Insights", expanded=False):
        from components.trends_analyzer import render_trends_analysis
        render_trends_analysis()
    
    st.markdown("---")
    
    # === INSIGHTS SECTION ===
    st.markdown("### ✨ Smart Insights")
    
    # Create insight cards in responsive grid
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        # Tax optimization score
        optimization_score = max(0, min(100, 100 - (max_days / tax_threshold * 100)))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #bbf7d0; 
                    text-align: center; margin-bottom: 1rem;">
            <h4 style="color: #166534; margin: 0 0 0.5rem 0;">📈 Tax Optimization</h4>
            <div style="font-size: 2rem; font-weight: 700; color: #166534;">
                {optimization_score:.0f}%
            </div>
            <p style="color: #166534; margin: 0; font-size: 0.9rem;">Excellent compliance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col2:
        # Days remaining calculation
        safe_days_remaining = max(0, tax_threshold - max_days - 30)  # 30-day buffer
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #f0f9ff 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #93c5fd; 
                    text-align: center; margin-bottom: 1rem;">
            <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">⏳ Safe Buffer Days</h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1e40af;">
                {safe_days_remaining}
            </div>
            <p style="color: #1e40af; margin: 0; font-size: 0.9rem;">Days with 30-day buffer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col3:
        # Next recommendation
        if days_remaining <= 30:
            recommendation = "Plan return trip soon"
            rec_color = "#dc2626"
            rec_bg = "#fee2e2"
            rec_border = "#fca5a5"
        elif days_remaining <= 60:
            recommendation = "Monitor closely"
            rec_color = "#f59e0b"
            rec_bg = "#fef3c7"
            rec_border = "#fcd34d"
        else:
            recommendation = "Continue current plan"
            rec_color = "#059669"
            rec_bg = "#d1fae5"
            rec_border = "#6ee7b7"
            
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {rec_bg} 0%, {rec_bg} 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid {rec_border}; 
                    text-align: center; margin-bottom: 1rem;">
            <h4 style="color: {rec_color}; margin: 0 0 0.5rem 0;">💡 Recommendation</h4>
            <div style="font-size: 1.2rem; font-weight: 600; color: {rec_color};">
                {recommendation}
            </div>
            <p style="color: {rec_color}; margin: 0; font-size: 0.9rem;">Based on current data</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing between sections
    st.write("")

    # === STATE RESIDENCY STATUS SECTION ===
    st.markdown("### 🗺️ Detailed State Residency Status")
    
    snowbird_data = SnowbirdData()
    
    # Loop through each state with enhanced mobile-responsive cards
    for state, days in st.session_state.states.items():
        status_text, status_class = snowbird_data.get_tax_status(days, state=state)
        # Get state-specific threshold
        state_threshold = snowbird_data.state_tax_thresholds.get(state, snowbird_data.tax_threshold)
        progress = min(days / state_threshold, 1.0) if state_threshold > 0 else 0
        days_remaining = max(0, state_threshold - days)
        
        # State icon mapping
        state_icon = "🌵" if "Arizona" in state else "❄️" if "Minnesota" in state else "🏠"
        
        # Create full-width card for each state
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fef7ff 0%, #e0f2fe 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; 
                    margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4 style="margin: 0 0 1rem 0; color: #374151; font-size: 1.3rem;">
                {state_icon} {state} Residency Tracker
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Use columns for responsive layout - stack on mobile
        state_col1, state_col2 = st.columns([2, 1])
        
        with state_col1:
            # Get state-specific threshold for display
            state_threshold = snowbird_data.state_tax_thresholds.get(state, snowbird_data.tax_threshold)
            
            # Progress bar with percentage
            st.progress(progress, text=f"{days}/{state_threshold} days ({progress*100:.1f}%)")
            
            # Status message with appropriate styling
            if status_text == "SAFE":
                st.success(f"✅ **{status_text}** - {days_remaining} days remaining before tax threshold")
            elif status_text in ["CAUTION", "CRITICAL"]:
                st.warning(f"⚠️ **{status_text}** - Only {days_remaining} days remaining!")
            else:
                st.error(f"🚨 **{status_text}** - Tax residency threshold reached")
        
        with state_col2:
            # Metric display for current days
            delta_text = f"+{days_remaining} safe" if days_remaining > 0 else "⚠️ Over limit"
            st.metric(
                label="Current Days", 
                value=days, 
                delta=delta_text
            )
    
    # Add section separator  
    st.markdown("---")

    # === FINANCIAL OVERVIEW SECTION ===
    st.markdown("### 💰 Financial Overview")
    
    # Import currency conversion utilities
    from utils.budget_converter import (
        convert_budget_value, convert_budget_dict, format_budget_value, 
        display_conversion_banner, get_conversion_status
    )
    
    # Display currency conversion status banner if adjustments are active
    display_conversion_banner()
    
    # Use responsive columns that stack on mobile
    fin_col1, fin_col2 = st.columns([1, 1])
    
    with fin_col1:
        # Home budgets card with currency conversion
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #bbf7d0; 
                    margin-bottom: 1rem;">
            <h4 style="color: #166534; margin: 0 0 1rem 0; font-size: 1.2rem;">
                🏠 Monthly Home Budgets
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        conversion_status = get_conversion_status()
        
        for state, budget in st.session_state.home_budgets.items():
            # Convert budget values based on current settings
            converted_budget = convert_budget_dict(budget)
            total_budget = sum(converted_budget.values())
            original_total = sum(budget.values())
            
            state_icon = "🌵" if "Arizona" in state else "❄️"
            
            # Calculate delta for currency/inflation impact
            delta_text = "per month"
            if conversion_status['has_adjustments'] and original_total > 0:
                change_percent = ((total_budget - original_total) / original_total) * 100
                if abs(change_percent) > 0.1:
                    delta_text = f"{change_percent:+.1f}% vs USD"
            
            # Use metric component with converted values
            st.metric(
                label=f"{state_icon} {state}",
                value=format_budget_value(total_budget),
                delta=delta_text
            )
            
            # Show individual category breakdown with conversion
            with st.expander(f"📋 {state} Budget Details"):
                for category, original_amount in budget.items():
                    converted_amount = converted_budget[category]
                    
                    col_cat, col_amount = st.columns([2, 1])
                    with col_cat:
                        st.write(f"• {category}")
                    with col_amount:
                        st.write(f"**{format_budget_value(converted_amount)}**")
                        
                        # Show original amount if converted
                        if conversion_status['has_adjustments']:
                            st.caption(f"(Original: ${original_amount:,} USD)")
    
    with fin_col2:
        # Seasonal expenses card with currency conversion
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #fdba74; 
                    margin-bottom: 1rem;">
            <h4 style="color: #c2410c; margin: 0 0 1rem 0; font-size: 1.2rem;">
                📊 Seasonal Expenses
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert seasonal cash flow values
        converted_seasonal = convert_budget_dict(st.session_state.seasonal_cash_flow)
        total_seasonal = sum(converted_seasonal.values())
        original_total_seasonal = sum(st.session_state.seasonal_cash_flow.values())
        
        # Calculate delta for total seasonal expenses
        delta_text = "across all categories"
        if conversion_status['has_adjustments'] and original_total_seasonal > 0:
            change_percent = ((total_seasonal - original_total_seasonal) / original_total_seasonal) * 100
            if abs(change_percent) > 0.1:
                delta_text = f"{change_percent:+.1f}% vs USD"
        
        # Total seasonal budget metric with converted values
        st.metric(
            label="🗓️ Total Monthly Seasonal",
            value=format_budget_value(total_seasonal),
            delta=delta_text
        )
        
        # Individual category breakdown with conversion
        st.markdown("**Category Breakdown:**")
        for category, original_amount in st.session_state.seasonal_cash_flow.items():
            converted_amount = converted_seasonal[category]
            
            # Add emoji based on category
            if "Travel" in category:
                emoji = "✈️"
            elif "Healthcare" in category:
                emoji = "🏥"
            elif "Insurance" in category:
                emoji = "🛡️"
            elif "Emergency" in category:
                emoji = "🚨"
            else:
                emoji = "💸"
            
            # Display converted amount
            st.write(f"  {emoji} {category}: **{format_budget_value(converted_amount)}**")
            
            # Show original amount if converted
            if conversion_status['has_adjustments']:
                st.caption(f"    💵 Original: ${original_amount:,} USD")
        
        # Add annual totals calculation
        st.markdown("---")
        st.markdown("**📅 Annual Projections:**")
        
        annual_seasonal = total_seasonal * 12
        st.write(f"• Total Annual Seasonal: **{format_budget_value(annual_seasonal)}**")
        
        # Calculate total annual home budgets
        total_annual_homes = 0
        for state, budget in st.session_state.home_budgets.items():
            converted_budget = convert_budget_dict(budget)
            total_annual_homes += sum(converted_budget.values()) * 12
        
        st.write(f"• Total Annual Home Budgets: **{format_budget_value(total_annual_homes)}**")
        
        # Grand total
        grand_total_annual = annual_seasonal + total_annual_homes
        st.write(f"• **Grand Total Annual: {format_budget_value(grand_total_annual)}**")
        
        if conversion_status['has_adjustments']:
            original_grand_total = (original_total_seasonal + sum(sum(budget.values()) for budget in st.session_state.home_budgets.values())) * 12
            st.caption(f"💵 Original Total: ${original_grand_total:,} USD")
    
    # Add final spacing
    st.write("")
    
    # === FOOTER MESSAGE ===
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.9rem; 
                background: #f8fafc; border-radius: 8px; margin-top: 2rem;">
        📱 <strong>Mobile-Friendly:</strong> This dashboard adapts to your screen size for easy viewing on any device.
    </div>
    """, unsafe_allow_html=True)
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