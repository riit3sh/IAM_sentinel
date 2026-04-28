import os
import sys

# Add root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.qdrant_store import get_vector_store
from app.services.hybrid_retriever import HybridRetriever
from app.services.reranker import DocumentReranker

def run_test_query():
    print("Loading services...")
    # Initialize basic components
    qdrant = get_vector_store()
    retriever = qdrant.as_retriever(search_kwargs={"k": 10})
    
    # Init Ensemble BM25 + Qdrant
    hybrid = HybridRetriever(qdrant_retriever=retriever)
    
    # Init Reranker
    reranker = DocumentReranker()
    
    query = "How to enforce MFA for the root account?"
    print(f"\nQUERY: {query}")
    print("-" * 50)
    
    # 1. Broad Retrieval
    print("Searching vector database and BM25...")
    hybrid_docs = hybrid.get_relevant_documents(query)
    
    print(f"Retrieved {len(hybrid_docs)} top results. Passing to Reranker...")
    
    # 2. Rerank
    final_docs = reranker.rerank(query, hybrid_docs, top_k=3)
    
    print("\n[ TOP 3 RERANKED CHUNKS ]\n")
    for i, doc in enumerate(final_docs):
        print(f"--- Chunk {i+1} ---")
        print(f"📄 Page    : {doc.metadata.get('page_number')}")
        print(f"📑 Section : {doc.metadata.get('section_title')}")
        print(f"🔗 Text    : {doc.page_content.strip()[:300]}...")
        print("-" * 50)

if __name__ == "__main__":
    run_test_query()
