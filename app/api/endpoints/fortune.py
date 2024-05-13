# app/api/endpoints/fortune.py

from fastapi import APIRouter, HTTPException
from app.models.schemas import FortuneRequest
from app.services.openai_service import generate_fortune

router = APIRouter()


@router.post("/check-my-fortune")
async def check_my_fortune(request: FortuneRequest):
    prompt = f"User with ID {request.userId} asks: {request.query} with cards {', '.join(request.tarotCards)}."
    try:
        fortune = generate_fortune(prompt)
        return {"fortune": fortune}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
