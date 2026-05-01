# 🛡️ AI AWS IAM Sentinel

AI AWS IAM Sentinel is an enterprise-grade GenAI assistant designed to provide precise, context-aware answers strictly from the **AWS IAM User Guide**. It leverages a robust RAG (Retrieval-Augmented Generation) pipeline to ensure high accuracy and security-focused responses.

---

## 🚀 Features

- **Context-Aware Q&A**: Answers questions based solely on the official AWS IAM User Guide.
- **Automated Data Pipeline**: Automatically parses, chunks, and indexes the AWS IAM PDF guide into a vector database on startup.
- **Hybrid Search**: Combines semantic search (vector) with BM25 keyword matching for optimal retrieval.
- **Enterprise-Ready**: Built with FastAPI and Next.js, optimized for production deployments.
- **Background Indexing**: Performs heavy indexing tasks in a background thread to keep the service responsive.

---

## 🏗️ Architecture

### **Tech Stack**
- **Frontend**: Next.js (TypeScript, Tailwind CSS, Lucide React)
- **Backend**: FastAPI (Python 3.11)
- **Vector Database**: Qdrant Cloud
- **LLM**: OpenAI GPT-4o (via LangChain)
- **Embeddings**: `BAAI/bge-small-en-v1.5` (running locally on CPU)
- **Orchestration**: LangChain & LangGraph

### **System Flow**
1. **Ingestion**: On startup, the system reads `iam-ug.pdf`, chunks it using recursive character splitting, and uploads embeddings to Qdrant.
2. **Retrieval**: When a user asks a question, the system retrieves relevant chunks using the BGE embedding model.
3. **Generation**: The context is passed to GPT-4o with a strict "answer only from context" prompt.

---

## 🛠️ Local Setup

### **Prerequisites**
- Docker & Docker Compose
- OpenAI API Key
- Qdrant Cloud Account (Free tier works)

### **Environment Setup**
1. Clone the repository.
2. Create a `.env` file in the root directory (use `.env.example` as a template):
   ```bash
   cp .env.example .env
   ```
3. Fill in your credentials:
   - `OPENAI_API_KEY`: Your OpenAI key.
   - `QDRANT_URL` & `QDRANT_API_KEY`: Your Qdrant Cloud instance details.
   - `DATABASE_URL`: Your database connection string (if using persistence).

### **Running with Docker**
The easiest way to run the entire system:
```bash
docker-compose up --build
```
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 Deployment

### **Render / Production**
This project is optimized for deployment on **Render**.
- The `Dockerfile` includes pre-caching of embedding models to prevent startup timeouts.
- Use `docker-compose.prod.yml` for production-grade configurations.

### **Hugging Face Spaces**
The project includes support for Hugging Face Spaces:
- See `backend/Dockerfile.hf` for the specific HF configuration.
- The system is designed to run efficiently on CPU-only environments.

---

## 📂 Project Structure

```text
├── backend/            # FastAPI Application
│   ├── app/            # Core logic, APIs, and services
│   ├── data/           # PDF source files
│   └── scripts/        # Utility scripts
├── frontend/           # Next.js UI
│   ├── src/            # Components and app logic
│   └── public/         # Static assets
├── data/               # Persistent data volume
└── docker-compose.yml  # Orchestration
```

---

## 📄 License

This project is for educational and enterprise demonstration purposes. Data source: [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html).
