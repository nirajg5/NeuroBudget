"""
retriever.py — High-level RAG retrieval interface.
Wraps vectorstore search with context formatting for LLM prompts.
"""

from typing import List, Dict, Optional
from rag.vectorstore import search_similar_transactions


def retrieve_relevant_transactions(
    query: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Retrieve transactions most relevant to the user's query.
    Used to inject context into LLM prompts.
    """
    return search_similar_transactions(query, top_k=top_k)


def format_transactions_as_context(transactions: List[Dict]) -> str:
    """
    Format retrieved transactions into a readable string for LLM context.

    Example output:
        Transaction 1: 2024-01-05 | Swiggy Order | ₹350 | Food
        Transaction 2: 2024-01-07 | Uber Ride | ₹180 | Transport
    """
    if not transactions:
        return "No relevant transactions found."

    lines = []
    for i, t in enumerate(transactions, 1):
        line = (
            f"Transaction {i}: "
            f"{t.get('date','N/A')} | "
            f"{t.get('description','N/A')} | "
            f"₹{t.get('amount', 0):,.2f} | "
            f"{t.get('category','Other')}"
        )
        lines.append(line)

    return "\n".join(lines)


def build_rag_context(query: str, top_k: int = 5) -> str:
    """
    One-shot helper: retrieve + format context string.
    Pass this into LLM prompts to ground responses in real data.
    """
    relevant = retrieve_relevant_transactions(query, top_k=top_k)
    return format_transactions_as_context(relevant)
