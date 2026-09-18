import os
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

from langchain_community.vectorstores import Chroma
from config import CHROMA_DB_DIR
from core.embeddings import ZenithLocalEmbeddings

@st.cache_resource
def get_vector_store():
    """
    Initializes and caches the local Chroma DB instance using ZenithLocalEmbeddings.
    """
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=ZenithLocalEmbeddings(),
        collection_metadata={"hnsw:space": "cosine"}
    )

def index_documents(documents):
    """
    Clears existing vector entries and indexes new document chunks into Chroma DB.
    """
    db = get_vector_store()
    existing = db.get()
    if existing and "ids" in existing and existing["ids"]:
        db.delete(ids=existing["ids"])
    db.add_documents(documents)
    return len(documents)

def inspect_vector_store():
    """
    Returns stored documents and IDs from Chroma DB.
    """
    db = get_vector_store()
    return db.get()
