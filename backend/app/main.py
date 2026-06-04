from fastapi import FastAPI
from app.routes import ingest, query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG API")

# Include routers
app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the RAG API"
    }
