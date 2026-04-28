from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI AWS IAM Sentinel"
    API_V1_STR: str = "/api/v1"
    
    # Postgres
    DATABASE_URL: str

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str
    
    # LLM
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
