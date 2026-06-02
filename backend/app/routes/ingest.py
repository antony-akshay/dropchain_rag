import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import UPLOAD_DIR
from app.services.rag_service import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        # Save file temporarily
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks_count = ingest_document(file_location)
        
        return {
            "message": "Document ingested successfully",
            "chunks": chunks_count
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if 'file_location' in locals() and os.path.exists(file_location):
            os.remove(file_location)
