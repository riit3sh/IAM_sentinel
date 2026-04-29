from fastapi import FastAPI, BackgroundTasks
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

@app.get("/")
def root():
    return {"message": "Welcome to AI AWS IAM Sentinel API"}

def run_indexing():
    """Runs PDF indexing inline (same process, no extra memory)."""
    import gc
    from langchain_core.documents import Document
    from app.services.document_parser import DocumentParser
    from app.services.chunker import DocumentChunker
    from app.services.qdrant_store import get_vector_store

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
    
    # Free parser memory before loading vectors
    del pages, chunks, parser, chunker
    gc.collect()
    
    print("\n🚀 [2/2] Uploading Vectors to Qdrant Cloud...")
    vector_store = get_vector_store()
    
    # Small batches to stay under 512MB RAM
    batch_size = 100
    total_batches = (len(documents) // batch_size) + 1
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        print(f"   -> Batch {i//batch_size + 1}/{total_batches}...")
        vector_store.add_documents(batch)
        # Free batch memory immediately
        del batch
        gc.collect()
        
    print("\n🎉 Indexing completely finished!")

@app.get("/api/v1/trigger-index")
def trigger_index(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_indexing)
    return {"message": "Indexing triggered in background! Watch Render logs for progress."}

