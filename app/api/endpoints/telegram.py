# app/api/endpoints/telegram.py

from fastapi import APIRouter
from app.models.schemas import TelegramLoginRequest

router = APIRouter()


@router.post("/login")
async def telegram_login(request: TelegramLoginRequest):
    user = request.dict()
    # Here you would normally check the database and create/update the user record
    return user
