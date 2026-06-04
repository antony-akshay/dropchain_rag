from sentence_transformers import SentenceTransformer
import os

model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
print(f"Downloading model: {model_name}")
SentenceTransformer(model_name)
print("Model download complete")
