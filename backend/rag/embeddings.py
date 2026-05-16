"""
embeddings.py — Text embedding generation using sentence-transformers.
Uses a local model (no API key needed for embeddings).
"""

from sentence_transformers import SentenceTransformer
from typing import List
from config import get_settings
import numpy as np

settings = get_settings()

# Load model once at module level (avoids repeated downloads)
_model: SentenceTransformer = None


def get_embedding_model() -> SentenceTransformer:
    """Lazy-load and cache the embedding model."""
    global _model
    if _model is None:
        print(f"[RAG] Loading embedding model: {settings.embedding_model}")
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts.

    Returns:
        numpy array of shape (len(texts), embedding_dim)
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return embeddings


def embed_query(query: str) -> np.ndarray:
    """
    Generate embedding for a single query string.

    Returns:
        1D numpy array
    """
    model = get_embedding_model()
    embedding = model.encode([query], normalize_embeddings=True)[0]
    return embedding
