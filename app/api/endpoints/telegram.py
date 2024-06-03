# app/api/endpoints/telegram.py
import json

from fastapi import APIRouter, HTTPException, Request
from pymongo import MongoClient
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.schemas import (
    TelegramLoginRequest,
    User,
    TelegramLoginResponse,
    TelegramLoginRequestUpdate,
)
from config import settings

router = APIRouter()

client = MongoClient(settings.MONGO_URI)
db = client["rabbitDB"]
users = db["users"]


@router.post("/api/tg/login")
async def telegram_login(request: TelegramLoginRequest):
    try:
        login = TelegramLoginRequest(**request.dict())
    except json.JSONDecodeError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid JSON payload"},
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": e.errors()}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(e)}"},
        )

    existing_user = users.find_one({"tg_id": login.tg_id})

    if existing_user is None:
        try:
            user = User(
                tg_id=login.tg_id,
                first_name=login.first_name,
                last_name=login.last_name,
                username=login.username,
                language_code=login.language_code,
            )
            users.insert_one(user.dict())
        except AttributeError as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": f"Invalid request: Missing or invalid field '{str(e)}'"
                },
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Internal server error: {str(e)}"},
            )

    else:
        user = User(**existing_user)

    response = TelegramLoginResponse(**user.dict())
    return response.dict()


@router.get("/api/tg/login/fetch")
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


@router.post("/api/tg/login/update")
async def telegram_login_update(request: TelegramLoginRequestUpdate):
    try:
        login = TelegramLoginRequestUpdate(**request.dict())
    except json.JSONDecodeError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid JSON payload"},
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": e.errors()}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(e)}"},
        )

    existing_user = users.find_one({"tg_id": login.tg_id})

    if existing_user is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "User does not exist!"},
        )
    else:
        try:
            users.update_one(
                {"tg_id": login.tg_id}, {"$set": {"first_name": login.first_name}}
            )
        except AttributeError as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": f"Invalid request: Missing or invalid field '{str(e)}'"
                },
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Internal server error: {str(e)}"},
            )

    return {"status": "ok"}
