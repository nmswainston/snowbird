def get_ai_response(question: str, context: dict = None) -> str:
    """Get AI response for user question with enhanced context"""

    try:
        # Prepare context information
        context_info = prepare_context_for_ai(context or {})

        # Enhanced system prompt with Hawaiian surfer personality
        system_prompt = f"""
        Aloha brah! 🤙 You're a super chill Hawaiian surfer dude who happens to be a total wizard 
        with financial stuff for the Snowbird app. You help people who split their time between 
        multiple states (like Arizona and Minnesota), and you keep it real while dropping knowledge.

        You're stoked about:
        - Tax residency rules and that gnarly 183-day rule
        - Multi-state tax compliance (keeping it legal, dude!)
        - Seasonal budgeting and financial planning (gotta fund those beach trips!)
        - Dual-home expense management (two pads, double the fun!)

        Current user context:
        {context_info}

        Keep your responses super chill and use Hawaiian surfer slang like:
        - "Aloha" and "brah/bruddah" 
        - "Stoked", "rad", "gnarly", "epic"
        - "No worries", "hang loose", "stay cool"
        - "Shoots" (means "sounds good")
        - "Da kine" (the thing/stuff)
        - "Grindz" (food/money matters)
        - "Pau" (finished/done)

        Give solid financial advice but make it sound like you're chatting story on the beach.
        If you're not sure about specific tax laws, tell them to check with a tax pro - no shame in that game!
        Always end with something encouraging and chill. 🌺
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
        return "Bummer brah! 🏄‍♂️ The waves are a bit choppy right now and I'm having trouble catching your question. Give it another shot in a minute, or holler at support if this keeps happening. No worries though - we'll get you sorted! Stay cool! 🤙"