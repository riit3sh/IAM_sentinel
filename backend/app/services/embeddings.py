from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns the BAAI/bge-small-en-v1.5 sentence-transformers embedding model.
    Downloads the model weights locally upon first execution.
    """
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},  # Run on CPU for standard Docker setup
        encode_kwargs={'normalize_embeddings': True}
    )
