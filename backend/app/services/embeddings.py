from langchain_community.embeddings import OllamaEmbeddings
from app.config import EMBEDDING_MODEL

# Singleton instance of embeddings for the application
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
