
import streamlit as st

def show_page():
    st.markdown('<h2 class="section-header">💰 Home Maintenance Budget</h2>', unsafe_allow_html=True)
    
    # Budget overview
    col1, col2 = st.columns(2)
    
    with col1:
        budget_home = st.selectbox("🏠 Select a home to view budget:", list(st.session_state.states.keys()))
        budget = st.session_state.home_budgets[budget_home]

        st.markdown(f'<div class="winter-card ice-card"><h3>🏠 {budget_home} Budget Overview</h3>', unsafe_allow_html=True)

        # Display budget with metrics
        total_budget = 0
        for category, amount in budget.items():
            col_metric1, col_metric2 = st.columns([2, 1])
            with col_metric1:
                st.metric(f"💸 {category}", f"${amount:,}", delta="per month")
            with col_metric2:
                new_amount = st.number_input(f"Edit {category}:", 
                                           min_value=0, 
                                           value=amount,
                                           key=f"edit_{budget_home}_{category}")
                if new_amount != amount:
                    st.session_state.home_budgets[budget_home][category] = new_amount
                    st.rerun()
            total_budget += amount

        st.markdown(f'<div class="metric-card"><h3>💰 Total Monthly Budget: ${total_budget:,}</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Budget comparison
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("📊 Budget Comparison")
        
        budget_totals = {}
        for state, budget in st.session_state.home_budgets.items():
            budget_totals[state] = sum(budget.values())
        
        for state, total in budget_totals.items():
            st.metric(f"🏠 {state} Total", f"${total:,}")
        
        # Show difference
        if len(budget_totals) >= 2:
            states = list(budget_totals.keys())
            diff = abs(budget_totals[states[0]] - budget_totals[states[1]])
            higher_state = states[0] if budget_totals[states[0]] > budget_totals[states[1]] else states[1]
            st.info(f"💡 {higher_state} costs ${diff:,} more per month")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Budget management
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("⚙️ Budget Management")
    
    # Add new category
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_home = st.selectbox("Select home for new category:", list(st.session_state.states.keys()), key="new_cat_home")
    with col2:
        new_category = st.text_input("New budget category:")
    with col3:
        new_amount = st.number_input("Amount ($):", min_value=0, key="new_budget_amount")
    
    if st.button("➕ Add Budget Category") and new_category and new_amount > 0:
        if new_category not in st.session_state.home_budgets[selected_home]:
            st.session_state.home_budgets[selected_home][new_category] = new_amount
            st.success(f"✅ Added {new_category} to {selected_home} budget!")
            st.rerun()
        else:
            st.warning(f"⚠️ Category '{new_category}' already exists in {selected_home}!")
    
    # Remove category
    remove_home = st.selectbox("Select home to remove category from:", list(st.session_state.states.keys()), key="remove_cat_home")
    if remove_home in st.session_state.home_budgets:
        categories = list(st.session_state.home_budgets[remove_home].keys())
        if categories:
            category_to_remove = st.selectbox("Select category to remove:", [""] + categories)
            if st.button("🗑️ Remove Category") and category_to_remove:
                del st.session_state.home_budgets[remove_home][category_to_remove]
                st.success(f"🗑️ Removed {category_to_remove} from {remove_home}!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Annual projections
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("📈 Annual Budget Projections")
    
    for state, budget in st.session_state.home_budgets.items():
        monthly_total = sum(budget.values())
        annual_total = monthly_total * 12
        
        # Calculate based on current days logged
        days_in_state = st.session_state.states[state]
        if days_in_state > 0:
            daily_cost = monthly_total / 30  # Rough estimate
            current_year_projection = daily_cost * days_in_state
        else:
            current_year_projection = 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"🏠 {state} Monthly", f"${monthly_total:,}")
        with col2:
            st.metric(f"📅 Annual Budget", f"${annual_total:,}")
        with col3:
            st.metric(f"📊 Current Year Cost", f"${current_year_projection:,.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
