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
    import subprocess, os, urllib.request
    
    # Ensure data directory exists
    os.makedirs("/app/data", exist_ok=True)
    pdf_path = "/app/data/iam-ug.pdf"
    
    # Download PDF from GitHub if not already present
    if not os.path.exists(pdf_path):
        print("[Index] Downloading iam-ug.pdf from GitHub...")
        pdf_url = "https://raw.githubusercontent.com/riit3sh/Render_IAM_sentinel/main/data/iam-ug.pdf"
        urllib.request.urlretrieve(pdf_url, pdf_path)
        print("[Index] Download complete.")
    
    # Ensure scripts directory exists and copy index script
    os.makedirs("/app/scripts", exist_ok=True)
    script_url = "https://raw.githubusercontent.com/riit3sh/Render_IAM_sentinel/main/scripts/index_data.py"
    urllib.request.urlretrieve(script_url, "/app/scripts/index_data.py")
    
    # Run the ingestion script in the background
    subprocess.Popen(["python", "scripts/index_data.py"])
    return {"message": "Indexing triggered in background! Check Render logs for progress."}
