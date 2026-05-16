"""
config.py — Centralized app configuration using pydantic-settings.
Reads from .env file automatically.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # OpenRouter
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./neurobudget.db"

    # File Uploads
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10

    # Vector Store
    vectorstore_dir: str = "vectorstore"

    # Embedding model (local sentence-transformers)
    embedding_model: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — call this everywhere instead of re-reading env."""
    return Settings()


# Create required directories on import
settings = get_settings()
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.vectorstore_dir, exist_ok=True)
