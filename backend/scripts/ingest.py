import os
import sys

# Add parent directory (/app or root) to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.document_parser import DocumentParser
from app.services.chunker import DocumentChunker

def test_ingestion():
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'iam-ug.pdf'))
    
    print(f"Reading from: {pdf_path}\n")
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    # 1. Parse Document
    print("Step 1: Parsing document with PyMuPDF...")
    parser = DocumentParser(file_path=pdf_path)
    pages = parser.extract_text()
    print(f"✅ Extracted {len(pages)} pages with text.\n")

    # 2. Chunk Document
    print("Step 2: Chunking document with RecursiveCharacterTextSplitter...")
    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=150)
    chunks = chunker.chunk_documents(pages)
    print(f"✅ Generated {len(chunks)} chunks.\n")

    # 3. Verify Output
    print("--- Verifying First 3 Chunks Output ---")
    for i in range(min(3, len(chunks))):
        print(f"\n[ Chunk {i+1} Output ]")
        print(f"Metadata : {chunks[i]['metadata']}")
        preview = chunks[i]['text'][:250].replace('\n', ' ')
        print(f"Text     : {preview}...")

if __name__ == "__main__":
    test_ingestion()
