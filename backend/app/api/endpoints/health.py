from fastapi import APIRouter
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    postgres: str
    qdrant: str

@router.get("", response_model=HealthResponse)
def health_check():
    db_status = "ok"
    qdrant_status = "ok"
    
    # Check Postgres
    try:
        import psycopg2
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.close()
    except Exception as e:
        db_status = "unreachable"

    # Check Qdrant
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        client.get_collections()
    except Exception as e:
        qdrant_status = "unreachable"

    overall_status = "ok" if db_status == "ok" and qdrant_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "message": "Backend status report",
        "postgres": db_status,
        "qdrant": qdrant_status
    }

