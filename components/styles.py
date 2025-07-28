
import streamlit as st

def load_custom_css():
    """Load custom CSS styles for the Snowbird app"""
    st.markdown("""
    <style>
        /* Import Google Fonts and Lucide Icons */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.js');

        /* Root variables for winter theme */
        :root {
            --primary-blue: #12BDF2;
            --light-blue: #E3F4FD;
            --ice-white: #FFFFFF;
            --snow-gray: #F8FAFC;
            --text-dark: #1E293B;
            --text-light: #64748B;
            --border-light: #E2E8F0;
            --shadow: rgba(18, 189, 242, 0.1);
        }

        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, var(--ice-white) 0%, var(--light-blue) 100%);
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-weight: 400;
            letter-spacing: -0.01em;
        }

        /* Header styling */
        .main-header {
            text-align: center;
            padding: 1.5rem 0;
            background: var(--ice-white);
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px var(--shadow);
            border: 1px solid var(--border-light);
        }

        .main-title {
            color: var(--primary-blue);
            font-size: clamp(1.5rem, 3vw, 2.2rem);
            font-weight: 600;
            margin-bottom: 0.3rem;
            text-shadow: none;
            letter-spacing: -0.02em;
        }

        .subtitle {
            color: var(--text-light);
            font-size: 0.95rem;
            font-weight: 400;
            letter-spacing: -0.01em;
        }

        /* Card styling */
        .winter-card {
            background: var(--ice-white);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px var(--shadow);
            border: 1px solid var(--border-light);
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .winter-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--shadow);
        }

        /* Icon styling */
        .icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            margin-right: 8px;
            vertical-align: middle;
        }

        .icon-large {
            width: 24px;
            height: 24px;
            margin-right: 12px;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-blue) 0%, #0EA5E9 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            letter-spacing: -0.01em !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 15px rgba(18, 189, 242, 0.3) !important;
        }

        /* Status indicators */
        .status-safe { color: #10B981; font-weight: 600; }
        .status-warning { color: #F59E0B; font-weight: 600; }
        .status-danger { color: #EF4444; font-weight: 600; }

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header { padding: 1rem; }
            .main-title { font-size: 1.4rem !important; }
            .winter-card { padding: 1rem; margin: 0.5rem 0; }
            
            /* Touch-friendly button sizing */
            .stButton > button {
                min-height: 44px !important;
                padding: 0.8rem 1.5rem !important;
                font-size: 1rem !important;
            }
        }
    </style>

    <!-- Lucide Icons Script -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            lucide.createIcons();
        });
    </script>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">
            <i data-lucide="home" class="icon-large"></i>
            Snowbird: Your Seasonal Financial Assistant
        </h1>
        <p class="subtitle">Manage your multi-state lifestyle with confidence</p>
    </div>
    """, unsafe_allow_html=True)
