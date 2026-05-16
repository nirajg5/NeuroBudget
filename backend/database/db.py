"""
db.py — SQLAlchemy SQLite setup.
Defines Transaction and ChatMessage tables with lightweight ORM models.
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from config import get_settings

settings = get_settings()

# SQLite engine — file-based, no server needed
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Required for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ─── ORM Models ───────────────────────────────────────────────────────────────

class TransactionModel(Base):
    """Stores parsed financial transactions."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="Other")
    source = Column(String, default="manual")      # Filename or "manual"
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessageModel(Base):
    """Stores conversation history per session."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)          # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─── DB Init & Dependency ─────────────────────────────────────────────────────

def init_db():
    """Create all tables. Call once at startup."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and closes it after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
