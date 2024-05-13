# app/models/schemas.py

from pydantic import BaseModel
from typing import List


class FortuneRequest(BaseModel):
    userId: str
    tarotCards: List[str]
    query: str


class TelegramLoginRequest(BaseModel):
    tg_id: str
    first_name: str
    last_name: str
    username: str
    language_code: str
