import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import health, chat

# API Routers
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["Health"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["Chat Inference"])

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"message": "Welcome to AI AWS IAM Sentinel API"}

def run_indexing_on_startup():
    """Runs PDF indexing if Qdrant Cloud is empty (runs in separate thread)."""
    try:
        from qdrant_client import QdrantClient
        from langchain_core.documents import Document
        from app.services.document_parser import DocumentParser
        from app.services.chunker import DocumentChunker
        from app.services.qdrant_store import get_vector_store
        
        # Connect to Qdrant and check if already populated
        client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        collection_name = "aws_iam_guide_v3"
        
        try:
            info = client.get_collection(collection_name)
            if info.points_count > 0:
                print(f"ℹ️ Qdrant already contains {info.points_count} points. Skipping automatic indexing.")
                return
        except Exception:
            # Collection might not exist yet, proceed to create and index
            print("ℹ️ Collection not found or empty. Proceeding with indexing...")
            pass

        pdf_path = "/app/data/iam-ug.pdf"
        
        print("\n🚀 [1/2] Parsing & Chunking Data...")
        parser = DocumentParser(pdf_path)
        pages = parser.extract_text()
        chunker = DocumentChunker()
        chunks = chunker.chunk_documents(pages)
        print(f"✅ Generated {len(chunks)} chunks.")
        
        documents = [
            Document(page_content=c['text'], metadata=c['metadata'])
            for c in chunks
        ]
        
        print("\n🚀 [2/2] Uploading Vectors to Qdrant Cloud...")
        vector_store = get_vector_store()
        
        # With 16GB RAM on HF Spaces, we can comfortably use larger batches
        batch_size = 500
        total_batches = (len(documents) // batch_size) + 1
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            print(f"   -> Batch {i//batch_size + 1}/{total_batches}...")
            vector_store.add_documents(batch)
            
        print("\n🎉 Automatic Indexing completely finished!")
    except Exception as e:
        print(f"❌ Startup Indexing failed: {e}")

def warm_up_model():
    """Warms up embedding model weights into memory on startup."""
    try:
        from app.services.embeddings import get_embeddings
        print("⚡ Warming up embedding model weights into memory...")
        embed_model = get_embeddings()
        embed_model.embed_query("warmup query text")
        print("⚡ Embedding model successfully warmed up in memory.")
    except Exception as e:
        print(f"⚠️ Warmup failed: {e}")

@app.on_event("startup")
def startup_event():
    # Run the indexing automatically in the background on startup
    threading.Thread(target=run_indexing_on_startup, daemon=True).start()
    # Pre-cache and warm up heavy model weights
    threading.Thread(target=warm_up_model, daemon=True).start()


