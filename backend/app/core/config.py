from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI AWS IAM Sentinel"
    API_V1_STR: str = "/api/v1"
    
    # Postgres
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "iam_sentinel"
    DATABASE_URL: str = "postgresql://admin:admin@postgres:5432/iam_sentinel"

    # Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    
    # LLM
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
