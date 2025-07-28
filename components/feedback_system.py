
"""
User feedback and support system for the Snowbird application.
"""
import streamlit as st
import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional
from utils.logging_config import logger

class FeedbackManager:
    """Manage user feedback and support requests"""
    
    def __init__(self):
        self.feedback_file = Path("logs/user_feedback.jsonl")
        self.feedback_file.parent.mkdir(exist_ok=True)
    
    def submit_feedback(self, feedback_type: str, message: str, email: str = None, rating: int = None) -> bool:
        """Submit user feedback"""
        try:
            feedback_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "type": feedback_type,
                "message": message,
                "email": email,
                "rating": rating,
                "session_id": st.session_state.get("session_id", "unknown"),
                "user_agent": st.get_option("browser.serverAddress") or "unknown"
            }
            
            with open(self.feedback_file, "a") as f:
                f.write(json.dumps(feedback_entry) + "\n")
            
            logger.info(f"Feedback submitted: {feedback_type}", extra=feedback_entry)
            return True
            
        except Exception as e:
            logger.error(f"Failed to submit feedback: {e}")
            return False
    
    def get_feedback_stats(self) -> Dict[str, int]:
        """Get feedback statistics for admin dashboard"""
        stats = {"total": 0, "bug_report": 0, "feature_request": 0, "general": 0, "rating_average": 0}
        total_rating = 0
        rating_count = 0
        
        try:
            if self.feedback_file.exists():
                with open(self.feedback_file, "r") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            stats["total"] += 1
                            feedback_type = entry.get("type", "general")
                            if feedback_type in stats:
                                stats[feedback_type] += 1
                            
                            if entry.get("rating"):
                                total_rating += entry["rating"]
                                rating_count += 1
                        except json.JSONDecodeError:
                            continue
            
            if rating_count > 0:
                stats["rating_average"] = round(total_rating / rating_count, 1)
            
        except Exception as e:
            logger.error(f"Failed to get feedback stats: {e}")
        
        return stats

def render_feedback_form():
    """Render the feedback form component"""
    st.subheader("📝 Share Your Feedback")
    
    feedback_manager = FeedbackManager()
    
    with st.form("feedback_form"):
        feedback_type = st.selectbox(
            "What type of feedback is this?",
            ["general", "bug_report", "feature_request", "support_request"],
            format_func=lambda x: {
                "general": "💬 General Feedback",
                "bug_report": "🐛 Bug Report", 
                "feature_request": "✨ Feature Request",
                "support_request": "🆘 Support Request"
            }[x]
        )
        
        message = st.text_area(
            "Your feedback *",
            placeholder="Please describe your feedback in detail...",
            height=120,
            help="Be as specific as possible to help us improve the app"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            rating = st.select_slider(
                "How would you rate your experience?",
                options=[1, 2, 3, 4, 5],
                value=5,
                format_func=lambda x: "⭐" * x
            )
        
        with col2:
            email = st.text_input(
                "Email (optional)",
                placeholder="your@email.com",
                help="Leave your email if you'd like a response"
            )
        
        submitted = st.form_submit_button("Submit Feedback", type="primary")
        
        if submitted:
            if message.strip():
                success = feedback_manager.submit_feedback(
                    feedback_type=feedback_type,
                    message=message,
                    email=email if email.strip() else None,
                    rating=rating
                )
                
                if success:
                    st.success("🎉 Thank you for your feedback! We appreciate you helping us improve.")
                    st.balloons()
                else:
                    st.error("❌ Failed to submit feedback. Please try again.")
            else:
                st.error("Please enter your feedback message.")

def render_help_section():
    """Render the help and FAQ section"""
    st.subheader("❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How does the 183-day tax rule work?",
            "answer": """
            The 183-day rule determines tax residency. If you spend 183+ days in a state during a tax year, 
            you may become a tax resident and owe state income taxes there. Snowbird helps you track your days 
            to stay under this threshold in states where you don't want to establish tax residency.
            """
        },
        {
            "question": "How do I log my location each day?",
            "answer": """
            Use the Day Tracker tab to log which state you're in each day. You can:
            - Log individual days
            - Bulk log multiple days for trips
            - Edit past entries if you made mistakes
            - View your progress toward the 183-day limit
            """
        },
        {
            "question": "Can I export my data for tax purposes?",
            "answer": """
            Yes! Go to the Admin tab and use the "Export Data" feature to download your location logs 
            as a CSV file. This creates a detailed record you can provide to your tax advisor.
            """
        },
        {
            "question": "How does the AI assistant work?",
            "answer": """
            The AI assistant uses your location and budget data to provide personalized financial advice. 
            It can help with tax strategies, budget optimization, and planning for your seasonal lifestyle. 
            Your data stays private and is never stored by the AI service.
            """
        },
        {
            "question": "Is my financial data secure?",
            "answer": """
            Yes! Your data is encrypted in your browser session and never permanently stored on our servers. 
            We use industry-standard security practices and you can optionally sync with Firebase for backup.
            """
        },
        {
            "question": "Can I use this app offline?",
            "answer": """
            Snowbird works as a Progressive Web App (PWA). You can install it on your phone/computer 
            and use basic features offline. Data will sync when you're back online.
            """
        }
    ]
    
    for i, faq in enumerate(faqs):
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])
    
    st.markdown("---")
    st.subheader("📧 Need More Help?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📖 Documentation**
        
        Check out our comprehensive docs for detailed guides and tutorials.
        """)
        if st.button("View Docs", key="docs_btn"):
            st.info("📚 Full documentation is available in the `/docs` folder of this project.")
    
    with col2:
        st.markdown("""
        **🐛 Report a Bug**
        
        Found something broken? Let us know and we'll fix it quickly.
        """)
        if st.button("Report Bug", key="bug_btn"):
            st.session_state.show_feedback = True
            st.rerun()
    
    with col3:
        st.markdown("""
        **💡 Feature Request**
        
        Have an idea for improvement? We'd love to hear it!
        """)
        if st.button("Suggest Feature", key="feature_btn"):
            st.session_state.show_feedback = True
            st.rerun()

def render_contact_info():
    """Render contact information"""
    st.markdown("""
    ### 📞 Contact Information
    
    - **Email**: support@snowbirdapp.com
    - **GitHub Issues**: [Report issues](https://github.com/yourusername/snowbird-app/issues)
    - **Documentation**: Available in `/docs` folder
    - **Response Time**: We typically respond within 24-48 hours
    
    ### 🔗 Useful Links
    
    - [Privacy Policy](#) - How we protect your data
    - [Terms of Service](#) - Usage guidelines  
    - [Tax Resources](#) - External tax guidance
    - [Seasonal Living Tips](#) - Lifestyle advice
    """)

# Global feedback manager instance
feedback_manager = FeedbackManager()
