import os
import shutil
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import PERSIST_DIR
from app.services.embeddings import embeddings

def delete_vectorstore() -> None:
    """Deletes the contents of the existing Chroma DB persist directory."""
    if os.path.exists(PERSIST_DIR):
        for item in os.listdir(PERSIST_DIR):
            item_path = os.path.join(PERSIST_DIR, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"Failed to delete {item_path}: {e}")

def create_vectorstore(documents: List[Document]) -> Chroma:
    """Creates a fresh vectorstore from documents. Deletes older ones if any."""
    # Filter tiny noise chunks
    chunks = [c for c in documents if len(c.page_content.strip()) > 30]

    delete_vectorstore()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    return vectorstore

def load_vectorstore() -> Chroma:
    """Loads an existing vectorstore from the persist directory."""
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
