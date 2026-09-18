import hashlib
import string
import numpy as np
from langchain_core.embeddings import Embeddings

class ZenithLocalEmbeddings(Embeddings):
    """
    Custom Feature Hashing Vectorizer Embedding Engine.
    Converts text into dense float numerical vectors of specified dimension
    without needing external cloud embedding APIs.
    """
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def _embed_text(self, text: str) -> list[float]:
        vector = np.zeros(self.dimensions)
        clean_text = text.lower().translate(str.maketrans("", "", string.punctuation))
        words = clean_text.split()
        if not words:
            return vector.tolist()
        for word in words:
            for i in range(5):  # 5 hash buckets per word for dense feature distribution
                h = hashlib.md5(f"{word}_{i}".encode('utf-8')).hexdigest()
                idx = int(h, 16) % self.dimensions
                val = -1.0 if int(h[0], 16) % 2 == 0 else 1.0
                vector[idx] += val
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)
