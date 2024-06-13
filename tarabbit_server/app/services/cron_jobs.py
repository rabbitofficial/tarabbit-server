from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from core.config import settings
from fastapi import APIRouter, HTTPException, Request
from pymongo import MongoClient
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

client = MongoClient(settings.MONGO_URI)
db = client["rabbitDB"]
users = db["users"]
tarot_rules = db["tarot_rules"]

# cron jobs
scheduler = AsyncIOScheduler()
# timezone="UTC"


async def reset_rolls():
    users.update_many({}, {"$inc": {"left_roll_times": 50}})
    print("Number of documents updated")


scheduler.add_job(func=reset_rolls, trigger="cron", hour="*/8")
# scheduler.add_job(func=reset_rolls, trigger="interval", seconds=3)
scheduler.start()


async def telegram_login_fetch(tg_id: str):
    if isinstance(tg_id, str):
        existing_user = users.find_one({"tg_id": tg_id}, {"_id": 0})
        if existing_user is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "User does not exist!"},
            )
        else:
            return json.loads(json.dumps(existing_user, default=str))
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid request: Missing or invalid param"},
        )


# cron jobs
