from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "NeuroBudget"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_HOST: str

    POSTGRES_PORT: int

    POSTGRES_DB: str

    OPENROUTER_API_KEY: str

    OPENROUTER_MODEL: str

    PINECONE_API_KEY: str

    PINECONE_INDEX: str

    PINECONE_REGION: str

    class Config:
        env_file = ".env"


settings = Settings()