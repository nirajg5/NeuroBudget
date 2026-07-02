"""
Application Configuration

Loads all environment variables from .env
"""

from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    # ======================================================
    # FastAPI
    # ======================================================

    APP_NAME: str = "NeuroBudget"

    APP_VERSION: str = "1.0.0"

    APP_DESCRIPTION: str = "AI Financial Copilot"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ======================================================
    # PostgreSQL
    # ======================================================

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_HOST: str

    POSTGRES_PORT: int

    POSTGRES_DB: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # ======================================================
    # OpenRouter
    # ======================================================

    OPENROUTER_API_KEY: str

    OPENROUTER_MODEL: str

    # ======================================================
    # Pinecone
    # ======================================================

    PINECONE_API_KEY: str

    PINECONE_INDEX: str

    PINECONE_REGION: str

    # ======================================================
    # Embedding Model
    # ======================================================

    EMBEDDING_MODEL: str = Field(
        default="BAAI/bge-small-en-v1.5"
    )

    # ======================================================
    # LangGraph
    # ======================================================

    MAX_CHAT_HISTORY: int = 10

    # ======================================================
    # Upload
    # ======================================================

    MAX_UPLOAD_SIZE_MB: int = 20


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()