from sentence_transformers import CrossEncoder

class DocumentReranker:
    def __init__(self, model_name="BAAI/bge-reranker-base"):
        """
        Initializes the CrossEncoder BGE Reranker.
        """
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list, top_k: int = 3):
        """
        Scores the top 10 retrieved chunks strictly against the query,
        returning only the highest quality top_k passages.
        """
        if not documents:
            return []
            
        # Build query-document pairs
        pairs = [[query, doc.page_content] for doc in documents]
        
        # Calculate raw semantic overlap scores using CrossEncoder architecture
        scores = self.model.predict(pairs)
        
        scored_docs = list(zip(documents, scores))
        sorted_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
        
        # Return only the documents ordered by best score
        return [doc for doc, score in sorted_docs[:top_k]]
