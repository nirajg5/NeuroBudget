"""
vectorstore.py — FAISS vector store management.
Stores transaction text embeddings for semantic retrieval.
"""

import faiss
import numpy as np
import json
import os
from typing import List, Dict, Optional
from rag.embeddings import embed_texts, embed_query
from config import get_settings

settings = get_settings()

# Paths for persistence
INDEX_PATH = os.path.join(settings.vectorstore_dir, "transactions.index")
METADATA_PATH = os.path.join(settings.vectorstore_dir, "metadata.json")

# In-memory state
_index: Optional[faiss.IndexFlatIP] = None   # Inner product (cosine for normalized vecs)
_metadata: List[Dict] = []                   # Parallel list of transaction dicts


def _load_or_create_index(dim: int) -> faiss.IndexFlatIP:
    """Load existing FAISS index from disk or create a new one."""
    global _index, _metadata

    if os.path.exists(INDEX_PATH):
        try:
            _index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, "r") as f:
                _metadata = json.load(f)
            print(f"[VectorStore] Loaded index with {_index.ntotal} vectors")
            return _index
        except Exception as e:
            print(f"[VectorStore] Failed to load index: {e}. Creating new one.")

    _index = faiss.IndexFlatIP(dim)
    _metadata = []
    return _index


def _save_index():
    """Persist FAISS index and metadata to disk."""
    if _index is not None:
        faiss.write_index(_index, INDEX_PATH)
        with open(METADATA_PATH, "w") as f:
            json.dump(_metadata, f, indent=2, default=str)


def add_transactions(transactions: List[Dict]):
    """
    Embed and add transactions to the FAISS vector store.
    Text format: "date: YYYY-MM-DD | description: XYZ | amount: 500 | category: Food"
    """
    global _index, _metadata

    if not transactions:
        return

    # Build text representations for embedding
    texts = [
        f"date: {t.get('date','')} | description: {t.get('description','')} | "
        f"amount: {t.get('amount',0)} | category: {t.get('category','Other')}"
        for t in transactions
    ]

    embeddings = embed_texts(texts)
    dim = embeddings.shape[1]

    if _index is None:
        _load_or_create_index(dim)

    # Add to FAISS
    _index.add(embeddings.astype(np.float32))
    _metadata.extend(transactions)

    _save_index()
    print(f"[VectorStore] Added {len(transactions)} transactions. Total: {_index.ntotal}")


def search_similar_transactions(query: str, top_k: int = 5) -> List[Dict]:
    """
    Find the most semantically similar transactions to a query.

    Example:
        query = "food spending last month"
        Returns top 5 matching food transactions.
    """
    global _index, _metadata

    if _index is None or _index.ntotal == 0:
        return []

    query_vec = embed_query(query).astype(np.float32).reshape(1, -1)
    top_k = min(top_k, _index.ntotal)

    distances, indices = _index.search(query_vec, top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx >= 0 and idx < len(_metadata):
            result = dict(_metadata[idx])
            result["similarity_score"] = round(float(dist), 4)
            results.append(result)

    return results


def get_total_vectors() -> int:
    """Return number of vectors currently in store."""
    if _index is None:
        return 0
    return _index.ntotal


def clear_vectorstore():
    """Reset the vector store (useful for testing)."""
    global _index, _metadata
    _index = None
    _metadata = []
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(METADATA_PATH):
        os.remove(METADATA_PATH)
