import streamlit as st
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from core.vector_store import get_vector_store, index_documents, inspect_vector_store
from core.llm_factory import generate_mock_stream

DEFAULT_DEMO_TEXT = (
    "Chroma DB is an AI-native open-source vector database designed for building LLM applications.\n\n"
    "Retrieval-Augmented Generation (RAG) is a technique that grants an LLM access to external data to answer questions accurately without fine-tuning."
)

def render_tab_rag(get_llm_fn):
    st.markdown('<div class="tab-header">RAG Studio & Vector DB</div>', unsafe_allow_html=True)
    st.caption("Learn & experiment with Document Chunking, Vector Embeddings, Chroma DB Storage, and Context Retrieval.")
    
    # Session state initialization
    if "rag_raw_text" not in st.session_state:
        st.session_state.rag_raw_text = DEFAULT_DEMO_TEXT
    if "is_custom_doc" not in st.session_state:
        st.session_state.is_custom_doc = False

    col1, col2 = st.columns([6, 6])
    
    # ---------------------------------------------------------
    # LEFT COLUMN: Ingestion, Chunking & DB Inspection
    # ---------------------------------------------------------
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📌 Step 1: Document Source & Selection")
        
        # Document source selector
        doc_source = st.radio(
            "Select Document Source:",
            ["Sample Demo Text (Default)", "Upload Custom File (PDF / TXT)"],
            horizontal=True
        )
        
        if doc_source == "Upload Custom File (PDF / TXT)":
            uploaded_file = st.file_uploader("Upload Text or PDF Document", type=["txt", "pdf"])
            if uploaded_file:
                if uploaded_file.name.endswith(".pdf"):
                    try:
                        pdf_reader = pypdf.PdfReader(uploaded_file)
                        extracted = ""
                        for page in pdf_reader.pages:
                            extracted += page.extract_text() or ""
                        st.session_state.rag_raw_text = extracted
                        st.session_state.is_custom_doc = True
                        st.success(f"✅ Parsed PDF '{uploaded_file.name}' ({len(pdf_reader.pages)} pages) successfully!")
                    except Exception as e:
                        st.error(f"PDF parsing error: {e}")
                else:
                    st.session_state.rag_raw_text = uploaded_file.read().decode("utf-8")
                    st.session_state.is_custom_doc = True
                    st.success(f"✅ Parsed Text File '{uploaded_file.name}' successfully!")
            else:
                st.info("👆 Please upload a PDF or TXT file above.")
        else:
            st.session_state.rag_raw_text = DEFAULT_DEMO_TEXT
            st.session_state.is_custom_doc = False
            st.info("ℹ️ Using Sample Demo Text. Switch option above to upload your own file.")

        st.markdown("---")
        st.markdown("### ✂️ Step 2: Chunk Splitter Strategy")
        st.caption("Splits long text into smaller overlapping chunks so LLMs can process relevant sections.")
        
        strategy = st.radio("Chunk Splitter Algorithm", ["Recursive Character", "Character Splitter"], horizontal=True)
        
        c1, c2 = st.columns(2)
        with c1:
            chunk_size = st.slider("Chunk Size (characters)", 100, 1000, 200, 50)
        with c2:
            chunk_overlap = st.slider("Chunk Overlap (characters)", 10, 200, 40, 10)
        
        # Create documents chunks
        if strategy == "Recursive Character":
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        else:
            splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="")
            
        chunks = splitter.create_documents([st.session_state.rag_raw_text])
        
        st.write(f"#### 🔍 Splitter Preview ({len(chunks)} chunks created)")
        html_chunks = []
        for i, doc in enumerate(chunks):
            bg_color = "rgba(16, 185, 129, 0.15)" if i % 2 == 0 else "rgba(6, 182, 212, 0.1)"
            border_color = "rgba(16, 185, 129, 0.3)" if i % 2 == 0 else "rgba(6, 182, 212, 0.2)"
            html_chunks.append(
                f'<div style="background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; font-size: 12px; color: #e5e7eb;">'
                f'<span style="font-weight: 700; color: #10b981; font-size: 10px;">Chunk #{i+1} ({len(doc.page_content)} chars)</span><br>{doc.page_content}'
                f'</div>'
            )
        st.markdown('<div style="max-height: 200px; overflow-y: auto; background: #050508; padding: 8px; border-radius: 8px;">' + "".join(html_chunks) + '</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💾 Step 3: Vector Store Ingestion")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📥 Index Chunks in Vector Store", use_container_width=True):
                with st.spinner("Embedding & Indexing in Chroma DB..."):
                    try:
                        count = index_documents(chunks)
                        st.success(f"Indexed {count} chunks into Chroma DB!")
                    except Exception as e:
                        st.error(f"Indexing failed: {str(e)}")
        with btn_col2:
            if st.button("🗑️ Clear Vector Database", use_container_width=True):
                try:
                    db = get_vector_store()
                    existing = db.get()
                    if existing and "ids" in existing and existing["ids"]:
                        db.delete(ids=existing["ids"])
                    st.warning("Cleared all stored vectors from Chroma DB.")
                except Exception as e:
                    st.error(f"Clear failed: {e}")
                    
        with st.expander("🔍 Inspect Chroma DB (Stored SQLite Rows)", expanded=False):
            try:
                data = inspect_vector_store()
                if not data or not data["ids"]:
                    st.info("Chroma DB is currently empty. Click 'Index Chunks' to store vectors.")
                else:
                    st.markdown(f"Total Stored Document Vectors: **{len(data['ids'])}**")
                    for i in range(len(data["ids"])):
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; color: #10b981; margin-bottom: 4px;">
                                <span>Vector Row ID: {data['ids'][i]}</span>
                            </div>
                            <div style="font-family: monospace; font-size: 11px; color: #d1d5db;">{data['documents'][i]}</div>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to read Chroma DB: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RIGHT COLUMN: Similarity Search & Context QA Sandbox
    # ---------------------------------------------------------
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔎 Step 4: Similarity Search & RAG Chat")
        st.caption("Search stored vector embeddings and inject retrieved context into the LLM system prompt.")
        
        search_query = st.text_input("Search Query", "What is Chroma DB?")
        retrieval_type = st.radio(
            "Retrieval Index Algorithm", 
            ["Dense (Semantic Vector Search)", "Sparse (Word-Overlap TF-IDF)"], 
            horizontal=True
        )
        
        retrieved_docs = []
        if search_query:
            if retrieval_type == "Dense (Semantic Vector Search)":
                try:
                    db = get_vector_store()
                    results = db.similarity_search_with_relevance_scores(search_query, k=2)
                    for doc, score in results:
                        retrieved_docs.append({"content": doc.page_content, "score": score})
                except Exception:
                    retrieved_docs = []
            else:
                query_words = set(search_query.lower().split())
                results = []
                for doc in chunks:
                    words = doc.page_content.lower().split()
                    intersection = query_words.intersection(words)
                    score = len(intersection) / max(len(query_words), 1)
                    results.append({"content": doc.page_content, "score": score})
                results.sort(key=lambda x: x["score"], reverse=True)
                retrieved_docs = results[:2]
                
        st.write("#### 🎯 Top Search Matches")
        if not retrieved_docs:
            st.info("No indexed documents found. Please click 'Index Chunks in Vector Store' first.")
        else:
            for i, match in enumerate(retrieved_docs):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; color: #9ca3af; margin-bottom: 5px;">
                        <span>Rank #{i+1} Match</span>
                        <span style="color: #10b981;">Similarity Score: {match['score']:.4f}</span>
                    </div>
                    <div style="font-family: monospace; font-size: 12px; color: #f3f4f6;">{match['content']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.write("#### 💬 Context-Injected RAG Query Console")
        rag_input = st.text_input("Question for RAG Pipeline", "Tell me about Chroma DB.")
        
        if st.button("🚀 Run RAG Query", use_container_width=True):
            context_str = "\n\n".join([item["content"] for item in retrieved_docs]) if retrieved_docs else "No context found."
            system_instruction = "Use ONLY the provided context to answer the query accurately without making assumptions."
            compiled_prompt = (
                f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
                f"--- CONTEXT START ---\n{context_str}\n--- CONTEXT END ---\n\n"
                f"User Question: {rag_input}\n"
                f"Detailed Answer:"
            )
            
            with st.expander("🔍 Inspect Injected System Prompt & Context", expanded=True):
                st.code(compiled_prompt, language="markdown")
                
            st.write("#### 🤖 LLM Answer Response")
            response_box = st.empty()
            full_response = ""
            llm = get_llm_fn()
            
            if llm is None:
                for word in generate_mock_stream(rag_input):
                    full_response += word
                    response_box.markdown(full_response + "▌")
                response_box.markdown(full_response)
            else:
                try:
                    messages = [
                        SystemMessage(content=system_instruction),
                        HumanMessage(content=f"Context:\n{context_str}\n\nQuestion: {rag_input}")
                    ]
                    for chunk in llm.stream(messages):
                        full_response += chunk.content
                        response_box.markdown(full_response + "▌")
                    response_box.markdown(full_response)
                except Exception as e:
                    st.error(f"RAG query failed: {str(e)}")
                    
        st.markdown('</div>', unsafe_allow_html=True)
