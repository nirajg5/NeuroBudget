"""
Database Initialization

Creates, Drops and Resets Database Tables
"""

from database.db import BaseModel, engine

# Import all models so SQLAlchemy registers them
from database import models

from core.logger import logger


def create_tables():
    """
    Create all database tables.
    """
    try:
        BaseModel.metadata.create_all(bind=engine)
        logger.success("✅ Database tables created successfully.")

    except Exception:
        logger.exception("❌ Failed to create database tables.")
        raise


def drop_tables():
    """
    Drop all database tables.
    WARNING: This deletes all data.
    """
    try:
        BaseModel.metadata.drop_all(bind=engine)
        logger.warning("⚠️ All database tables dropped.")

    except Exception:
        logger.exception("❌ Failed to drop database tables.")
        raise


def reset_database():
    """
    Drop all tables and recreate them.
    """
    logger.info("Resetting Database...")

    drop_tables()

    create_tables()

    logger.success("🎉 Database reset completed successfully.")


if __name__ == "__main__":

    
    create_tables()