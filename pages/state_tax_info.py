
import streamlit as st
import pandas as pd

# State tax information database
state_tax_info = {
    "Alabama": {"income_tax": "2.0% - 5.0%", "sales_tax": "4.0%", "property_tax": "0.41%", "retirement_friendly": "Moderate"},
    "Alaska": {"income_tax": "None", "sales_tax": "None", "property_tax": "1.19%", "retirement_friendly": "High"},
    "Arizona": {"income_tax": "2.59% - 4.5%", "sales_tax": "5.6%", "property_tax": "0.66%", "retirement_friendly": "High"},
    "Arkansas": {"income_tax": "2.0% - 5.9%", "sales_tax": "6.5%", "property_tax": "0.63%", "retirement_friendly": "Moderate"},
    "California": {"income_tax": "1.0% - 13.3%", "sales_tax": "7.25%", "property_tax": "0.75%", "retirement_friendly": "Low"},
    "Colorado": {"income_tax": "4.4%", "sales_tax": "2.9%", "property_tax": "0.51%", "retirement_friendly": "Moderate"},
    "Connecticut": {"income_tax": "3.0% - 6.99%", "sales_tax": "6.35%", "property_tax": "2.14%", "retirement_friendly": "Low"},
    "Delaware": {"income_tax": "0% - 6.6%", "sales_tax": "None", "property_tax": "0.57%", "retirement_friendly": "High"},
    "Florida": {"income_tax": "None", "sales_tax": "6.0%", "property_tax": "0.83%", "retirement_friendly": "Very High"},
    "Georgia": {"income_tax": "1.0% - 5.75%", "sales_tax": "4.0%", "property_tax": "0.93%", "retirement_friendly": "Moderate"},
    "Hawaii": {"income_tax": "1.4% - 11.0%", "sales_tax": "4.0%", "property_tax": "0.28%", "retirement_friendly": "Moderate"},
    "Idaho": {"income_tax": "1.125% - 6.925%", "sales_tax": "6.0%", "property_tax": "0.69%", "retirement_friendly": "Moderate"},
    "Illinois": {"income_tax": "4.95%", "sales_tax": "6.25%", "property_tax": "2.27%", "retirement_friendly": "Low"},
    "Indiana": {"income_tax": "3.23%", "sales_tax": "7.0%", "property_tax": "0.87%", "retirement_friendly": "Moderate"},
    "Iowa": {"income_tax": "0.33% - 8.53%", "sales_tax": "6.0%", "property_tax": "1.56%", "retirement_friendly": "Moderate"},
    "Kansas": {"income_tax": "3.1% - 5.7%", "sales_tax": "6.5%", "property_tax": "1.41%", "retirement_friendly": "Moderate"},
    "Kentucky": {"income_tax": "5.0%", "sales_tax": "6.0%", "property_tax": "0.86%", "retirement_friendly": "Moderate"},
    "Louisiana": {"income_tax": "1.85% - 4.25%", "sales_tax": "4.45%", "property_tax": "0.56%", "retirement_friendly": "Moderate"},
    "Maine": {"income_tax": "5.8% - 7.15%", "sales_tax": "5.5%", "property_tax": "1.28%", "retirement_friendly": "Low"},
    "Maryland": {"income_tax": "2.0% - 5.75%", "sales_tax": "6.0%", "property_tax": "1.09%", "retirement_friendly": "Low"},
    "Massachusetts": {"income_tax": "5.0%", "sales_tax": "6.25%", "property_tax": "1.23%", "retirement_friendly": "Low"},
    "Michigan": {"income_tax": "4.25%", "sales_tax": "6.0%", "property_tax": "1.54%", "retirement_friendly": "Moderate"},
    "Minnesota": {"income_tax": "5.35% - 9.85%", "sales_tax": "6.875%", "property_tax": "1.12%", "retirement_friendly": "Low"},
    "Mississippi": {"income_tax": "0% - 5.0%", "sales_tax": "7.0%", "property_tax": "0.81%", "retirement_friendly": "High"},
    "Missouri": {"income_tax": "1.5% - 5.4%", "sales_tax": "4.225%", "property_tax": "0.97%", "retirement_friendly": "Moderate"},
    "Montana": {"income_tax": "1.0% - 6.9%", "sales_tax": "None", "property_tax": "0.84%", "retirement_friendly": "Moderate"},
    "Nebraska": {"income_tax": "2.46% - 6.84%", "sales_tax": "5.5%", "property_tax": "1.73%", "retirement_friendly": "Moderate"},
    "Nevada": {"income_tax": "None", "sales_tax": "4.6%", "property_tax": "0.53%", "retirement_friendly": "Very High"},
    "New Hampshire": {"income_tax": "None*", "sales_tax": "None", "property_tax": "2.20%", "retirement_friendly": "High"},
    "New Jersey": {"income_tax": "1.4% - 10.75%", "sales_tax": "6.625%", "property_tax": "2.49%", "retirement_friendly": "Very Low"},
    "New Mexico": {"income_tax": "1.7% - 5.9%", "sales_tax": "5.125%", "property_tax": "0.80%", "retirement_friendly": "Moderate"},
    "New York": {"income_tax": "4.0% - 10.9%", "sales_tax": "4.0%", "property_tax": "1.69%", "retirement_friendly": "Low"},
    "North Carolina": {"income_tax": "4.99%", "sales_tax": "4.75%", "property_tax": "0.84%", "retirement_friendly": "Moderate"},
    "North Dakota": {"income_tax": "1.1% - 2.9%", "sales_tax": "5.0%", "property_tax": "1.04%", "retirement_friendly": "High"},
    "Ohio": {"income_tax": "0% - 3.99%", "sales_tax": "5.75%", "property_tax": "1.62%", "retirement_friendly": "Moderate"},
    "Oklahoma": {"income_tax": "0.25% - 5.0%", "sales_tax": "4.5%", "property_tax": "0.90%", "retirement_friendly": "Moderate"},
    "Oregon": {"income_tax": "4.75% - 9.9%", "sales_tax": "None", "property_tax": "0.93%", "retirement_friendly": "Moderate"},
    "Pennsylvania": {"income_tax": "3.07%", "sales_tax": "6.0%", "property_tax": "1.58%", "retirement_friendly": "High"},
    "Rhode Island": {"income_tax": "3.75% - 5.99%", "sales_tax": "7.0%", "property_tax": "1.63%", "retirement_friendly": "Low"},
    "South Carolina": {"income_tax": "0% - 7.0%", "sales_tax": "6.0%", "property_tax": "0.57%", "retirement_friendly": "High"},
    "South Dakota": {"income_tax": "None", "sales_tax": "4.2%", "property_tax": "1.31%", "retirement_friendly": "Very High"},
    "Tennessee": {"income_tax": "None", "sales_tax": "7.0%", "property_tax": "0.74%", "retirement_friendly": "Very High"},
    "Texas": {"income_tax": "None", "sales_tax": "6.25%", "property_tax": "1.80%", "retirement_friendly": "High"},
    "Utah": {"income_tax": "4.85%", "sales_tax": "6.1%", "property_tax": "0.58%", "retirement_friendly": "Moderate"},
    "Vermont": {"income_tax": "3.35% - 8.75%", "sales_tax": "6.0%", "property_tax": "1.90%", "retirement_friendly": "Low"},
    "Virginia": {"income_tax": "2.0% - 5.75%", "sales_tax": "5.3%", "property_tax": "0.81%", "retirement_friendly": "Moderate"},
    "Washington": {"income_tax": "None", "sales_tax": "6.5%", "property_tax": "0.94%", "retirement_friendly": "High"},
    "West Virginia": {"income_tax": "3.0% - 6.5%", "sales_tax": "6.0%", "property_tax": "0.60%", "retirement_friendly": "Moderate"},
    "Wisconsin": {"income_tax": "3.54% - 7.65%", "sales_tax": "5.0%", "property_tax": "1.85%", "retirement_friendly": "Moderate"},
    "Wyoming": {"income_tax": "None", "sales_tax": "4.0%", "property_tax": "0.62%", "retirement_friendly": "Very High"}
}

def show_page():
    st.markdown('<h2 class="section-header">🏛️ State Tax Information</h2>', unsafe_allow_html=True)
    
    # Individual state lookup
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
        st.subheader("🔍 Individual State Lookup")
        
        selected_state = st.selectbox("🏛️ Select a state for detailed tax info:", 
                                    list(state_tax_info.keys()),
                                    index=list(state_tax_info.keys()).index("Arizona") if "Arizona" in state_tax_info else 0)
        
        if selected_state in state_tax_info:
            tax_info = state_tax_info[selected_state]
            
            st.markdown(f"### 🏛️ {selected_state} Tax Overview")
            
            # Display metrics in a clean format
            col_tax1, col_tax2 = st.columns(2)
            with col_tax1:
                st.metric("💰 Income Tax Rate", tax_info["income_tax"])
                st.metric("🛒 Sales Tax Rate", tax_info["sales_tax"])
            with col_tax2:
                st.metric("🏠 Property Tax Rate", tax_info["property_tax"])
                
                # Retirement friendliness with color coding
                friendliness = tax_info["retirement_friendly"]
                if friendliness == "Very High":
                    color = "#10B981"
                elif friendliness == "High":
                    color = "#34D399"
                elif friendliness == "Moderate":
                    color = "#F59E0B"
                elif friendliness == "Low":
                    color = "#F87171"
                else:
                    color = "#EF4444"
                
                st.markdown(f'<div style="padding: 1rem; background: {color}20; border: 1px solid {color}; border-radius: 10px; text-align: center;"><strong>👴 Retirement Friendly</strong><br><span style="color: {color}; font-weight: bold;">{friendliness}</span></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("📊 Your States Comparison")
        
        # Compare user's states
        if st.session_state.states:
            comparison_data = []
            for state_name in st.session_state.states.keys():
                if state_name in state_tax_info:
                    info = state_tax_info[state_name]
                    days = st.session_state.states[state_name]
                    comparison_data.append({
                        "State": state_name,
                        "Days Logged": days,
                        "Income Tax": info["income_tax"],
                        "Sales Tax": info["sales_tax"],
                        "Property Tax": info["property_tax"],
                        "Retirement Friendly": info["retirement_friendly"]
                    })
            
            if comparison_data:
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Quick comparison insights
                st.markdown("**💡 Quick Insights:**")
                for data in comparison_data:
                    state = data["State"]
                    days = data["Days Logged"]
                    friendly = data["Retirement Friendly"]
                    st.write(f"• **{state}** ({days} days): {friendly} retirement friendliness")
        else:
            st.info("📝 Add some states to see comparison data!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # State search and filter
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("🔍 Advanced State Search & Filtering")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        income_tax_filter = st.selectbox("Filter by Income Tax:", 
                                       ["All", "No Income Tax", "Low (< 5%)", "Moderate (5-8%)", "High (> 8%)"])
    
    with col2:
        retirement_filter = st.selectbox("Filter by Retirement Friendliness:", 
                                       ["All", "Very High", "High", "Moderate", "Low", "Very Low"])
    
    with col3:
        search_state = st.text_input("🔍 Search state name:")
    
    # Apply filters
    filtered_states = {}
    for state, info in state_tax_info.items():
        # Apply search filter
        if search_state and search_state.lower() not in state.lower():
            continue
        
        # Apply income tax filter
        if income_tax_filter != "All":
            income_tax = info["income_tax"]
            if income_tax_filter == "No Income Tax" and "None" not in income_tax:
                continue
            elif income_tax_filter == "Low (< 5%)" and ("None" in income_tax or not any(char.isdigit() and float(income_tax.split('%')[0].split()[-1]) < 5.0 for char in income_tax if char.isdigit())):
                continue
        
        # Apply retirement filter
        if retirement_filter != "All" and info["retirement_friendly"] != retirement_filter:
            continue
        
        filtered_states[state] = info
    
    # Display filtered results
    if filtered_states:
        st.markdown(f"**📋 Found {len(filtered_states)} states matching your criteria:**")
        
        # Create a comprehensive table
        display_data = []
        for state, info in filtered_states.items():
            display_data.append({
                "State": state,
                "Income Tax": info["income_tax"],
                "Sales Tax": info["sales_tax"],
                "Property Tax": info["property_tax"],
                "Retirement Friendly": info["retirement_friendly"]
            })
        
        df_filtered = pd.DataFrame(display_data)
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    else:
        st.warning("No states match your current filter criteria.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tax planning insights
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("💡 Tax Planning Insights")
    
    # Best states for different criteria
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌟 Best for No Income Tax:**")
        no_income_tax_states = [state for state, info in state_tax_info.items() if "None" in info["income_tax"]]
        for state in no_income_tax_states[:5]:  # Show top 5
            retirement_level = state_tax_info[state]["retirement_friendly"]
            st.write(f"• **{state}** - {retirement_level} retirement friendliness")
    
    with col2:
        st.markdown("**👴 Best for Retirement:**")
        retirement_friendly_states = sorted(
            [(state, info) for state, info in state_tax_info.items()],
            key=lambda x: {"Very High": 5, "High": 4, "Moderate": 3, "Low": 2, "Very Low": 1}[x[1]["retirement_friendly"]],
            reverse=True
        )
        
        for state, info in retirement_friendly_states[:5]:  # Show top 5
            st.write(f"• **{state}** - {info['retirement_friendly']}")
    
    # Recommendations based on user's current states
    if st.session_state.states:
        st.markdown("**🎯 Recommendations for Your Portfolio:**")
        user_states = list(st.session_state.states.keys())
        
        # Find potential improvement states
        current_friendliness = []
        for state in user_states:
            if state in state_tax_info:
                friendliness = state_tax_info[state]["retirement_friendly"]
                current_friendliness.append(friendliness)
        
        # Suggest better alternatives
        better_states = []
        for state, info in state_tax_info.items():
            if state not in user_states and info["retirement_friendly"] in ["Very High", "High"]:
                better_states.append(state)
        
        if better_states:
            st.info(f"💡 Consider exploring these retirement-friendly alternatives: {', '.join(better_states[:3])}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download tax data
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("📥 Export Tax Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All State Data", type="primary"):
            df_all = pd.DataFrame.from_dict(state_tax_info, orient='index').reset_index()
            df_all.rename(columns={'index': 'State'}, inplace=True)
            
            csv_data = df_all.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name="state_tax_information.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🔍 Export Filtered Results"):
            if filtered_states:
                df_filtered_export = pd.DataFrame.from_dict(filtered_states, orient='index').reset_index()
                df_filtered_export.rename(columns={'index': 'State'}, inplace=True)
                
                csv_filtered = df_filtered_export.to_csv(index=False)
                st.download_button(
                    label="💾 Download Filtered CSV",
                    data=csv_filtered,
                    file_name="filtered_state_tax_info.csv",
                    mime="text/csv"
                )
            else:
                st.info("No filtered data to export")
    
    st.markdown('</div>', unsafe_allow_html=True)
