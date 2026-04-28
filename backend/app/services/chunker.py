import hashlib
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            # We prefer splitting on double newlines to keep paragraphs together
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_documents(self, page_documents: List[Dict]) -> List[Dict]:
        """
        Splits page texts into granular semantic chunks while preserving and enhancing metadata.
        """
        chunks = []
        for doc in page_documents:
            text = doc["text"]
            metadata = doc["metadata"]
            
            # Split page text into smaller LangChain chunks
            text_chunks = self.splitter.split_text(text)
            
            for i, chunk_text in enumerate(text_chunks):
                # Generate a unique deterministic hash for the chunk id
                unique_str = f"{metadata['source_file']}_{metadata['page_number']}_{i}"
                chunk_id = hashlib.sha256(unique_str.encode()).hexdigest()[:12]
                
                chunk_metadata = {
                    **metadata,
                    "chunk_id": chunk_id,
                }
                
                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })
                
        return chunks
