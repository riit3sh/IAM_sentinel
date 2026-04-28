from fastapi import APIRouter
from app.core.config import settings
import psycopg2
from qdrant_client import QdrantClient
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    postgres: str
    qdrant: str

@router.get("/", response_model=HealthResponse)
def health_check():
    db_status = "ok"
    qdrant_status = "ok"
    
    # Check Postgres
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.close()
    except Exception as e:
        db_status = f"unreachable"

    # Check Qdrant
    try:
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        client.get_collections()
    except Exception as e:
        qdrant_status = f"unreachable"

    overall_status = "ok" if db_status == "ok" and qdrant_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "message": "Backend status report",
        "postgres": db_status,
        "qdrant": qdrant_status
    }
