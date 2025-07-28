
import streamlit as st

def render_floating_actions():
    """Render floating action buttons for quick tasks"""
    
    # Floating action button CSS
    st.markdown("""
    <style>
    .floating-actions {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .fab {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        text-decoration: none;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    .fab-primary {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
    }
    
    .fab-secondary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .fab-info {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    @media (max-width: 768px) {
        .floating-actions {
            bottom: 80px; /* Account for mobile browser bars */
            right: 15px;
        }
        .fab {
            width: 48px;
            height: 48px;
            font-size: 20px;
        }
    }
    </style>
    
    <div class="floating-actions">
        <button class="fab fab-primary" onclick="document.querySelector('[data-testid=stSidebar] button:contains(📅)').click()" title="Quick Log Day">
            📅
        </button>
        <button class="fab fab-secondary" onclick="document.querySelector('[data-testid=stSidebar] button:contains(💰)').click()" title="Quick Budget Check">
            💰
        </button>
        <button class="fab fab-info" onclick="document.querySelector('[data-testid=stSidebar] button:contains(🤖)').click()" title="Ask AI">
            🤖
        </button>
    </div>
    """, unsafe_allow_html=True)

def render_quick_action_panel():
    """Render quick action panel at top of dashboard with Hawaiian vibes"""
    
    from utils.hawaii_expressions import da_kine_greeting
    st.markdown(f"### ⚡ Quick Actions - {da_kine_greeting()}")
    
    # Make it mobile-responsive
    is_mobile = st.session_state.get('mobile_view', False)
    
    if is_mobile:
        # Stack buttons vertically on mobile
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📅 Log Da Kine", use_container_width=True, type="primary"):
                st.session_state.quick_action = "log_day"
                st.switch_page("📅 Day Tracker")
            
            if st.button("🤖 Ask Bruddah AI", use_container_width=True):
                st.session_state.quick_action = "ask_ai"
                st.switch_page("🤖 AI Assistant")
        
        with col2:
            if st.button("💰 Check Money", use_container_width=True):
                st.session_state.quick_action = "check_budget"
                st.switch_page("💰 Budgets")
            
            if st.button("📊 Full Report", use_container_width=True):
                st.session_state.quick_action = "view_report"
                st.switch_page("📋 Reports")
    else:
        # Desktop layout - 4 columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📅 Log Today", use_container_width=True, type="primary"):
                st.session_state.quick_action = "log_day"
                st.switch_page("📅 Day Tracker")
        
        with col2:
            if st.button("💰 Check Budget", use_container_width=True):
                st.session_state.quick_action = "check_budget"
                st.switch_page("💰 Budgets")
        
        with col3:
            if st.button("🤖 Ask AI Kokua", use_container_width=True):
                st.session_state.quick_action = "ask_ai"
                st.switch_page("🤖 AI Assistant")
        
        with col4:
            if st.button("📊 Full Report", use_container_width=True):
                st.session_state.quick_action = "view_report"
                st.switch_page("📋 Reports")
