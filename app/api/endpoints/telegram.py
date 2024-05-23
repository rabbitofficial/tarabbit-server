# app/api/endpoints/telegram.py
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import ValidationError
from app.models.schemas import TelegramLoginRequest, User

router = APIRouter()

client = MongoClient('mongodb://localhost:27017/')
db = client['rabbitDB']
users = db['users']

@router.post("/login")
async def telegram_login(request: TelegramLoginRequest):
    try:
        login = TelegramLoginRequest(**request.dict())
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing_user = users.find_one({"tg_id": login.tg_id})
    if existing_user is not None:
        return

    user = User(
        tg_id=login.tg_id,
        first_name=login.first_name,
        last_name=login.last_name,
        username=login.username,
        language_code=telegram_login.language_code
    )
    users.insert_one(user.dict())

    return user.dict()
