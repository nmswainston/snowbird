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