
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def render_reports():
    """Render the reports interface"""
    
    # Reports tabs
    report_tabs = st.tabs(["📊 Overview", "📈 Trends", "📋 Tax Summary", "📥 Export"])
    
    with report_tabs[0]:
        render_overview_report()
    
    with report_tabs[1]:
        render_trends_report()
    
    with report_tabs[2]:
        render_tax_summary()
    
    with report_tabs[3]:
        render_export_options()

def render_overview_report():
    """Render overview report"""
    st.subheader("📊 Residency Overview Report")
    
    # Get current data
    arizona_days = st.session_state.get('states', {}).get('Arizona', 0)
    minnesota_days = st.session_state.get('states', {}).get('Minnesota', 0)
    tax_threshold = st.session_state.get('tax_threshold', 183)
    
    # Create summary
    total_days = arizona_days + minnesota_days
    days_remaining = 365 - total_days
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Arizona Days", arizona_days)
    
    with col2:
        st.metric("Minnesota Days", minnesota_days)
    
    with col3:
        st.metric("Total Days Logged", total_days)
    
    with col4:
        st.metric("Days Remaining", days_remaining)
    
    # Tax status summary
    st.subheader("Tax Residency Status")
    
    primary_state = 'Arizona' if arizona_days >= minnesota_days else 'Minnesota'
    primary_days = max(arizona_days, minnesota_days)
    days_to_threshold = max(0, tax_threshold - primary_days)
    
    if primary_days >= tax_threshold:
        st.error(f"🚨 Tax resident of {primary_state} ({primary_days} days)")
    elif days_to_threshold <= 30:
        st.warning(f"⚠️ Close to {primary_state} tax residency ({days_to_threshold} days remaining)")
    else:
        st.success(f"✅ Safe from tax residency ({days_to_threshold} days remaining)")
    
    # Progress visualization
    if total_days > 0:
        st.subheader("State Distribution")
        
        # Create simple progress bars
        st.write("**Arizona**")
        st.progress(arizona_days / tax_threshold if tax_threshold > 0 else 0, 
                   text=f"{arizona_days}/{tax_threshold} days")
        
        st.write("**Minnesota**")
        st.progress(minnesota_days / tax_threshold if tax_threshold > 0 else 0,
                   text=f"{minnesota_days}/{tax_threshold} days")

def render_trends_report():
    """Render trends analysis"""
    st.subheader("📈 Trends Analysis")
    
    # This would typically show historical data
    # For now, show current period analysis
    
    arizona_days = st.session_state.get('states', {}).get('Arizona', 0)
    minnesota_days = st.session_state.get('states', {}).get('Minnesota', 0)
    
    if arizona_days > 0 or minnesota_days > 0:
        # Simple trend analysis
        st.write("**Current Period Analysis:**")
        
        total_days = arizona_days + minnesota_days
        if total_days > 0:
            az_percentage = (arizona_days / total_days) * 100
            mn_percentage = (minnesota_days / total_days) * 100
            
            st.write(f"- Arizona: {az_percentage:.1f}% of logged days")
            st.write(f"- Minnesota: {mn_percentage:.1f}% of logged days")
            
            # Recommendations
            st.subheader("📋 Recommendations")
            
            if az_percentage > 60:
                st.info("💡 Consider spending more time in Minnesota to balance residency")
            elif mn_percentage > 60:
                st.info("💡 Consider spending more time in Arizona to balance residency")
            else:
                st.success("✅ Good balance between states")
    else:
        st.info("Start logging days to see trend analysis")

def render_tax_summary():
    """Render tax summary report"""
    st.subheader("📋 Tax Summary Report")
    
    # Get data
    arizona_days = st.session_state.get('states', {}).get('Arizona', 0)
    minnesota_days = st.session_state.get('states', {}).get('Minnesota', 0)
    tax_threshold = st.session_state.get('tax_threshold', 183)
    
    # Tax implications
    st.write("**Tax Residency Analysis:**")
    
    # Arizona analysis
    st.write("**Arizona:**")
    if arizona_days >= tax_threshold:
        st.error(f"🚨 Tax resident ({arizona_days} days ≥ {tax_threshold} threshold)")
    else:
        remaining = tax_threshold - arizona_days
        st.success(f"✅ Not tax resident ({remaining} days below threshold)")
    
    # Minnesota analysis
    st.write("**Minnesota:**")
    if minnesota_days >= tax_threshold:
        st.error(f"🚨 Tax resident ({minnesota_days} days ≥ {tax_threshold} threshold)")
    else:
        remaining = tax_threshold - minnesota_days
        st.success(f"✅ Not tax resident ({remaining} days below threshold)")
    
    # Planning recommendations
    st.subheader("📅 Planning Recommendations")
    
    total_logged = arizona_days + minnesota_days
    remaining_year = 365 - total_logged
    
    if remaining_year > 0:
        st.write(f"**Remaining days in year:** {remaining_year}")
        
        # Safe allocation
        safe_az = min(remaining_year, tax_threshold - arizona_days - 1)
        safe_mn = min(remaining_year, tax_threshold - minnesota_days - 1)
        
        if safe_az > 0:
            st.write(f"- Can safely spend up to {safe_az} more days in Arizona")
        if safe_mn > 0:
            st.write(f"- Can safely spend up to {safe_mn} more days in Minnesota")

def render_export_options():
    """Render export options"""
    st.subheader("📥 Export Options")
    
    # Export data
    export_data = {
        "Report Date": datetime.now().strftime("%Y-%m-%d"),
        "Arizona Days": st.session_state.get('states', {}).get('Arizona', 0),
        "Minnesota Days": st.session_state.get('states', {}).get('Minnesota', 0),
        "Tax Threshold": st.session_state.get('tax_threshold', 183),
        "Home Budgets": dict(st.session_state.get('home_budgets', {})),
        "Seasonal Expenses": dict(st.session_state.get('seasonal_cash_flow', {}))
    }
    
    # JSON export
    import json
    json_data = json.dumps(export_data, indent=2, default=str)
    
    st.download_button(
        label="📄 Download JSON Report",
        data=json_data,
        file_name=f"snowbird_report_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    # CSV export for residency data
    if st.session_state.get('states'):
        csv_data = []
        for state, days in st.session_state.get('states', {}).items():
            csv_data.append({"State": state, "Days": days})
        
        df = pd.DataFrame(csv_data)
        csv_string = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download CSV Report",
            data=csv_string,
            file_name=f"residency_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Summary text export
    summary_text = f"""
SNOWBIRD RESIDENCY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

RESIDENCY SUMMARY:
- Arizona Days: {export_data['Arizona Days']}
- Minnesota Days: {export_data['Minnesota Days']}
- Tax Threshold: {export_data['Tax Threshold']}

BUDGET SUMMARY:
- Number of Properties: {len(export_data['Home Budgets'])}
- Seasonal Categories: {len(export_data['Seasonal Expenses'])}

Report generated by Snowbird Financial Assistant
"""
    
    st.download_button(
        label="📝 Download Text Summary",
        data=summary_text,
        file_name=f"snowbird_summary_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
