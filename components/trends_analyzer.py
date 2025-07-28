
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

class TrendsAnalyzer:
    """Analyze and display user trends"""
    
    @staticmethod
    def generate_mock_daily_data():
        """Generate sample daily data for trends (in real app, this would come from logs)"""
        # Create sample data for last 30 days
        dates = []
        states = []
        
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            dates.append(date)
            # Mock pattern: more Arizona in winter months, more Minnesota in summer
            if date.month in [11, 12, 1, 2, 3]:  # Winter months
                states.append('Arizona' if i % 3 != 0 else 'Minnesota')
            else:  # Summer months
                states.append('Minnesota' if i % 3 != 0 else 'Arizona')
        
        return pd.DataFrame({
            'date': dates,
            'state': states
        })
    
    @staticmethod
    def render_monthly_trends():
        """Render monthly residency trends"""
        st.markdown("### 📈 Monthly Trends")
        
        # Get mock data (replace with real data in production)
        df = TrendsAnalyzer.generate_mock_daily_data()
        
        # Group by month and state
        df['month'] = df['date'].dt.strftime('%Y-%m')
        monthly_counts = df.groupby(['month', 'state']).size().reset_index(name='days')
        
        # Create stacked bar chart
        fig = px.bar(monthly_counts, 
                    x='month', 
                    y='days', 
                    color='state',
                    title='Monthly Residency Pattern',
                    color_discrete_map={'Arizona': '#ff6b35', 'Minnesota': '#4a90e2'})
        
        fig.update_layout(
            height=400,
            xaxis_title="Month",
            yaxis_title="Days",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_spending_trends():
        """Render spending trends analysis"""
        st.markdown("### 💸 Spending Trends")
        
        budgets = st.session_state.get('home_budgets', {})
        if not budgets:
            st.info("Add property budgets to see spending trends!")
            return
        
        # Create spending comparison
        spending_data = []
        for home, budget in budgets.items():
            for category, amount in budget.items():
                spending_data.append({
                    'home': home,
                    'category': category,
                    'amount': amount
                })
        
        df = pd.DataFrame(spending_data)
        
        # Spending by category across homes
        fig = px.bar(df, 
                    x='category', 
                    y='amount', 
                    color='home',
                    title='Monthly Spending by Category',
                    text='amount')
        
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_insights_summary():
        """Render key insights"""
        st.markdown("### 💡 Smart Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🏠 Residency Patterns**
            - Most active state: Arizona
            - Longest stay: 45 days consecutive  
            - Best compliance month: January
            - Recommended next move: Minnesota
            """)
        
        with col2:
            st.markdown("""
            **💰 Spending Insights**
            - Highest cost location: Arizona
            - Most expensive category: Property Tax
            - Potential savings: $200/month
            - Budget optimization available
            """)

def render_trends_analysis():
    """Main function to render all trends"""
    TrendsAnalyzer.render_monthly_trends()
    TrendsAnalyzer.render_spending_trends()
    TrendsAnalyzer.render_insights_summary()
