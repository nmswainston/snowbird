
import streamlit as st

def show_page():
    st.markdown('<h2 class="section-header">💸 Seasonal Cash Flow Plan</h2>', unsafe_allow_html=True)
    
    # Seasonal expenses overview
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("💰 Current Seasonal Expenses")
    
    total_seasonal = 0
    if st.session_state.seasonal_cash_flow:
        # Display in a nice grid
        cols = st.columns(min(3, len(st.session_state.seasonal_cash_flow)))
        for i, (category, amount) in enumerate(st.session_state.seasonal_cash_flow.items()):
            with cols[i % 3]:
                st.metric(f"💸 {category}", f"${amount:,}", delta="per month")
            total_seasonal += amount

    st.markdown(f'<div class="metric-card"><h3>💰 Total Monthly Seasonal Expenses: ${total_seasonal:,}</h3></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Edit seasonal expenses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="winter-card">', unsafe_allow_html=True)
        st.subheader("✏️ Edit Existing Expenses")
        
        for category in st.session_state.seasonal_cash_flow:
            current_amount = st.session_state.seasonal_cash_flow[category]
            new_value = st.number_input(f"💸 {category} ($):", 
                                       min_value=0, 
                                       value=current_amount,
                                       key=f"seasonal_edit_{category}")
            if new_value != current_amount:
                st.session_state.seasonal_cash_flow[category] = new_value
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("➕ Add New Expense Category")
        
        new_seasonal_category = st.text_input("💡 New expense category:")
        new_seasonal_amount = st.number_input("💰 Amount ($):", min_value=0, key="new_seasonal_amount")
        
        if st.button("➕ Add Seasonal Category", type="primary") and new_seasonal_category and new_seasonal_amount > 0:
            if new_seasonal_category not in st.session_state.seasonal_cash_flow:
                st.session_state.seasonal_cash_flow[new_seasonal_category] = new_seasonal_amount
                st.success(f"✅ Added {new_seasonal_category}!")
                st.rerun()
            else:
                st.warning(f"⚠️ Category '{new_seasonal_category}' already exists!")
        
        # Remove categories
        st.subheader("🗑️ Remove Category")
        if st.session_state.seasonal_cash_flow:
            category_to_remove = st.selectbox("Select category to remove:", 
                                            [""] + list(st.session_state.seasonal_cash_flow.keys()))
            if st.button("🗑️ Remove Category") and category_to_remove:
                del st.session_state.seasonal_cash_flow[category_to_remove]
                st.success(f"🗑️ Removed {category_to_remove}!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Seasonal planning and analysis
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("📊 Seasonal Analysis & Planning")
    
    # Calculate different scenarios
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**❄️ Winter Season (6 months)**")
        winter_total = total_seasonal * 6
        st.metric("Total Winter Costs", f"${winter_total:,}")
        
    with col2:
        st.markdown("**🌞 Summer Season (6 months)**")
        summer_total = total_seasonal * 6
        st.metric("Total Summer Costs", f"${summer_total:,}")
        
    with col3:
        st.markdown("**📅 Annual Total**")
        annual_seasonal = total_seasonal * 12
        st.metric("Annual Seasonal Expenses", f"${annual_seasonal:,}")
    
    # Cash flow recommendations
    st.subheader("💡 Cash Flow Recommendations")
    
    if total_seasonal > 0:
        # Calculate recommended savings
        recommended_emergency = total_seasonal * 3  # 3 months emergency fund
        recommended_annual = total_seasonal * 12    # Full year fund
        
        st.info(f"💰 **Emergency Fund Recommendation**: ${recommended_emergency:,} (3 months of seasonal expenses)")
        st.info(f"📈 **Annual Planning Fund**: ${recommended_annual:,} (Full year of seasonal expenses)")
        
        # Monthly savings target
        monthly_savings_target = annual_seasonal / 12
        st.success(f"🎯 **Monthly Savings Target**: ${monthly_savings_target:,} to cover all seasonal expenses")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Expense categories breakdown
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("📈 Expense Categories Breakdown")
    
    if st.session_state.seasonal_cash_flow:
        # Create a simple visualization using progress bars
        max_expense = max(st.session_state.seasonal_cash_flow.values()) if st.session_state.seasonal_cash_flow else 0
        
        for category, amount in st.session_state.seasonal_cash_flow.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{category}**")
            with col2:
                st.write(f"${amount:,}")
            with col3:
                percentage = (amount / total_seasonal * 100) if total_seasonal > 0 else 0
                st.write(f"{percentage:.1f}%")
            
            # Progress bar showing relative size
            if max_expense > 0:
                progress = amount / max_expense
                st.progress(progress, text=f"{category}: ${amount:,}")
    else:
        st.info("📝 No seasonal expenses added yet. Start by adding your first expense category!")
    
    st.markdown('</div>', unsafe_allow_html=True)
