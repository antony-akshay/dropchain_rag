import os
from dotenv import load_dotenv

load_dotenv()

# Configuration constants
PERSIST_DIR = os.getenv("PERSIST_DIR", "./chroma_db")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/compound-mini")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
