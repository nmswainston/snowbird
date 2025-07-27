
import streamlit as st
import datetime
import os

# Configure Streamlit for deployment
st.set_page_config(page_title="Snowbird AI Financial Assistant")

# Try to load OpenAI, handle if not available or no API key
try:
    from openai import OpenAI
    # Load your OpenAI API key from environment variables (Replit Secrets)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key.strip():
        try:
            client = OpenAI(api_key=api_key)
            openai_available = True
        except Exception:
            openai_available = False
            st.warning("OpenAI API key configured but invalid. AI features disabled.")
    else:
        openai_available = False
        st.info("OpenAI API key not found. AI chat features will be disabled.")
except ImportError:
    openai_available = False
    st.info("OpenAI library not available. AI chat features will be disabled.")

# Default values
default_states = {"Arizona": 0, "Minnesota": 0}
default_home_budgets = {
    "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
    "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
}
default_seasonal_cash_flow = {
    "Travel": 300,
    "Healthcare": 400,
    "Supplemental Insurance": 200
}
default_tax_threshold = 183

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

# Session state initialization
if "states" not in st.session_state:
    st.session_state.states = default_states.copy()
if "home_budgets" not in st.session_state:
    st.session_state.home_budgets = default_home_budgets.copy()
if "seasonal_cash_flow" not in st.session_state:
    st.session_state.seasonal_cash_flow = default_seasonal_cash_flow.copy()
if "tax_threshold" not in st.session_state:
    st.session_state.tax_threshold = default_tax_threshold
if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""
if "state_tax_info" not in st.session_state:
    st.session_state.state_tax_info = state_tax_info

# Streamlit UI
st.title("❄️ Snowbird AI Financial Assistant 🏖️")
st.write("Helping you fly between seasons with your finances in check.")

# Settings section
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Tax threshold setting
    st.subheader("Tax Residency Threshold")
    new_threshold = st.number_input("Days to be considered tax resident:", 
                                   min_value=1, max_value=365, 
                                   value=st.session_state.tax_threshold)
    if new_threshold != st.session_state.tax_threshold:
        st.session_state.tax_threshold = new_threshold
    
    # Budget editing
    st.subheader("Edit Home Budgets")
    for state in ["Arizona", "Minnesota"]:
        st.write(f"**{state}**")
        for category in st.session_state.home_budgets[state]:
            new_value = st.number_input(f"{state} - {category} ($):", 
                                       min_value=0, 
                                       value=st.session_state.home_budgets[state][category],
                                       key=f"budget_{state}_{category}")
            st.session_state.home_budgets[state][category] = new_value
    
    # Seasonal cash flow editing
    st.subheader("Edit Seasonal Cash Flow")
    for category in st.session_state.seasonal_cash_flow:
        new_value = st.number_input(f"{category} ($):", 
                                   min_value=0, 
                                   value=st.session_state.seasonal_cash_flow[category],
                                   key=f"seasonal_{category}")
        st.session_state.seasonal_cash_flow[category] = new_value
    
    # Add new categories
    st.subheader("Add New Categories")
    new_seasonal_category = st.text_input("New seasonal expense category:")
    new_seasonal_amount = st.number_input("Amount ($):", min_value=0, key="new_seasonal_amount")
    if st.button("Add Seasonal Category") and new_seasonal_category:
        st.session_state.seasonal_cash_flow[new_seasonal_category] = new_seasonal_amount
        st.success(f"Added {new_seasonal_category}!")
        st.rerun()
    
    # State Management
    st.subheader("Manage Your States")
    current_states = list(st.session_state.states.keys())
    
    # Remove states
    if len(current_states) > 1:
        state_to_remove = st.selectbox("Remove a state:", [""] + current_states)
        if st.button("Remove State") and state_to_remove:
            del st.session_state.states[state_to_remove]
            if state_to_remove in st.session_state.home_budgets:
                del st.session_state.home_budgets[state_to_remove]
            st.success(f"Removed {state_to_remove}!")
            st.rerun()
    
    # Add new states
    all_states = list(state_tax_info.keys())
    available_states = [s for s in all_states if s not in current_states]
    if available_states:
        new_state = st.selectbox("Add a new state:", [""] + available_states)
        if st.button("Add State") and new_state:
            st.session_state.states[new_state] = 0
            st.session_state.home_budgets[new_state] = {"Utilities": 200, "Insurance": 150, "HOA": 100}
            st.success(f"Added {new_state}!")
            st.rerun()

# Log location
st.header("🏡 Log Your Location")
state_options = list(st.session_state.states.keys())
location = st.radio("Where are you today?", state_options)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"Log a day in {location}"):
        st.session_state.states[location] += 1
        st.success(f"Logged a day in {location}!")
with col2:
    if st.button(f"Remove a day from {location}") and st.session_state.states[location] > 0:
        st.session_state.states[location] -= 1
        st.success(f"Removed a day from {location}!")
with col3:
    # Manual day entry
    manual_days = st.number_input(f"Set {location} days directly:", 
                                 min_value=0, max_value=365,
                                 value=st.session_state.states[location],
                                 key=f"manual_{location}")
    if manual_days != st.session_state.states[location]:
        st.session_state.states[location] = manual_days

# Show budgets
st.header("📊 Home Maintenance Budget")
budget_home = st.selectbox("Select a home to view budget:", list(st.session_state.states.keys()))
budget = st.session_state.home_budgets[budget_home]
st.subheader(f"{budget_home} Budget")

# Display budget with total
total_budget = 0
for category, amount in budget.items():
    st.write(f"- {category}: ${amount}/month")
    total_budget += amount
st.write(f"**Total Monthly Budget: ${total_budget}**")

# Seasonal cash flow
st.header("💸 Seasonal Cash Flow Plan")
total_seasonal = 0
for category, amount in st.session_state.seasonal_cash_flow.items():
    st.write(f"- {category}: ${amount}/month")
    total_seasonal += amount
st.write(f"**Total Monthly Seasonal Expenses: ${total_seasonal}**")

# Residency tracker
st.header("📅 Tax Residency Tracker")
st.write(f"*Tax residency threshold: {st.session_state.tax_threshold} days*")
for state, days in st.session_state.states.items():
    st.write(f"{state}: {days} days")
    if days >= st.session_state.tax_threshold:
        st.warning(f"You may now be considered a tax resident of {state}!")

# Progress bars for visual representation
st.subheader("Days Progress")
for state, days in st.session_state.states.items():
    progress = min(days / st.session_state.tax_threshold, 1.0)
    st.progress(progress, text=f"{state}: {days}/{st.session_state.tax_threshold} days")

# Tax Information
st.header("💰 State Tax Information")
tax_state = st.selectbox("Select a state to view tax info:", list(st.session_state.states.keys()), key="tax_info_selector")
if tax_state in st.session_state.state_tax_info:
    tax_info = st.session_state.state_tax_info[tax_state]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Income Tax Rate", tax_info["income_tax"])
        st.metric("Sales Tax Rate", tax_info["sales_tax"])
    with col2:
        st.metric("Property Tax Rate", tax_info["property_tax"])
        st.metric("Retirement Friendly", tax_info["retirement_friendly"])
    
    # Show comparison if multiple states
    if len(st.session_state.states) > 1:
        st.subheader("State Tax Comparison")
        comparison_data = []
        for state_name in st.session_state.states.keys():
            if state_name in st.session_state.state_tax_info:
                info = st.session_state.state_tax_info[state_name]
                comparison_data.append({
                    "State": state_name,
                    "Income Tax": info["income_tax"],
                    "Sales Tax": info["sales_tax"],
                    "Property Tax": info["property_tax"],
                    "Retirement Friendly": info["retirement_friendly"]
                })
        
        if comparison_data:
            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

# Ask the AI
st.header("🤖 Ask Snowbird AI")
question = st.text_input("Ask a financial question:")
if st.button("Get AI Advice"):
    if not openai_available:
        st.session_state.chat_response = "OpenAI API key not configured. Please add your OPENAI_API_KEY to Replit Secrets."
    elif not question.strip():
        st.session_state.chat_response = "Please enter a question first."
    else:
        try:
            # Include current data in the AI context
            context = f"""
            Current situation:
            - Days in Arizona: {st.session_state.states['Arizona']}
            - Days in Minnesota: {st.session_state.states['Minnesota']}
            - Tax threshold: {st.session_state.tax_threshold} days
            - Arizona monthly budget: ${sum(st.session_state.home_budgets['Arizona'].values())}
            - Minnesota monthly budget: ${sum(st.session_state.home_budgets['Minnesota'].values())}
            - Total seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a friendly AI financial assistant for seasonal residents (snowbirds). Here's their current situation: {context}"},
                    {"role": "user", "content": question}
                ]
            )
            st.session_state.chat_response = response.choices[0].message.content
        except Exception as e:
            st.session_state.chat_response = f"Error: {e}"

if st.session_state.chat_response:
    st.markdown("**AI Response:**")
    st.write(st.session_state.chat_response)

# Reset option
st.header("🔄 Reset Data")
if st.button("Reset All Data to Defaults", type="secondary"):
    st.session_state.states = default_states.copy()
    st.session_state.home_budgets = default_home_budgets.copy()
    st.session_state.seasonal_cash_flow = default_seasonal_cash_flow.copy()
    st.session_state.tax_threshold = default_tax_threshold
    st.session_state.chat_response = ""
    st.success("All data reset to defaults!")
    st.rerun()
