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


class TelegramLoginRequestUpdate(BaseModel):
    tg_id: str
    first_name: str


class TelegramLoginResponse(BaseModel):
    tg_id: str
    first_name: str
    last_name: str
    language_code: str

class ReferralRequest(BaseModel):
    referrer_id: str
    referred_id: str

class ReferralResponse(BaseModel):
    id: str
    referrer_id: str
    referred_id: str
    status: str

class ReferralFetchRequest(BaseModel):
    id: str
    referrer_id: str

class ReferralUpdateRequest(BaseModel):
    id: str
    status: str


class User(BaseModel):
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


class TarotRules(BaseModel):
    rule_name: str
    flip_card_deduction: int
    roll_added_points: int
    every_day_sent_rolls: int
    default_question_list: List[str]

class Referral(BaseModel):
    id: str
    referrer_id: str
    referred_id: str
    status: str
    created_at: datetime
