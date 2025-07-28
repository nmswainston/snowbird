
import streamlit as st
from utils.budget_converter import convert_budget_dict, format_budget_value, display_conversion_banner

def render_budget_tracker():
    """Render the budget tracking interface"""
    
    # Display currency conversion banner if active
    display_conversion_banner()
    
    # Budget management tabs
    budget_tabs = st.tabs(["🏠 Home Budgets", "📊 Seasonal Expenses", "📈 Analysis"])
    
    with budget_tabs[0]:
        render_home_budgets()
    
    with budget_tabs[1]:
        render_seasonal_expenses()
    
    with budget_tabs[2]:
        render_budget_analysis()

def render_home_budgets():
    """Render home budget management"""
    st.subheader("🏠 Monthly Home Budgets")
    
    # Add new home budget
    with st.expander("➕ Add New Home Budget"):
        new_home = st.text_input("Home/Property Name:")
        if new_home and new_home not in st.session_state.home_budgets:
            st.session_state.home_budgets[new_home] = {
                "Mortgage/Rent": 0,
                "Utilities": 0,
                "Maintenance": 0,
                "Insurance": 0,
                "Other": 0
            }
            st.success(f"Added budget for {new_home}")
            st.rerun()
    
    # Display existing budgets
    for home, budget in st.session_state.home_budgets.items():
        with st.expander(f"🏡 {home} Budget", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                updated_budget = {}
                for category, amount in budget.items():
                    updated_budget[category] = st.number_input(
                        f"{category}:",
                        value=float(amount),
                        min_value=0.0,
                        step=50.0,
                        key=f"{home}_{category}"
                    )
                
                st.session_state.home_budgets[home] = updated_budget
            
            with col2:
                # Convert and display total
                converted_budget = convert_budget_dict(updated_budget)
                total = sum(converted_budget.values())
                st.metric("Monthly Total", format_budget_value(total))
                
                if st.button(f"🗑️ Remove {home}", key=f"remove_{home}"):
                    del st.session_state.home_budgets[home]
                    st.rerun()

def render_seasonal_expenses():
    """Render seasonal expense management"""
    st.subheader("📊 Monthly Seasonal Expenses")
    
    # Default seasonal categories
    default_categories = {
        "Travel Costs": 0,
        "Healthcare": 0, 
        "Insurance": 0,
        "Emergency Fund": 0,
        "Entertainment": 0
    }
    
    # Initialize if not exists
    if not st.session_state.seasonal_cash_flow:
        st.session_state.seasonal_cash_flow = default_categories.copy()
    
    # Allow editing seasonal expenses
    for category, amount in st.session_state.seasonal_cash_flow.items():
        st.session_state.seasonal_cash_flow[category] = st.number_input(
            f"💸 {category}:",
            value=float(amount),
            min_value=0.0,
            step=25.0,
            key=f"seasonal_{category}"
        )
    
    # Add custom category
    with st.expander("➕ Add Custom Category"):
        new_category = st.text_input("Category Name:")
        new_amount = st.number_input("Monthly Amount:", min_value=0.0, step=25.0)
        
        if st.button("Add Category") and new_category:
            st.session_state.seasonal_cash_flow[new_category] = new_amount
            st.success(f"Added {new_category}")
            st.rerun()

def render_budget_analysis():
    """Render budget analysis and insights"""
    st.subheader("📈 Budget Analysis")
    
    # Calculate totals
    total_home_budget = sum(sum(convert_budget_dict(budget).values()) for budget in st.session_state.home_budgets.values())
    total_seasonal = sum(convert_budget_dict(st.session_state.seasonal_cash_flow).values())
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Home Budgets", format_budget_value(total_home_budget))
    
    with col2:
        st.metric("Total Seasonal", format_budget_value(total_seasonal))
    
    with col3:
        st.metric("Combined Monthly", format_budget_value(total_home_budget + total_seasonal))
    
    # Annual projection
    annual_total = (total_home_budget + total_seasonal) * 12
    st.metric("Projected Annual Total", format_budget_value(annual_total))
    
    # Budget breakdown chart
    if total_home_budget > 0 or total_seasonal > 0:
        import plotly.express as px
        import pandas as pd
        
        # Create breakdown data
        breakdown_data = []
        
        # Add home budgets
        for home, budget in st.session_state.home_budgets.items():
            converted = convert_budget_dict(budget)
            total = sum(converted.values())
            if total > 0:
                breakdown_data.append({"Category": f"🏠 {home}", "Amount": total, "Type": "Home"})
        
        # Add seasonal expenses
        converted_seasonal = convert_budget_dict(st.session_state.seasonal_cash_flow)
        for category, amount in converted_seasonal.items():
            if amount > 0:
                breakdown_data.append({"Category": f"📊 {category}", "Amount": amount, "Type": "Seasonal"})
        
        if breakdown_data:
            df = pd.DataFrame(breakdown_data)
            
            # Pie chart
            fig = px.pie(df, values='Amount', names='Category', 
                        title="Monthly Budget Breakdown",
                        color='Type',
                        color_discrete_map={"Home": "#3b82f6", "Seasonal": "#f59e0b"})
            
            st.plotly_chart(fig, use_container_width=True)
