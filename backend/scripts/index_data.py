import os
import sys
import pickle
import time

# Add root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from app.services.document_parser import DocumentParser
from app.services.chunker import DocumentChunker
from app.services.qdrant_store import get_vector_store

def build_index():
    pdf_path = "/app/data/iam-ug.pdf"
    bm25_path = "/app/data/bm25_index.pkl"
    
    print("\n🚀 [1/3] Parsing & Chunking Data...")
    parser = DocumentParser(pdf_path)
    pages = parser.extract_text()
    chunker = DocumentChunker()
    chunks = chunker.chunk_documents(pages)
    print(f"✅ Generated {len(chunks)} chunks.")
    
    documents = [
        Document(page_content=c['text'], metadata=c['metadata'])
        for c in chunks
    ]
    
    print("\n🚀 [2/3] Building Local BM25 Sparse Index...")
    start_time = time.time()
    bm25_retriever = BM25Retriever.from_documents(documents)
    # We retrieve 10 items for hybrid fusion limit.
    bm25_retriever.k = 10 
    
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25_retriever, f)
    print(f"✅ Saved BM25 to {bm25_path} (Took {time.time()-start_time:.1f}s)")
        
    print("\n🚀 [3/3] Uploading Vectors to Qdrant (This will take a few minutes)...")
    vector_store = get_vector_store()
    
    # We will upload in batches to avoid RAM overflows in downloading BAAI embeds
    batch_size = 200
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        print(f"   -> Processing Batch {i//batch_size + 1} of {(len(documents)//batch_size)+1}...")
        vector_store.add_documents(batch)
        
    print("\n🎉 Indexing completely finished!")

if __name__ == "__main__":
    build_index()
