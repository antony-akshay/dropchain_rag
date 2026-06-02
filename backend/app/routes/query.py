from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest, QueryResponse
from app.services.rag_service import answer_question

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = answer_question(request.query)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
