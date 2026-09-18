import streamlit as st
import tiktoken
from langchain_core.messages import HumanMessage
from core.llm_factory import generate_mock_stream

def render_tab_playground(get_llm_fn):
    st.markdown('<div class="tab-header">LLM & Tokenizer Playground</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Visual BPE Tokenizer")
        st.caption("Enter text to see how BPE splits words into word-piece tokens.")
        
        token_input = st.text_area("Input Text", "FastAPI and LangChain are tools for AI engineering.", height=120)
        
        if token_input:
            try:
                encoding = tiktoken.get_encoding("cl100k_base")
                tokens = encoding.encode(token_input)
                
                st.markdown(f"**Total Tokens**: `{len(tokens)}` | **Length**: `{len(token_input)}` chars")
                
                html_spans = []
                colors = ["#4c1d95", "#831843", "#064e3b", "#0f766e", "#1e3a8a"]
                for i, token in enumerate(tokens):
                    word = encoding.decode([token])
                    color = colors[i % len(colors)]
                    html_spans.append(
                        f'<span style="background-color: {color}; color: #f3f4f6; padding: 2px 5px; margin: 3px; border-radius: 4px; display: inline-block; font-family: monospace; font-size: 13px;">{word}</span>'
                    )
                st.markdown('<div style="background: #050508; border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; max-height: 180px; overflow-y: auto;">' + "".join(html_spans) + '</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Tokenizer error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Interactive Completion Chat")
        
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
            
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_query = st.chat_input("Ask LLM anything...")
        if user_query:
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            
            llm = get_llm_fn()
            
            with st.chat_message("assistant"):
                response_box = st.empty()
                full_response = ""
                
                if llm is None:
                    for word in generate_mock_stream(user_query):
                        full_response += word
                        response_box.markdown(full_response + "▌")
                    response_box.markdown(full_response)
                else:
                    try:
                        messages = [HumanMessage(content=user_query)]
                        for chunk in llm.stream(messages):
                            full_response += chunk.content
                            response_box.markdown(full_response + "▌")
                        response_box.markdown(full_response)
                    except Exception as e:
                        st.error(f"Execution failed: {str(e)}")
                        
            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
        st.markdown('</div>', unsafe_allow_html=True)
