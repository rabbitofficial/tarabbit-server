# app/models/schemas.py

from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime


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


class UserDB(BaseModel):
    id: Optional[str]
    tg_id: str
    name: Optional[str]
    email: Optional[str]
    points: Optional[int]
    level: Optional[int]
    group: Optional[str]
    left_roll_times: Optional[int]
    total_rolled_times: Optional[int]
    created_at: Optional[datetime]
    first_name: str
    last_name: str
    username: str
    invited_total_friends: Optional[int]
    invited_normal_friends: Optional[int]
    invited_premium_friends: Optional[int]
    tarot_requested_times: Optional[int]
    language_code: str
    joined_community: Optional[bool]
    joined_X: Optional[bool]
    update_at: Optional[datetime]
    is_premium: Optional[bool]
    photo_url: Optional[str]
