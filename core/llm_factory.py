import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

def get_llm(provider: str, temperature: float, google_api_key: str = ""):
    """
    Factory function to initialize LLM instances based on selected provider.
    """
    if provider == "Gemini API":
        if not google_api_key:
            st.sidebar.warning("Please provide a Gemini API Key to run real models.")
            return None
        return ChatGoogleGenerativeAI(
            model="gemini-3.6-flash", 
            google_api_key=google_api_key, 
            temperature=temperature, 
            max_retries=0
        )
    elif provider == "Local Ollama":
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
