
"""
AI Answer Rating System for the Snowbird application.
Handles rating collection, storage, and analytics for AI responses.
"""
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import streamlit as st
from utils.logging_config import logger

class AIRatingManager:
    """Manage AI answer ratings and feedback"""
    
    def __init__(self):
        self.ratings_file = Path("logs/ai_ratings.jsonl")
        self.ratings_file.parent.mkdir(exist_ok=True)
    
    def record_rating(self, question: str, response: str, rating: str, session_id: str = None) -> bool:
        """
        Record a user rating for an AI response
        
        Args:
            question: The user's original question
            response: The AI's response text
            rating: Either 'thumbs_up' or 'thumbs_down'
            session_id: Optional session identifier
        
        Returns:
            bool: True if rating was successfully recorded
        """
        try:
            rating_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "question": question,
                "response": response,
                "rating": rating,
                "session_id": session_id or st.session_state.get("session_id", "unknown"),
                "question_length": len(question),
                "response_length": len(response)
            }
            
            # Write to JSONL file (one JSON object per line)
            with open(self.ratings_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(rating_entry, ensure_ascii=False) + "\n")
            
            logger.info(f"AI rating recorded: {rating}", extra={
                "rating": rating,
                "question_preview": question[:50] + "..." if len(question) > 50 else question
            })
            return True
            
        except Exception as e:
            logger.error(f"Failed to record AI rating: {e}")
            return False
    
    def get_rating_stats(self) -> Dict[str, any]:
        """
        Get aggregated rating statistics for admin dashboard
        
        Returns:
            Dict containing rating statistics
        """
        stats = {
            "total_ratings": 0,
            "thumbs_up": 0,
            "thumbs_down": 0,
            "thumbs_up_percentage": 0,
            "average_question_length": 0,
            "average_response_length": 0,
            "recent_ratings": []
        }
        
        try:
            if not self.ratings_file.exists():
                return stats
            
            ratings_data = []
            total_q_length = 0
            total_r_length = 0
            
            with open(self.ratings_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        ratings_data.append(entry)
                        
                        # Count ratings
                        if entry.get("rating") == "thumbs_up":
                            stats["thumbs_up"] += 1
                        elif entry.get("rating") == "thumbs_down":
                            stats["thumbs_down"] += 1
                        
                        # Track lengths for averages
                        total_q_length += entry.get("question_length", 0)
                        total_r_length += entry.get("response_length", 0)
                        
                    except (json.JSONDecodeError, KeyError):
                        continue
            
            stats["total_ratings"] = len(ratings_data)
            
            # Calculate percentages
            if stats["total_ratings"] > 0:
                stats["thumbs_up_percentage"] = round(
                    (stats["thumbs_up"] / stats["total_ratings"]) * 100, 1
                )
                stats["average_question_length"] = round(total_q_length / stats["total_ratings"])
                stats["average_response_length"] = round(total_r_length / stats["total_ratings"])
            
            # Get recent ratings (last 10)
            stats["recent_ratings"] = sorted(
                ratings_data, 
                key=lambda x: x.get("timestamp", ""), 
                reverse=True
            )[:10]
            
        except Exception as e:
            logger.error(f"Failed to get rating stats: {e}")
        
        return stats
    
    def get_recent_feedback(self, limit: int = 5) -> List[Dict]:
        """Get recent feedback entries for display"""
        try:
            if not self.ratings_file.exists():
                return []
            
            feedback_entries = []
            with open(self.ratings_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        feedback_entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            # Return most recent entries
            return sorted(
                feedback_entries,
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent feedback: {e}")
            return []

def render_ai_rating_buttons(question: str, response: str, unique_key: str = ""):
    """
    Render thumbs up/down rating buttons for an AI response
    
    Args:
        question: The original user question
        response: The AI response text
        unique_key: Unique identifier for the button widgets
    """
    rating_manager = AIRatingManager()
    
    # Create columns for the rating buttons
    st.markdown("---")
    st.markdown("**Was this response helpful?**")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("👍", key=f"thumbs_up_{unique_key}", help="This response was helpful"):
            # Record the positive rating
            success = rating_manager.record_rating(
                question=question,
                response=response,
                rating="thumbs_up"
            )
            
            if success:
                st.success("👍 Thank you for your feedback!")
                st.balloons()
            else:
                st.error("Failed to record rating. Please try again.")
    
    with col2:
        if st.button("👎", key=f"thumbs_down_{unique_key}", help="This response was not helpful"):
            # Record the negative rating
            success = rating_manager.record_rating(
                question=question,
                response=response,
                rating="thumbs_down"
            )
            
            if success:
                st.success("👎 Thank you for your feedback! We'll work to improve our responses.")
            else:
                st.error("Failed to record rating. Please try again.")

def render_rating_analytics():
    """Render AI rating analytics for the admin dashboard"""
    st.subheader("📊 AI Response Analytics")
    
    rating_manager = AIRatingManager()
    stats = rating_manager.get_rating_stats()
    
    if stats["total_ratings"] == 0:
        st.info("No AI response ratings recorded yet.")
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Ratings",
            value=stats["total_ratings"]
        )
    
    with col2:
        st.metric(
            label="👍 Positive",
            value=stats["thumbs_up"],
            delta=f"{stats['thumbs_up_percentage']}%"
        )
    
    with col3:
        st.metric(
            label="👎 Negative", 
            value=stats["thumbs_down"],
            delta=f"{100 - stats['thumbs_up_percentage']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="Satisfaction Rate",
            value=f"{stats['thumbs_up_percentage']}%"
        )
    
    # Show recent feedback
    st.markdown("---")
    st.subheader("Recent Feedback")
    
    recent_ratings = stats["recent_ratings"]
    if recent_ratings:
        for i, rating in enumerate(recent_ratings):
            with st.expander(f"Rating {i+1} - {rating.get('rating', 'unknown').replace('_', ' ').title()} ({rating.get('timestamp', 'Unknown time')[:10]})"):
                st.write(f"**Question:** {rating.get('question', 'N/A')}")
                st.write(f"**Response:** {rating.get('response', 'N/A')[:200]}...")
                st.write(f"**Rating:** {'👍' if rating.get('rating') == 'thumbs_up' else '👎'}")
    else:
        st.info("No recent ratings to display.")

# Global rating manager instance
ai_rating_manager = AIRatingManager()
