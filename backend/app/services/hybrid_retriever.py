import os
import pickle
from langchain.retrievers import EnsembleRetriever

class HybridRetriever:
    def __init__(self, qdrant_retriever, bm25_path="/app/data/bm25_index.pkl"):
        """
        Builds a LangChain EnsembleRetriever merging Semantic Search and Keyword Search.
        By default, we weight the dense vectors (semantic) at 70% and sparse (keyword) at 30%.
        """
        self.qdrant_retriever = qdrant_retriever
        self.bm25_path = bm25_path
        self.bm25_retriever = self._load_bm25()
        
        if self.bm25_retriever:
            # We must set k limits equal if we want reciprocal rank fusion to work cleanly
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=[self.bm25_retriever, self.qdrant_retriever],
                weights=[0.3, 0.7] 
            )
        else:
            print("[Warning] BM25 index not found. Falling back to dense vector search only.")
            self.ensemble_retriever = self.qdrant_retriever

    def _load_bm25(self):
        if os.path.exists(self.bm25_path):
            with open(self.bm25_path, "rb") as f:
                return pickle.load(f)
        return None

    def get_relevant_documents(self, query: str):
        # We retrieve a larger net of top 10 documents so the Reranker can sort them
        return self.ensemble_retriever.invoke(query)
