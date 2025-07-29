"""
AI Assistant Component for Snowbird Financial Assistant
Provides AI-powered financial advice and guidance
"""

import streamlit as st
import datetime
import openai
import random
from typing import Dict, List
from utils.logger import logger

def get_ai_response(question: str, context: dict = None) -> str:
    """Get AI response for user question with enhanced context"""

    try:
        # Prepare context information
        context_info = prepare_context_for_ai(context or {})

        # System prompt for helpful financial assistant responses  
        system_prompt = f"""
        You are a knowledgeable financial assistant specializing in multi-state tax residency for the Snowbird application. 
        You help people who split their time between multiple states (like Arizona and Minnesota) with tax compliance and financial planning.

        Your expertise includes:
        - Tax residency rules and the 183-day rule
        - Multi-state tax compliance
        - Seasonal budgeting and financial planning
        - Dual-home expense management

        Current user context:
        {context_info}

        IMPORTANT: Respond in a friendly, helpful, and professional manner. Focus on providing clear guidance like:
        - "Great question!" (for engagement)
        - "Here's what I recommend" (for guidance)
        - "Let me help you with that" (for assistance)
        - "You're on the right track" (for encouragement)
        - "Consider this approach" (for suggestions)
        - "That's completed" (for finished tasks)
        - "I understand" (for acknowledgment)

        Always maintain a helpful and professional tone while providing accurate financial advice.
        If you're uncertain about specific tax laws, recommend consulting with a tax professional.
        Always end with something encouraging and positive.
        """

        # Make API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=600,  # Increased for more colorful responses
            temperature=0.8   # Bit more creative for that surfer vibe
        )

        ai_response = response.choices[0].message.content.strip()

        # Ensure response is helpful and clear
        if len(ai_response) < 20:  # If response is too short, add helpful context
            helpful_starters = [
                "Let me help you with that. ",
                "Here's what I recommend: ",
                "Great question! ",
                "I'd be happy to assist: "
            ]
            ai_response = random.choice(helpful_starters) + ai_response

        # Log the interaction for analytics
        if hasattr(st.session_state, 'ai_interactions'):
            st.session_state.ai_interactions.append({
                'timestamp': datetime.now(),
                'question': question,
                'response': ai_response
            })

        return ai_response

    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "I apologize, but I'm currently experiencing some technical difficulties. Please try again in a few minutes. If the problem persists, please contact support. We'll get it sorted out!"

def prepare_context_for_ai(context: dict) -> str:
    """Prepare context information for AI assistant"""
    context_parts = []
    
    if 'states' in context:
        context_parts.append(f"Current state days: {context['states']}")
    
    if 'budget_data' in context:
        context_parts.append(f"Budget information available")
    
    if 'tax_threshold' in context:
        context_parts.append(f"Tax threshold: {context['tax_threshold']} days")
    
    return "\n".join(context_parts) if context_parts else "No specific context provided"

def render_ai_assistant(openai_client=None):
    """Render the AI assistant interface"""
    st.markdown("### 🤖 Ask Your Financial Assistant")
    
    # Initialize session state for chat history
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # Chat input
    user_question = st.text_area(
        "Ask a question about tax residency, budgeting, or financial planning:",
        placeholder="e.g., How many days can I spend in Arizona before becoming a tax resident?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        ask_button = st.button("🤖 Ask AI", type="primary")
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.ai_chat_history = []
            st.rerun()
    
    # Process AI request
    if ask_button and user_question.strip():
        with st.spinner("Getting AI response..."):
            try:
                # Prepare context from session state
                context = {
                    'states': getattr(st.session_state, 'states', {}),
                    'tax_threshold': 183,
                    'budget_data': getattr(st.session_state, 'budget_data', {})
                }
                
                # Get AI response
                ai_response = get_ai_response(user_question, context)
                
                # Add to chat history
                st.session_state.ai_chat_history.append({
                    'question': user_question,
                    'response': ai_response,
                    'timestamp': datetime.datetime.now()
                })
                
                st.rerun()
                
            except Exception as e:
                logger.error(f"Error in AI assistant: {e}")
                st.error("Sorry, I'm having trouble right now. Please try again later.")
    
    # Display chat history
    if st.session_state.ai_chat_history:
        st.markdown("---")
        st.markdown("### 💬 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.ai_chat_history[-5:])):  # Show last 5 conversations
            with st.expander(f"Q: {chat['question'][:60]}..." if len(chat['question']) > 60 else f"Q: {chat['question']}", expanded=(i == 0)):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['response']}")
                st.caption(f"Asked on {chat['timestamp'].strftime('%Y-%m-%d at %H:%M')}")
                
                # Add rating buttons for each response
                from utils.ai_rating_system import render_ai_rating_buttons
                render_ai_rating_buttons(
                    question=chat['question'],
                    response=chat['response'],
                    unique_key=f"chat_{i}"
                )
    
    # AI Tips section
    with st.expander("💡 AI Assistant Tips", expanded=False):
        st.markdown("""
        **Great questions to ask:**
        - "How many days can I spend in each state?"
        - "What expenses should I track for dual residency?"
        - "When should I establish domicile in a new state?"
        - "What tax documents do I need to keep?"
        - "How do I optimize my seasonal budget?"
        
        **The AI can help with:**
        - Tax residency rules and the 183-day rule
        - Multi-state compliance strategies
        - Seasonal budgeting advice
        - Property management tips
        """)
    
    # AI Response Analytics (if available)
    if hasattr(st.session_state, 'ai_interactions') and st.session_state.ai_interactions:
        if st.checkbox("Show AI Usage Analytics"):
            st.markdown("---")
            st.markdown("### 📊 Your AI Usage")
            
            total_questions = len(st.session_state.ai_interactions)
            st.metric("Total Questions Asked", total_questions)
            
            if total_questions > 0:
                avg_length = sum(len(q['question']) for q in st.session_state.ai_interactions) / total_questions
                st.metric("Average Question Length", f"{avg_length:.0f} characters")