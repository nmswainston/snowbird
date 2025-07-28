
"""
Performance optimization utilities for the Snowbird application.
"""
import streamlit as st
import time
import functools
from typing import Any, Callable, Dict, Optional
import hashlib
import json

class PerformanceOptimizer:
    """Optimize app performance with intelligent caching and lazy loading"""
    
    @staticmethod
    @st.cache_data(ttl=3600, max_entries=100)
    def cached_ai_response(query: str, user_context: str) -> str:
        """Cache AI responses to avoid repeated API calls"""
        # This will be called by the AI assistant
        return f"cached_response_for_{hashlib.md5(f'{query}_{user_context}'.encode()).hexdigest()}"
    
    @staticmethod
    @st.cache_data(ttl=1800)  # 30 minutes
    def calculate_tax_projections(states_data: Dict[str, int], threshold: int) -> Dict[str, Any]:
        """Cache expensive tax calculations"""
        total_days = sum(states_data.values())
        remaining_days = 365 - total_days
        
        projections = {}
        for state, days in states_data.items():
            if days > 0:
                days_to_threshold = threshold - days
                risk_level = "HIGH" if days > threshold * 0.9 else "MEDIUM" if days > threshold * 0.7 else "LOW"
                projections[state] = {
                    "current_days": days,
                    "days_to_threshold": days_to_threshold,
                    "risk_level": risk_level,
                    "percentage_used": (days / threshold) * 100
                }
        
        return {
            "projections": projections,
            "total_days": total_days,
            "remaining_days": remaining_days,
            "calculated_at": time.time()
        }
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def generate_budget_analytics(budget_data: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Cache budget analysis calculations"""
        analytics = {
            "total_monthly": 0,
            "by_category": {},
            "by_location": {},
            "cost_comparison": {}
        }
        
        for location, categories in budget_data.items():
            location_total = sum(categories.values())
            analytics["by_location"][location] = location_total
            analytics["total_monthly"] += location_total
            
            for category, amount in categories.items():
                if category not in analytics["by_category"]:
                    analytics["by_category"][category] = 0
                analytics["by_category"][category] += amount
        
        # Cost comparison between locations
        locations = list(budget_data.keys())
        if len(locations) >= 2:
            loc1, loc2 = locations[0], locations[1]
            analytics["cost_comparison"] = {
                "higher_cost_location": loc1 if analytics["by_location"][loc1] > analytics["by_location"][loc2] else loc2,
                "difference": abs(analytics["by_location"][loc1] - analytics["by_location"][loc2]),
                "percentage_difference": abs(analytics["by_location"][loc1] - analytics["by_location"][loc2]) / max(analytics["by_location"].values()) * 100
            }
        
        return analytics

def lazy_load_component(component_func: Callable, trigger_text: str = "Load Component", **kwargs) -> Any:
    """Lazy load expensive components"""
    if st.button(trigger_text):
        with st.spinner("Loading..."):
            return component_func(**kwargs)
    return None

def performance_monitor(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if execution_time > 1.0:  # Log slow operations
            st.toast(f"⚠️ {func.__name__} took {execution_time:.2f}s", icon="⏱️")
        
        return result
    return wrapper

class ImageOptimizer:
    """Optimize image loading and display"""
    
    @staticmethod
    def compress_and_cache_image(image_path: str, max_width: int = 800) -> str:
        """Compress and cache images for better performance"""
        # In a real implementation, you'd use PIL to resize/compress
        # For now, return the original path
        return image_path
    
    @staticmethod
    def lazy_load_image(image_path: str, alt_text: str, max_width: int = None) -> None:
        """Lazy load images with proper alt text"""
        width_style = f"max-width: {max_width}px;" if max_width else ""
        st.markdown(f"""
        <img src="{image_path}" 
             alt="{alt_text}" 
             loading="lazy" 
             style="{width_style} height: auto;"
             onerror="this.style.display='none'">
        """, unsafe_allow_html=True)

# Memory usage monitoring
def monitor_memory_usage():
    """Monitor and display memory usage"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    if memory_mb > 500:  # Alert if using more than 500MB
        st.warning(f"⚠️ High memory usage: {memory_mb:.1f} MB")
    
    return memory_mb
