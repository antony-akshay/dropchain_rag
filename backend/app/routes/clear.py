from fastapi import APIRouter, HTTPException
from app.services.vectorstore import delete_vectorstore

router = APIRouter()

@router.post("/clear")
async def clear():
    """Deletes the existing ChromaDB vectorstore."""
    try:
        delete_vectorstore()
        return {"message": "Vectorstore cleared successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
