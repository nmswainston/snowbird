    import streamlit as st
    import datetime
    import openai
    import os

    # Load your OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

    # State data
    states = {"Arizona": 0, "Minnesota": 0}
    home_budgets = {
        "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
        "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
    }
    seasonal_cash_flow = {
        "Travel": 300,
        "Healthcare": 400,
        "Supplemental Insurance": 200
    }
    TAX_THRESHOLD_DAYS = 183

    # Session state init
    if "states" not in st.session_state:
        st.session_state.states = states
    if "chat_response" not in st.session_state:
        st.session_state.chat_response = ""

    # Streamlit UI
    st.title("❄️ Snowbird AI Financial Assistant 🏖️")
    st.write("Helping you fly between seasons with your finances in check.")

    # Log location
    st.header("🏡 Log Your Location")
    location = st.radio("Where are you today?", ("Arizona", "Minnesota"))
    if st.button(f"Log a day in {location}"):
        st.session_state.states[location] += 1
        st.success(f"Logged a day in {location}!")

    # Show budgets
    st.header("📊 Home Maintenance Budget")
    budget_home = st.selectbox("Select a home to view budget:", ["Arizona", "Minnesota"])
    budget = home_budgets[budget_home]
    st.subheader(f"{budget_home} Budget")
    for k, v in budget.items():
        st.write(f"- {k}: ${v}/month")

    # Seasonal cash flow
    st.header("💸 Seasonal Cash Flow Plan")
    for k, v in seasonal_cash_flow.items():
        st.write(f"- {k}: ${v}/month")

    # Residency tracker
    st.header("📅 Tax Residency Tracker")
    for state, days in st.session_state.states.items():
        st.write(f"{state}: {days} days")
        if days >= TAX_THRESHOLD_DAYS:
            st.warning(f"You may now be considered a tax resident of {state}!")

    # Ask the AI
    st.header("🤖 Ask Snowbird AI")
    question = st.text_input("Ask a financial question:")
    if st.button("Get AI Advice"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a friendly AI financial assistant for seasonal residents (snowbirds)."},
                    {"role": "user", "content": question}
                ]
            )
            st.session_state.chat_response = response['choices'][0]['message']['content']
        except Exception as e:
            st.session_state.chat_response = f"Error: {e}"

    if st.session_state.chat_response:
        st.markdown("**AI Response:**")
        st.write(st.session_state.chat_response)
