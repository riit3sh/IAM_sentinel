from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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

@app.get("/api/v1/trigger-index")
def trigger_index():
    import subprocess
    # Run the ingestion script in the background so it doesn't time out the HTTP request
    subprocess.Popen(["python", "scripts/index_data.py"])
    return {"message": "Indexing triggered in background! Check Render logs for progress."}
