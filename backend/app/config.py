import os
from dotenv import load_dotenv

load_dotenv()

# Configuration constants
PERSIST_DIR = "/app/chroma_db/data"
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/compound-mini")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
