def get_ai_response(question: str, context: dict = None) -> str:
    """Get AI response for user question with enhanced context"""

    try:
        # Prepare context information
        context_info = prepare_context_for_ai(context or {})

        # System prompt for Hawaiian surfer personality responses
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

        IMPORTANT: Respond using a relaxed Hawaiian surfer personality and pidgin English. Use phrases like:
        - "Aloha" and "brah/bruddah" 
        - "Stoked", "rad", "gnarly", "epic"
        - "No worries", "hang loose", "stay cool"
        - "Shoots" (means "sounds good")
        - "Da kine" (the thing/stuff)
        - "Grindz" (food/money matters)
        - "Pau" (finished/done)

        Give solid financial advice but make it sound like you're having a casual conversation on the beach.
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

        # Add some extra Hawaiian flair if the response seems too formal
        if not any(word in ai_response.lower() for word in ['aloha', 'brah', 'stoked', 'rad', 'shoots']):
            ai_response = f"Aloha brah! 🤙 {ai_response}\n\nStay stoked and keep riding those financial waves! 🌊"

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
        return "Bummer brah! 🏄‍♂️ Da waves stay choppy right now and I stay having trouble catching your question. Give um another shot in one minute, or holler at support if dis keeps happening. No worries though - we gonna get you sorted! Stay cool! 🤙"