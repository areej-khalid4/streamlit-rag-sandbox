import time
import streamlit as st
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    ChatGoogleGenerativeAI = None

try:
    from langchain_ollama import ChatOllama
except Exception:
    ChatOllama = None

def get_llm(provider: str, temperature: float, google_api_key: str = "", model_name: str = "gemini-2.0-flash"):
    """
    Factory function to initialize LLM instances based on selected provider.
    """
    if provider == "Gemini API":
        if ChatGoogleGenerativeAI is None:
            st.sidebar.error("langchain-google-genai is not available in this environment.")
            return None
        if not google_api_key:
            st.sidebar.warning("Please provide a Gemini API Key to run real models.")
            return None

        # Clean model string
        target_model = model_name if model_name else "gemini-2.0-flash"
        return ChatGoogleGenerativeAI(
            model=target_model, 
            google_api_key=google_api_key, 
            temperature=temperature, 
            max_retries=1
        )
    elif provider == "Local Ollama":
        if ChatOllama is None:
            st.sidebar.warning("langchain-ollama is not installed in this environment.")
            return None
        return ChatOllama(
            model="llama3", 
            temperature=temperature, 
            base_url="http://localhost:11434",
            options={
                "stop": ["Question:", "Observation:", "\nQuestion:", "\nObservation:", "\nThought:"]
            }
        )
    else:
        return None

def generate_mock_stream(prompt: str, provider: str = "Mock Provider", temperature: float = 0.3):
    """
    Simulated word-by-word streaming LLM completion generator (offline fallback).
    """
    words = (
        f"This is a simulated Mock LLM response to your prompt:\n\n"
        f"\"{prompt}\"\n\n"
        f"To interact with live generative models, please configure either Local Ollama on port 11434 "
        f"or supply a Gemini API Key in the sidebar controllers.\n\n"
        f"Your inputs were: temperature={temperature}, provider={provider}."
    ).split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.04)
