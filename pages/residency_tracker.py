
import streamlit as st

def show_page():
    st.markdown('<h2 class="section-header">📅 Tax Residency Tracker</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-style: italic; opacity: 0.8;">Tax residency threshold: {st.session_state.tax_threshold} days</p>', unsafe_allow_html=True)
    
    # Residency status cards
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("🏠 Current Residency Status")
    
    for state, days in st.session_state.states.items():
        progress = min(days / st.session_state.tax_threshold, 1.0)
        
        # Determine status and styling
        if days >= st.session_state.tax_threshold:
            status = "🔴 TAX RESIDENT"
            status_class = "status-danger"
            progress_color = "#EF4444"
        elif days >= st.session_state.tax_threshold * 0.85:
            status = "⚠️ CRITICAL"
            status_class = "status-warning"
            progress_color = "#F59E0B"
        elif days >= st.session_state.tax_threshold * 0.7:
            status = "🟡 CAUTION"
            status_class = "status-warning"
            progress_color = "#F59E0B"
        else:
            status = "✅ SAFE"
            status_class = "status-safe"
            progress_color = "#10B981"
        
        # State residency card
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"### 🏠 {state}")
        with col2:
            st.metric("Days Logged", f"{days}")
        with col3:
            st.markdown(f'<div class="{status_class}" style="text-align: center; font-size: 1.1rem; margin-top: 1rem;">{status}</div>', unsafe_allow_html=True)
        
        # Progress bar with custom styling
        st.progress(progress, text=f"{state}: {days}/{st.session_state.tax_threshold} days ({progress*100:.1f}%)")
        
        # Risk assessment
        remaining_days = st.session_state.tax_threshold - days
        if remaining_days > 0:
            st.info(f"💡 You can spend {remaining_days} more days in {state} before becoming a tax resident")
        else:
            excess_days = days - st.session_state.tax_threshold
            st.error(f"⚠️ You have exceeded the threshold by {excess_days} days in {state}")
        
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Settings and thresholds
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Tax Threshold Settings")
        
        new_threshold = st.number_input("🎯 Tax residency threshold (days):", 
                                       min_value=1, max_value=365, 
                                       value=st.session_state.tax_threshold,
                                       help="Number of days after which you're considered a tax resident")
        
        if new_threshold != st.session_state.tax_threshold:
            st.session_state.tax_threshold = new_threshold
            st.success(f"✅ Updated threshold to {new_threshold} days!")
            st.rerun()
        
        # Common thresholds reference
        st.markdown("**📋 Common Tax Thresholds:**")
        st.write("• 183 days (most states)")
        st.write("• 120 days (some states)")
        st.write("• 90 days (some states)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("📊 Risk Assessment Summary")
        
        # Overall risk level
        max_risk = 0
        highest_risk_state = ""
        
        for state, days in st.session_state.states.items():
            risk = (days / st.session_state.tax_threshold) * 100
            if risk > max_risk:
                max_risk = risk
                highest_risk_state = state
        
        if max_risk >= 100:
            risk_level = "🔴 HIGH RISK"
            risk_color = "#EF4444"
        elif max_risk >= 85:
            risk_level = "🟠 CRITICAL"
            risk_color = "#F59E0B"
        elif max_risk >= 70:
            risk_level = "🟡 CAUTION"
            risk_color = "#F59E0B"
        else:
            risk_level = "🟢 LOW RISK"
            risk_color = "#10B981"
        
        st.markdown(f'<div style="text-align: center; font-size: 1.2rem; color: {risk_color}; font-weight: bold; margin: 1rem 0;"><h3>{risk_level}</h3></div>', unsafe_allow_html=True)
        
        if highest_risk_state:
            st.write(f"**Highest risk state:** {highest_risk_state} ({max_risk:.1f}%)")
        
        # Days remaining calculation
        import datetime
        today = datetime.date.today()
        days_left_in_year = (datetime.date(today.year, 12, 31) - today).days
        
        st.write(f"**Days left in {today.year}:** {days_left_in_year}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed analysis
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("📈 Detailed Residency Analysis")
    
    # Monthly breakdown if we have log data
    if st.session_state.day_log:
        import datetime
        today = datetime.date.today()
        year_start = datetime.date(today.year, 1, 1)
        
        monthly_breakdown = {}
        for log in st.session_state.day_log:
            log_date = datetime.datetime.fromisoformat(log['date']).date()
            if log_date >= year_start:
                month_key = log_date.strftime('%Y-%m')
                state = log['state']
                if month_key not in monthly_breakdown:
                    monthly_breakdown[month_key] = {}
                if state not in monthly_breakdown[month_key]:
                    monthly_breakdown[month_key][state] = 0
                monthly_breakdown[month_key][state] += 1
        
        if monthly_breakdown:
            st.markdown("**📅 Monthly Breakdown (Current Year):**")
            for month in sorted(monthly_breakdown.keys()):
                month_name = datetime.datetime.strptime(month, '%Y-%m').strftime('%B %Y')
                st.write(f"**{month_name}:**")
                for state, count in monthly_breakdown[month].items():
                    st.write(f"  • {state}: {count} days")
    
    # Recommendations
    st.subheader("💡 Strategic Recommendations")
    
    for state, days in st.session_state.states.items():
        remaining_days = st.session_state.tax_threshold - days
        if remaining_days > 0:
            import datetime
            today = datetime.date.today()
            days_left_in_year = (datetime.date(today.year, 12, 31) - today).days
            if remaining_days < days_left_in_year:
                st.warning(f"⚠️ **{state}**: Limit stays to {remaining_days} more days this year")
            else:
                st.success(f"✅ **{state}**: You can safely spend {remaining_days} more days this year")
        else:
            excess_days = days - st.session_state.tax_threshold
            st.error(f"🚨 **{state}**: Already exceeded threshold by {excess_days} days")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Residency Report", type="primary"):
            import json
            export_data = {
                'export_date': datetime.date.today().isoformat(),
                'tax_threshold': st.session_state.tax_threshold,
                'state_totals': st.session_state.states,
                'day_log': st.session_state.day_log,
                'risk_assessment': {
                    'highest_risk_state': highest_risk_state,
                    'max_risk_percentage': max_risk,
                    'risk_level': risk_level
                }
            }
            
            st.download_button(
                label="💾 Download Residency Report",
                data=json.dumps(export_data, indent=2),
                file_name=f"residency_report_{datetime.date.today().isoformat()}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Reset Day Counters"):
            for state in st.session_state.states:
                st.session_state.states[state] = 0
            st.session_state.day_log = []
            st.success("✅ Day counters reset!")
            st.rerun()
    
    with col3:
        if st.button("⚙️ Update Threshold"):
            st.info("💡 Use the settings panel above to update your tax threshold")
    
    st.markdown('</div>', unsafe_allow_html=True)
