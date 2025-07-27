
import streamlit as st
import datetime
import os

# Try to load OpenAI, handle if not available or no API key
try:
    from openai import OpenAI
    # Load your OpenAI API key from environment variables (Replit Secrets)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        client = OpenAI(api_key=api_key)
        openai_available = True
    else:
        openai_available = False
except ImportError:
    openai_available = False

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

# Log location
st.header("🏡 Log Your Location")
location = st.radio("Where are you today?", ("Arizona", "Minnesota"))
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
budget_home = st.selectbox("Select a home to view budget:", ["Arizona", "Minnesota"])
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
