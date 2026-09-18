import streamlit as st

def apply_custom_css():
    """
    Applies custom dark glassmorphic styling to the Streamlit app.
    """
    st.markdown("""
    <style>
        .stApp {
            background-color: #06070a;
            color: #f3f4f6;
        }
        .glass-card {
            background: rgba(17, 20, 31, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        .highlight-label {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #10b981;
        }
        .tab-header {
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_branding():
    """
    Renders sidebar brand header.
    """
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); display: flex; align-items: center; justify-content: center; font-weight: 900; color: white;">Z</div>
        <div>
            <h2 style="margin: 0; font-size: 18px; line-height: 1;">ZENITH</h2>
            <span style="font-size: 9px; color: #8b5cf6; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;">AI Streamlit Sandbox</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
