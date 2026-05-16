"""
chat_memory.py — Manages per-session conversation history stored in SQLite.
Used to give the AI context about past messages in the same session.
"""

from sqlalchemy.orm import Session
from database.db import ChatMessageModel
from typing import List, Dict


def save_message(db: Session, session_id: str, role: str, content: str):
    """Persist a chat message to the database."""
    msg = ChatMessageModel(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()


def get_history(db: Session, session_id: str, limit: int = 10) -> List[Dict]:
    """
    Retrieve the last `limit` messages for a session.
    Returns list of {"role": ..., "content": ...} dicts — ready for OpenAI format.
    """
    messages = (
        db.query(ChatMessageModel)
        .filter(ChatMessageModel.session_id == session_id)
        .order_by(ChatMessageModel.created_at.desc())
        .limit(limit)
        .all()
    )
    # Reverse to get chronological order
    return [{"role": m.role, "content": m.content} for m in reversed(messages)]


def clear_history(db: Session, session_id: str):
    """Clear all messages for a session (useful for testing)."""
    db.query(ChatMessageModel).filter(
        ChatMessageModel.session_id == session_id
    ).delete()
    db.commit()
