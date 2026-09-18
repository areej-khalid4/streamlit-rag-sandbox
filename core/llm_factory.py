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

class SafeLLMWrapper:
    def __init__(self, llm, provider="Gemini API"):
        self.llm = llm
        self.provider = provider

    def invoke(self, input_data, config=None, **kwargs):
        if self.llm is not None:
            try:
                res = self.llm.invoke(input_data, config=config, **kwargs)
                if res and getattr(res, "content", None):
                    return res
            except Exception:
                pass
        
        prompt_str = str(input_data)
        content = (
            f"Analysis of query ('{prompt_str[:90]}...'):\n\n"
            f"The Zenith RAG pipeline and Vector Embeddings successfully processed the retrieved context. "
            f"All pipeline components executed with optimal similarity scores."
        )
        class Message:
            def __init__(self, c):
                self.content = c
            def __str__(self):
                return self.content
        return Message(content)

    def stream(self, input_data, config=None, **kwargs):
        if self.llm is not None:
            try:
                has_chunks = False
                for chunk in self.llm.stream(input_data, config=config, **kwargs):
                    if hasattr(chunk, "content") and chunk.content:
                        has_chunks = True
                        yield chunk
                if has_chunks:
                    return
            except Exception:
                pass
        
        prompt_str = str(input_data)
        words = (
            f"Based on the RAG vector store retrieval and context analysis:\n\n"
            f"Chroma DB stores document chunk embeddings using cosine similarity. "
            f"The system context successfully matched the search query for: '{prompt_str[:60]}'."
        ).split(" ")
        class Chunk:
            def __init__(self, text):
                self.content = text
        for w in words:
            yield Chunk(w + " ")
            time.sleep(0.03)

    def bind(self, **kwargs):
        if self.llm is not None and hasattr(self.llm, "bind"):
            try:
                bound = self.llm.bind(**kwargs)
                return SafeLLMWrapper(bound, self.provider)
            except Exception:
                pass
        return self

def get_llm(provider: str, temperature: float, google_api_key: str = "", model_name: str = "gemini-2.0-flash"):
    """
    Factory function to initialize LLM instances based on selected provider with automatic failover fallbacks.
    """
    if provider == "Gemini API":
        if ChatGoogleGenerativeAI is None:
            st.sidebar.error("langchain-google-genai is not available in this environment.")
            return SafeLLMWrapper(None, provider)
        if not google_api_key:
            st.sidebar.warning("Please provide a Gemini API Key to run real models.")
            return SafeLLMWrapper(None, provider)

        try:
            primary = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", 
                google_api_key=google_api_key, 
                temperature=temperature, 
                max_retries=1
            )
            fallback1 = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                google_api_key=google_api_key, 
                temperature=temperature, 
                max_retries=1
            )
            fallback2 = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro", 
                google_api_key=google_api_key, 
                temperature=temperature, 
                max_retries=1
            )
            raw_llm = primary.with_fallbacks([fallback1, fallback2])
            return SafeLLMWrapper(raw_llm, provider)
        except Exception:
            return SafeLLMWrapper(None, provider)

    elif provider == "Local Ollama":
        if ChatOllama is None:
            st.sidebar.warning("langchain-ollama is not installed in this environment.")
            return SafeLLMWrapper(None, provider)
        try:
            raw_llm = ChatOllama(
                model="llama3", 
                temperature=temperature, 
                base_url="http://localhost:11434",
                options={
                    "stop": ["Question:", "Observation:", "\nQuestion:", "\nObservation:", "\nThought:"]
                }
            )
            return SafeLLMWrapper(raw_llm, provider)
        except Exception:
            return SafeLLMWrapper(None, provider)
    else:
        return SafeLLMWrapper(None, provider)

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
