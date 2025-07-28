
import streamlit as st
from functools import wraps
import time
import hashlib
from typing import Any, Callable

def smart_cache(ttl: int = 300, key_func: Callable = None):
    """Smart caching decorator with TTL and custom key function"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                key_data = f"{func.__name__}_{str(args)}_{str(kwargs)}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Check cache
            if hasattr(st.session_state, f"cache_{cache_key}"):
                cached_data, timestamp = getattr(st.session_state, f"cache_{cache_key}")
                if time.time() - timestamp < ttl:
                    return cached_data
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            setattr(st.session_state, f"cache_{cache_key}", (result, time.time()))
            
            return result
        return wrapper
    return decorator

@smart_cache(ttl=60)  # Cache for 1 minute
def get_tax_status_summary():
    """Cached tax status calculation"""
    if not hasattr(st.session_state, 'states') or not st.session_state.states:
        return {"status": "no_data", "message": "No location data available"}
    
    max_days = max(st.session_state.states.values())
    threshold = getattr(st.session_state, 'tax_threshold', 183)
    remaining = threshold - max_days
    
    if remaining <= 0:
        return {"status": "tax_resident", "message": "Tax resident status"}
    elif remaining <= 10:
        return {"status": "critical", "message": f"{remaining} days until tax residency"}
    elif remaining <= 30:
        return {"status": "caution", "message": f"{remaining} days remaining"}
    else:
        return {"status": "safe", "message": f"{remaining} days remaining"}
