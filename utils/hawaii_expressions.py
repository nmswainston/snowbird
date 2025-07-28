"""
Hawaiian expressions and local slang for the Snowbird app
Bringing that authentic island vibe to your seasonal living experience
"""

import random
from typing import List, Dict

class HawaiiExpressions:
    """Hawaiian and local pidgin expressions for the Snowbird app"""

    # Da kine greetings and positive vibes
    GREETINGS = [
        "Aloha brah! 🤙",
        "Shoots, howzit! 🌺", 
        "What's da buggah? 🏄‍♂️",
        "Eh, how you stay? 🌊",
        "Rajah dat! 🌴",
        "Chee-hoo! 🏖️"
    ]

    # Success messages with local flavor
    SUCCESS_MESSAGES = [
        "Shoots! Das da kine! ✨",
        "Rajah! All pau! 🎉",
        "Broke da mouth good! 🤙",
        "Stay good to go! 🏄‍♂️",
        "No worries, bruddah! 😎",
        "Das how we roll! 🌊"
    ]

    # Error messages with aloha spirit
    ERROR_MESSAGES = [
        "Shoots, someting stay pilau... 😅",
        "Eh, da kine stay broke! 🔧",
        "No make like dat! Try again! 💪",
        "Wot da heck? No can! 🤔",
        "Auwe! Someting went sideways! 🌀",
        "Eh, stay all hamajang! Let's fix! 🛠️"
    ]

    # Loading and waiting messages
    LOADING_MESSAGES = [
        "Hang loose, loading da kine... 🏄‍♂️",
        "Stay patient, bruddah... 🌊",
        "Almost pau, just small kine wait... ⏰",
        "Getting da goods ready... 📦",
        "Making da magic happen... ✨",
        "Chill out, almost done... 😎"
    ]

    # Tax and financial advice with local wisdom
    TAX_ADVICE = [
        "No make pilikia with da taxes, brah! 📊",
        "Keep track da kine or IRS stay mad! 💸",
        "Smart money moves, island style! 🏝️",
        "Stay organized like one good local! 📝",
        "No mess around with da government! ⚖️",
        "Financial planning, Hawaii style! 🌺"
    ]

    # Budget wisdom
    BUDGET_WISDOM = [
        "Mo money, mo problems... but still need track! 💰",
        "Spend wise like da old timers! 👴",
        "Save some coin for da keiki! 👶",
        "Budget tight like one good lei! 🌺",
        "No blow all da money on one place! 🎯",
        "Smart spending da Hawaiian way! 🏖️"
    ]

    # State-specific expressions
    STATE_EXPRESSIONS = {
        "Arizona": [
            "Hot like da desert, brah! 🌵",
            "Dry heat, but still hot! ☀️",
            "Cactus country vibes! 🌵",
            "Desert living stay different! 🏜️"
        ],
        "Minnesota": [
            "Cold like da mountain top! ❄️", 
            "Bundle up, bruddah! 🧥",
            "Snow day vibes! ⛄",
            "Mainland winter stay real! 🥶"
        ],
        "Florida": [
            "Humid like da jungle! 🌴",
            "Gator country, watch out! 🐊", 
            "Beach vibes, but different! 🏖️",
            "Mainland tropics! 🌺"
        ],
        "California": [
            "Surf's up, California style! 🏄",
            "Golden state golden vibes! ✨",
            "West coast, best coast! 🌊",
            "Cali living da dream! 😎"
        ]
    }

    # Time-based greetings
    TIME_GREETINGS = {
        "morning": [
            "Good morning, sunshine! 🌅",
            "Rise and grind, island style! ☀️",
            "Another beautiful day in paradise! 🌴",
            "Morning waves looking good! 🌊"
        ],
        "afternoon": [
            "Afternoon vibes stay strong! 🌞",
            "Midday grindtime! 💪",
            "Sun stay high, energy stay higher! ⬆️",
            "Afternoon hustle da kine! 🏃‍♂️"
        ],
        "evening": [
            "Evening pau hana vibes! 🌅",
            "Sunset time, relax time! 🌇", 
            "Night time, right time! 🌙",
            "Evening chill session! 😌"
        ]
    }

    @classmethod
    def get_random_greeting(cls) -> str:
        """Get a random Hawaiian greeting"""
        return random.choice(cls.GREETINGS)

    @classmethod  
    def get_success_message(cls) -> str:
        """Get a random success message"""
        return random.choice(cls.SUCCESS_MESSAGES)

    @classmethod
    def get_error_message(cls) -> str:
        """Get a random error message with aloha spirit"""
        return random.choice(cls.ERROR_MESSAGES)

    @classmethod
    def get_loading_message(cls) -> str:
        """Get a random loading message"""
        return random.choice(cls.LOADING_MESSAGES)

    @classmethod
    def get_state_expression(cls, state: str) -> str:
        """Get a state-specific expression"""
        expressions = cls.STATE_EXPRESSIONS.get(state, ["Stay good wherever you stay! 🌍"])
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
        """Get Hawaiian-style tax wisdom"""
        return random.choice(cls.TAX_ADVICE)

    @classmethod
    def get_budget_wisdom(cls) -> str:
        """Get local budget wisdom"""
        return random.choice(cls.BUDGET_WISDOM)

# Convenience functions for easy use throughout the app
def da_kine_greeting():
    """Quick access to Hawaiian greeting"""
    return HawaiiExpressions.get_random_greeting()

def da_kine_success():
    """Quick access to success message"""
    return HawaiiExpressions.get_success_message()

def da_kine_loading():
    """Quick access to loading message"""
    return HawaiiExpressions.get_loading_message()

def da_kine_error():
    """Quick access to error message with aloha spirit"""
    return HawaiiExpressions.get_error_message()

def da_kine_state_vibe(state: str):
    """Quick access to state-specific vibes"""
    return HawaiiExpressions.get_state_expression(state)

def da_kine_time_vibe():
    """Quick access to time-appropriate greeting"""
    return HawaiiExpressions.get_time_greeting()