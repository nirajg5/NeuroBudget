"""
CRUD Operations for Chat History
"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import ChatHistory

def create_chat(
    db: Session,
    chat: ChatHistory
) -> ChatHistory:

    db.add(chat)

    db.commit()

    db.refresh(chat)

    return chat

def bulk_create_chats(
    db: Session,
    chats: List[ChatHistory]
):

    db.bulk_save_objects(chats)

    db.commit()

def get_chat_by_id(
    db: Session,
    chat_id: int
) -> Optional[ChatHistory]:

    return (
        db.query(ChatHistory)
        .filter(
            ChatHistory.chat_id == chat_id
        )
        .first()
    )

def get_chat_history(
    db: Session,
    session_id: str
):

    return (
        db.query(ChatHistory)
        .filter(
            ChatHistory.session_id == session_id
        )
        .order_by(
            ChatHistory.created_at.asc()
        )
        .all()
    )

def get_latest_chat(
    db: Session,
    session_id: str
):

    return (
        db.query(ChatHistory)
        .filter(
            ChatHistory.session_id == session_id
        )
        .order_by(
            ChatHistory.created_at.desc()
        )
        .first()
    )

def update_chat(
    db: Session,
    chat_id: int,
    **kwargs
):

    chat = get_chat_by_id(
        db,
        chat_id
    )

    if chat is None:

        return None

    for key, value in kwargs.items():

        if hasattr(chat, key):

            setattr(chat, key, value)

    db.commit()

    db.refresh(chat)

    return chat

def delete_chat(
    db: Session,
    chat_id: int
):

    chat = get_chat_by_id(
        db,
        chat_id
    )

    if chat is None:

        return False

    db.delete(chat)

    db.commit()

    return True

def delete_chat(
    db: Session,
    chat_id: int
):

    chat = get_chat_by_id(
        db,
        chat_id
    )

    if chat is None:

        return False

    db.delete(chat)

    db.commit()

    return True


def delete_all_chats(
    db: Session
):

    db.query(ChatHistory).delete()

    db.commit()

def delete_all_chats(
    db: Session
):

    db.query(ChatHistory).delete()

    db.commit()

def get_session_count(
    db: Session
):

    return (
        db.query(
            func.count(
                func.distinct(
                    ChatHistory.session_id
                )
            )
        )
        .scalar()
    )

def get_recent_chats(
    db: Session,
    limit: int = 20
):

    return (
        db.query(ChatHistory)
        .order_by(
            ChatHistory.created_at.desc()
        )
        .limit(limit)
        .all()
    )

def search_messages(
    db: Session,
    keyword: str
):

    return (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_message.ilike(f"%{keyword}%")
        )
        .all()
    )

def get_latest_ai_response(
    db: Session,
    session_id: str
):

    chat = get_latest_chat(
        db,
        session_id
    )

    if chat is None:

        return None

    return chat.ai_response

def delete_session(
    db: Session,
    session_id: str
):
    """
    Delete all chats for a session.
    """

    deleted = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.session_id == session_id
        )
        .delete()
    )

    db.commit()

    return deleted