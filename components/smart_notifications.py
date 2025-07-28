
import streamlit as st
import datetime
from typing import List, Dict, Any

class SmartNotificationSystem:
    """Intelligent notification system for Snowbird app"""
    
    @staticmethod
    def get_priority_alerts() -> List[Dict[str, Any]]:
        """Generate priority alerts based on user data"""
        alerts = []
        
        # Get current data
        states = st.session_state.get('states', {})
        tax_threshold = st.session_state.get('tax_threshold', 183)
        
        for state, days in states.items():
            # High priority: Close to threshold
            if days > tax_threshold * 0.9:
                alerts.append({
                    'type': 'danger',
                    'icon': '🚨',
                    'title': f'{state} Tax Risk',
                    'message': f'Only {tax_threshold - days} days left before tax residency!',
                    'priority': 'high'
                })
            
            # Medium priority: Getting close
            elif days > tax_threshold * 0.75:
                alerts.append({
                    'type': 'warning', 
                    'icon': '⚠️',
                    'title': f'{state} Monitor',
                    'message': f'{days} days logged. Consider planning your moves.',
                    'priority': 'medium'
                })
        
        # Budget alerts
        budgets = st.session_state.get('home_budgets', {})
        for home, budget in budgets.items():
            total = sum(budget.values())
            if total > 3000:  # High budget alert
                alerts.append({
                    'type': 'info',
                    'icon': '💰',
                    'title': 'High Budget Alert',
                    'message': f'{home}: ${total:,}/month - Consider optimization',
                    'priority': 'low'
                })
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        alerts.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return alerts[:5]  # Top 5 alerts
    
    @staticmethod
    def render_notification_banner():
        """Render notification banner at top of dashboard"""
        alerts = SmartNotificationSystem.get_priority_alerts()
        
        if not alerts:
            # Show positive message when no alerts
            st.success("🌊 All systems looking good! You're staying compliant and on budget.")
            return
        
        # Show alerts in compact banner
        for alert in alerts:
            if alert['type'] == 'danger':
                st.error(f"{alert['icon']} **{alert['title']}**: {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"{alert['icon']} **{alert['title']}**: {alert['message']}")
            else:
                st.info(f"{alert['icon']} **{alert['title']}**: {alert['message']}")
    
    @staticmethod
    def render_notification_sidebar():
        """Render notifications in sidebar"""
        with st.sidebar:
            st.markdown("### 🔔 Smart Alerts")
            
            alerts = SmartNotificationSystem.get_priority_alerts()
            
            if alerts:
                for alert in alerts[:3]:  # Show top 3 in sidebar
                    st.markdown(f"""
                    <div style="background: {'#fee2e2' if alert['type'] == 'danger' else '#fef3c7' if alert['type'] == 'warning' else '#e0f2fe'}; 
                                padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem; border-left: 3px solid {'#dc2626' if alert['type'] == 'danger' else '#f59e0b' if alert['type'] == 'warning' else '#0284c7'};">
                        <strong>{alert['icon']} {alert['title']}</strong><br>
                        <small>{alert['message']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🌊 All good!")

# Usage functions
def render_smart_notifications():
    """Main function to render notifications"""
    SmartNotificationSystem.render_notification_banner()

def render_sidebar_notifications():
    """Render sidebar notifications"""
    SmartNotificationSystem.render_notification_sidebar()
