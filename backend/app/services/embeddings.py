from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL
from typing import Optional

_embeddings: Optional[HuggingFaceEmbeddings] = None

def get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        print("Embedding model loaded.")
    return _embeddings

# Proxy object or just use get_embeddings() in services
# For langchain compatibility, we might need the object, but we'll use lazy loading in services.