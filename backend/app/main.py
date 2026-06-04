from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ingest, query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the RAG API"
    }
