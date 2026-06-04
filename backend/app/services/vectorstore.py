import os
import chromadb
from chromadb.config import Settings
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import PERSIST_DIR
from app.services.embeddings import get_embeddings

# Singleton client
_client: Optional[chromadb.PersistentClient] = None

def get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        os.makedirs(PERSIST_DIR, exist_ok=True)
        _client = chromadb.PersistentClient(
            path=PERSIST_DIR,
            settings=Settings(allow_reset=True)
        )
    return _client

def delete_vectorstore() -> None:
    client = get_client()
    try:
        client.reset()
    except Exception as e:
        print(f"Reset error: {e}")

def create_vectorstore(documents: List[Document]) -> Chroma:
    chunks = [c for c in documents if len(c.page_content.strip()) > 30]
    delete_vectorstore()
    
    vectorstore = Chroma(
        client=get_client(),
        embedding_function=get_embeddings(),
        persist_directory=PERSIST_DIR
    )
    
    if chunks:
        vectorstore.add_documents(chunks)
    return vectorstore

def load_vectorstore() -> Chroma:
    return Chroma(
        client=get_client(),
        embedding_function=get_embeddings(),
        persist_directory=PERSIST_DIR
    )
