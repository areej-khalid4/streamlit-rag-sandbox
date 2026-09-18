import os
import streamlit as st
from config import BASE_DIR, get_gemini_api_key
from core.llm_factory import get_llm
from ui.styles import apply_custom_css, render_sidebar_branding
from ui.tab_playground import render_tab_playground
from ui.tab_rag import render_tab_rag
from ui.tab_agents import render_tab_agents
from ui.tab_eval import render_tab_eval

# ---------------------------------------------------------
# Page Configuration & CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Zenith | AI & RAG Streamlit Sandbox",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# ---------------------------------------------------------
# Sidebar Configurations
# ---------------------------------------------------------
render_sidebar_branding()

st.sidebar.subheader("Model Configuration")
provider = st.sidebar.selectbox("LLM Provider", ["Mock Provider", "Local Ollama", "Gemini API"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

google_api_key = st.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    value=get_gemini_api_key()
)

# Shared LLM getter callback
def get_current_llm():
    return get_llm(provider=provider, temperature=temperature, google_api_key=google_api_key)

# ---------------------------------------------------------
# Main Tabs Layout Routing
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 LLM & Tokenizer",
    "📚 RAG Studio",
    "🤖 Agentic Workflows (LangGraph)",
    "📊 Grounding Evaluator"
])

with tab1:
    render_tab_playground(get_current_llm)

with tab2:
    render_tab_rag(get_current_llm)

with tab3:
    render_tab_agents(get_current_llm)

with tab4:
    render_tab_eval()
