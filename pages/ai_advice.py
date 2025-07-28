
import streamlit as st
import datetime
import os

def show_page():
    st.markdown('<h2 class="section-header">🤖 Snowbird AI Assistant</h2>', unsafe_allow_html=True)
    
    # Try to load OpenAI
    try:
        from openai import OpenAI
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
    
    # Enhanced AI Chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("💬 Chat with Snowbird AI")
        
        question = st.text_area("🗣️ Ask about your travel plans, tax implications, or get smart suggestions:", 
                               height=100,
                               placeholder="Example: How many more days can I safely stay in Arizona this year?")
        
        if st.button("🚀 Get AI Advice", type="primary", use_container_width=True):
            if not openai_available:
                st.session_state.chat_response = "OpenAI API key not configured. Please add your OPENAI_API_KEY to Replit Secrets."
            elif not question.strip():
                st.session_state.chat_response = "Please enter a question first."
            else:
                try:
                    # Enhanced context for AI
                    context = f"""
                    Current Snowbird Situation (as of {datetime.date.today()}):
                    
                    RESIDENCY STATUS:
                    - Tax threshold: {st.session_state.tax_threshold} days
                    {chr(10).join([f"- {state}: {days} days ({(days/st.session_state.tax_threshold)*100:.1f}% of threshold)" for state, days in st.session_state.states.items()])}
                    
                    FINANCIAL OVERVIEW:
                    - Home budgets: {', '.join([f"{state}: ${sum(budget.values())}" for state, budget in st.session_state.home_budgets.items()])}
                    - Seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
                    
                    RECENT ACTIVITY:
                    {chr(10).join([f"- {log['date']}: {log['state']}" for log in sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:5]])}
                    
                    Please provide helpful, specific advice considering tax implications, costs, and optimal planning.
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"You are an expert financial and tax planning assistant for snowbirds (seasonal residents). You help optimize travel schedules, minimize tax burdens, and manage multi-residence expenses. Provide specific, actionable advice. Current context: {context}"},
                            {"role": "user", "content": question}
                        ]
                    )
                    st.session_state.chat_response = response.choices[0].message.content
                except Exception as e:
                    st.session_state.chat_response = f"Error: {e}"
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
        st.subheader("⚡ Quick Questions")
        
        quick_questions = [
            "How many more days can I safely stay in Arizona?",
            "What's my current tax risk assessment?", 
            "Suggest an optimal travel schedule for next month",
            "Compare costs between my residences",
            "When should I plan my next move?",
            "What are the tax implications of my current status?",
            "How can I minimize my tax burden?",
            "What's the most cost-effective residence strategy?"
        ]
        
        for i, q in enumerate(quick_questions):
            if st.button(f"💡 {q}", key=f"quick_ai_{i}", use_container_width=True):
                question = q
                # Trigger the same AI logic as above
                if openai_available:
                    try:
                        context = f"""
                        Current Snowbird Situation (as of {datetime.date.today()}):
                        
                        RESIDENCY STATUS:
                        - Tax threshold: {st.session_state.tax_threshold} days
                        {chr(10).join([f"- {state}: {days} days ({(days/st.session_state.tax_threshold)*100:.1f}% of threshold)" for state, days in st.session_state.states.items()])}
                        
                        FINANCIAL OVERVIEW:
                        - Home budgets: {', '.join([f"{state}: ${sum(budget.values())}" for state, budget in st.session_state.home_budgets.items()])}
                        - Seasonal expenses: ${sum(st.session_state.seasonal_cash_flow.values())}/month
                        
                        RECENT ACTIVITY:
                        {chr(10).join([f"- {log['date']}: {log['state']}" for log in sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:5]])}
                        """
                        
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": f"You are an expert financial and tax planning assistant for snowbirds. Provide specific, actionable advice. Context: {context}"},
                                {"role": "user", "content": question}
                            ]
                        )
                        st.session_state.chat_response = response.choices[0].message.content
                    except Exception as e:
                        st.session_state.chat_response = f"Error: {e}"
                else:
                    st.session_state.chat_response = "OpenAI API key not configured. Please add your OPENAI_API_KEY to Replit Secrets."
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display AI Response
    if st.session_state.chat_response:
        st.markdown('<div class="winter-card" style="border-left: 4px solid var(--primary-color);">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Response:")
        st.markdown(st.session_state.chat_response)
        
        # Action buttons for the response
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Response"):
                # Add to a simple chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "question": question if 'question' in locals() else "Quick question",
                    "response": st.session_state.chat_response
                })
                st.success("✅ Response saved to chat history!")
        
        with col2:
            if st.button("🔄 Ask Follow-up"):
                st.session_state.follow_up = True
        
        with col3:
            if st.button("❌ Clear Response"):
                st.session_state.chat_response = ""
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat History
    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
        st.subheader("📚 Chat History")
        
        # Show recent conversations
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
            timestamp = datetime.datetime.fromisoformat(chat["timestamp"])
            with st.expander(f"💬 {chat['question'][:50]}... - {timestamp.strftime('%m/%d %H:%M')}"):
                st.write(f"**Question:** {chat['question']}")
                st.write(f"**Response:** {chat['response']}")
        
        # Export chat history
        if st.button("📤 Export Chat History"):
            import json
            chat_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="💾 Download Chat History",
                data=chat_data,
                file_name=f"snowbird_ai_chat_{datetime.date.today().isoformat()}.json",
                mime="application/json"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Planning Tools
    st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
    st.subheader("🛠️ AI Planning Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📅 Schedule Optimizer**")
        if st.button("🎯 Optimize My Schedule", use_container_width=True):
            if openai_available:
                context = f"I need help optimizing my travel schedule. Current status: {st.session_state.states}. Tax threshold: {st.session_state.tax_threshold} days."
                # Could implement schedule optimization logic here
                st.info("💡 Schedule optimization coming soon! Use the chat for now.")
            else:
                st.error("OpenAI API required for this feature")
    
    with col2:
        st.markdown("**💰 Cost Optimizer**")
        if st.button("💡 Minimize My Costs", use_container_width=True):
            if openai_available:
                st.info("💡 Cost optimization coming soon! Use the chat for now.")
            else:
                st.error("OpenAI API required for this feature")
    
    with col3:
        st.markdown("**🚨 Risk Analyzer**")
        if st.button("⚠️ Analyze Tax Risks", use_container_width=True):
            # This can work without AI
            risk_analysis = []
            for state, days in st.session_state.states.items():
                risk_pct = (days / st.session_state.tax_threshold) * 100
                if risk_pct >= 90:
                    risk_analysis.append(f"🔴 {state}: {risk_pct:.1f}% - CRITICAL")
                elif risk_pct >= 75:
                    risk_analysis.append(f"🟠 {state}: {risk_pct:.1f}% - HIGH")
                elif risk_pct >= 50:
                    risk_analysis.append(f"🟡 {state}: {risk_pct:.1f}% - MODERATE")
                else:
                    risk_analysis.append(f"🟢 {state}: {risk_pct:.1f}% - LOW")
            
            if risk_analysis:
                st.info("**Risk Analysis:**\n" + "\n".join(risk_analysis))
            else:
                st.info("No risk data available yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Smart Insights (without AI)
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("🧠 Smart Insights")
    
    # Generate insights based on current data
    insights = []
    
    # Day-based insights
    total_days = sum(st.session_state.states.values())
    if total_days > 0:
        insights.append(f"📊 You've logged {total_days} total days across all residences this year.")
    
    # Risk insights
    for state, days in st.session_state.states.items():
        remaining = st.session_state.tax_threshold - days
        if 0 < remaining <= 30:
            insights.append(f"⚠️ You're within 30 days of tax residency in {state} ({remaining} days remaining).")
        elif remaining <= 0:
            insights.append(f"🚨 You've exceeded the tax threshold in {state} by {abs(remaining)} days.")
    
    # Budget insights
    budgets = [sum(budget.values()) for budget in st.session_state.home_budgets.values()]
    if len(budgets) > 1:
        max_budget = max(budgets)
        min_budget = min(budgets)
        diff = max_budget - min_budget
        insights.append(f"💰 Your most expensive residence costs ${diff:,} more per month than your least expensive.")
    
    # Seasonal insights
    seasonal_total = sum(st.session_state.seasonal_cash_flow.values())
    if seasonal_total > 0:
        insights.append(f"💸 Your seasonal expenses total ${seasonal_total:,} per month (${seasonal_total * 12:,} annually).")
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("💡 Start logging your days and adding budget information to get personalized insights!")
    
    st.markdown('</div>', unsafe_allow_html=True)
