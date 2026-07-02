"""
Database Configuration

Creates:

1. PostgreSQL Engine
2. Database Session
3. SQLAlchemy Base
4. FastAPI Dependency
"""

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from core.config import settings
from core.logger import logger


# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

# ==========================================================
# Base Class
# ==========================================================

BaseModel = declarative_base()

# ==========================================================
# FastAPI Dependency
# ==========================================================

def get_db():
    """
    Dependency for FastAPI.

    Example:
        db: Session = Depends(get_db)
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ==========================================================
# Database Connection Test
# ==========================================================

def test_connection():
    """
    Tests PostgreSQL connection.
    """

    db = SessionLocal()

    try:

        db.execute(text("SELECT 1"))

        logger.success("✅ PostgreSQL Connected Successfully")

    except Exception:

        logger.exception("❌ Failed to connect to PostgreSQL")

        raise

    finally:

        db.close()