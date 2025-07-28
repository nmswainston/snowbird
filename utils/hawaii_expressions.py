"""
Standard expressions for the Snowbird app
Providing professional and friendly messaging throughout the application
"""

import random
from typing import List, Dict

class StandardExpressions:
    """Standard expressions for the Snowbird app"""

    # Friendly greetings and positive vibes
    GREETINGS = [
        "Hello there!",
        "Hi, how's it going! 😊", 
        "What's happening? 🙂",
        "Hey, how are you? 👍",
        "Great to see you! 🌟",
        "Welcome back!"
    ]

    # Success messages with positive flavor
    SUCCESS_MESSAGES = [
        "Excellent! That's perfect! ✨",
        "Great! All done! 🎉",
        "Outstanding work! 👍",
        "All good to go! 🚀",
        "No worries, all set! 😎",
        "That's how it's done! 👏"
    ]

    # Error messages with helpful spirit
    ERROR_MESSAGES = [
        "Oops, something went wrong... 😅",
        "Looks like there's an issue! 🔧",
        "Let's try that again! 💪",
        "Hmm, that didn't work! 🤔",
        "Something went wrong! 🌀",
        "Let's get this fixed! 🛠️"
    ]

    # Loading and waiting messages
    LOADING_MESSAGES = [
        "Please wait, loading... ⏳",
        "Just a moment... 🔄",
        "Almost done, small wait... ⏰",
        "Getting things ready... 📦",
        "Making things happen... ✨",
        "Hang tight, almost done... 😊"
    ]

    # Tax and financial advice with professional wisdom
    TAX_ADVICE = [
        "Stay organized with your taxes! 📊",
        "Keep track of everything for the IRS! 💸",
        "Smart money moves, professional style! 🏛️",
        "Stay organized like a pro! 📝",
        "Don't mess around with government requirements! ⚖️",
        "Financial planning made simple! 💼"
    ]

    # Budget wisdom
    BUDGET_WISDOM = [
        "More money, more responsibility... track it well! 💰",
        "Spend wisely like the experts! 👔",
        "Save for the future! 💳",
        "Budget tight like a good plan! 📋",
        "Don't spend everything in one place! 🎯",
        "Smart spending the professional way! 💼"
    ]

    # State-specific expressions
    STATE_EXPRESSIONS = {
        "Arizona": [
            "Hot desert climate! 🌵",
            "Dry heat conditions! ☀️",
            "Desert living lifestyle! 🌵",
            "Southwest living is unique! 🏜️"
        ],
        "Minnesota": [
            "Cold winter weather! ❄️", 
            "Bundle up for the cold! 🧥",
            "Snow season vibes! ⛄",
            "Northern winters are intense! 🥶"
        ],
        "Florida": [
            "Humid tropical climate! 🌴",
            "Watch out for alligators! 🐊", 
            "Beach lifestyle, different vibe! 🏖️",
            "Southern tropics! 🌺"
        ],
        "California": [
            "Great surfing weather! 🏄",
            "Golden state living! ✨",
            "West coast lifestyle!",
            "California dreaming! 😎"
        ]
    }

    # Time-based greetings
    TIME_GREETINGS = {
        "morning": [
            "Good morning, sunshine! 🌅",
            "Rise and shine! ☀️",
            "Beautiful morning ahead! 🌴",
            "Morning energy is great!"
        ],
        "afternoon": [
            "Afternoon productivity! 🌞",
            "Midday focus time! 💪",
            "High energy afternoon! ⬆️",
            "Afternoon hustle time! 🏃‍♂️"
        ],
        "evening": [
            "Evening relaxation time! 🌅",
            "Sunset time, relax time! 🌇", 
            "Night time, right time! 🌙",
            "Evening chill session! 😌"
        ]
    }

    @classmethod
    def get_random_greeting(cls) -> str:
        """Get a random standard greeting"""
        return random.choice(cls.GREETINGS)

    @classmethod  
    def get_success_message(cls) -> str:
        """Get a random success message"""
        return random.choice(cls.SUCCESS_MESSAGES)

    @classmethod
    def get_error_message(cls) -> str:
        """Get a random error message with positive spirit"""
        return random.choice(cls.ERROR_MESSAGES)

    @classmethod
    def get_loading_message(cls) -> str:
        """Get a random loading message"""
        return random.choice(cls.LOADING_MESSAGES)

    @classmethod
    def get_state_expression(cls, state: str) -> str:
        """Get a state-specific expression"""
        expressions = cls.STATE_EXPRESSIONS.get(state, ["Great location wherever you are! 🌍"])
        return random.choice(expressions)

    @classmethod
    def get_time_greeting(cls, hour: int = None) -> str:
        """Get time-appropriate greeting"""
        if hour is None:
            from datetime import datetime
            hour = datetime.now().hour

        if 5 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 17:
            time_period = "afternoon" 
        else:
            time_period = "evening"

        return random.choice(cls.TIME_GREETINGS[time_period])

    @classmethod
    def get_tax_advice(cls) -> str:
        """Get professional tax wisdom"""
        return random.choice(cls.TAX_ADVICE)

    @classmethod
    def get_budget_wisdom(cls) -> str:
        """Get professional budget wisdom"""
        return random.choice(cls.BUDGET_WISDOM)

# Convenience functions for easy use throughout the app
def standard_greeting():
    """Quick access to standard greeting"""
    return StandardExpressions.get_random_greeting()

def standard_success():
    """Quick access to success message"""
    return StandardExpressions.get_success_message()

def standard_loading():
    """Quick access to loading message"""
    return StandardExpressions.get_loading_message()

def standard_error():
    """Quick access to error message with positive spirit"""
    return StandardExpressions.get_error_message()

def standard_state_vibe(state: str):
    """Quick access to state-specific vibes"""
    return StandardExpressions.get_state_expression(state)

def standard_time_vibe():
    """Quick access to time-appropriate greeting"""
    return StandardExpressions.get_time_greeting()