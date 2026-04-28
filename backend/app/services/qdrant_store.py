import socket
import urllib.request
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from app.core.config import settings
from app.services.embeddings import get_embeddings

def get_qdrant_client():
    """Builds a raw Qdrant client."""
    return QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

def create_collection_if_not_exists(collection_name: str = "aws_iam_guide"):
    client = get_qdrant_client()
    try:
        client.get_collection(collection_name)
    except Exception:
        # If it doesn't exist, an exception is thrown. Create it.
        # BAAI/bge-small embeddings have 384 dimensions.
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def get_vector_store(collection_name: str = "aws_iam_guide"):
    """
    Returns the LangChain Qdrant vector store interface.
    """
    create_collection_if_not_exists(collection_name)
    client = get_qdrant_client()
    
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=get_embeddings()
    )
