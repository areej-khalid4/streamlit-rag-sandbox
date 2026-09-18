import streamlit as st
from core.evaluator import calculate_grounding_metrics

def render_tab_eval():
    st.markdown('<div class="tab-header">Evaluation & Observability</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Local Grounding & RAG Metrics")
    st.caption("Evaluate output answers against matching context blocks using local overlap formulas.")
    
    col1, col2 = st.columns([6, 6])
    
    with col1:
        eval_context = st.text_area(
            "Retrieved Context Chunks", 
            "Chroma DB runs locally on SQLite files and stores text embeddings vector indexes."
        )
        eval_answer = st.text_area(
            "LLM Generated Answer", 
            "Chroma DB is a local database running on SQLite and storing vector indexes."
        )
        
    with col2:
        faithfulness, relevance = calculate_grounding_metrics(eval_context, eval_answer)
        
        st.write("#### Evaluation Indicators")
        st.metric("Faithfulness Score (No Hallucination)", f"{faithfulness:.2%}")
        st.progress(faithfulness)
        
        st.metric("Answer Relevance Score", f"{relevance:.2%}")
        st.progress(relevance)
        
        if faithfulness > 0.7:
            st.success("✅ Output grounded! No hallucination detected.")
        else:
            st.warning("⚠️ Low grounding score. Answer contains words not found in retrieved context.")
            
    st.markdown('</div>', unsafe_allow_html=True)
