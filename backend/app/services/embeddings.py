from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL

# Singleton instance of embeddings for the application
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)