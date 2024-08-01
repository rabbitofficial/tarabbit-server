# app/api/endpoints/telegram.py
import json

from fastapi import APIRouter, HTTPException, Request
from pymongo import MongoClient
from app.core.config import point_rule
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse

from models.schemas import (
    TelegramLoginRequest,
    User,
    TelegramLoginResponse,
    TelegramLoginRequestUpdate,
    TarotRules,
)
from core.config import settings

router = APIRouter()

client = MongoClient(settings.MONGO_URI)
db = client["rabbitDB"]
users = db["users"]
tarot_rules = db["tarot_rules"]

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

    # get setting from db
    appSettings = tarot_rules.find_one({"rule_name": "rule1"})
    left_roll_times = 10
    if appSettings is not None:
        left_roll_times = appSettings["every_day_sent_rolls"]

    if existing_user is None:
        try:
            user = User(
                tg_id=login.tg_id,
                first_name=login.first_name,
                last_name=login.last_name,
                username=login.username,
                language_code=login.language_code,
                left_roll_times=left_roll_times,
                level = 0,
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
            not_none_fields = {
                k: v
                for k, v in login.dict().items()
                if v != None and k != "tg_id"
            }
            if "points" in not_none_fields:
                level =0
                level_point_list = point_rule.LEVEL_DEFINE
                for i,level_point in enumerate(level_point_list):
                    if not_none_fields["points"] > level_point:
                        level = 5 - i
                        break
                user = users.find_one({"tg_id": login.tg_id}, {'points': 1, '_id': 0, "level": 1})
                if user["level"] is None or int(user["level"]) < level:
                    not_none_fields["level"] = level
            users.update_one({"tg_id": login.tg_id}, {"$set": not_none_fields})
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


@router.post("/api/tg/tarot_rules/add")
async def telegram_rules_add(request: TarotRules):
    try:
        ruleData = TarotRules(**request.dict())
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
    try:
        rule = TarotRules(
            rule_name=ruleData.rule_name,
            flip_card_deduction=ruleData.flip_card_deduction,
            roll_added_points=ruleData.roll_added_points,
            every_day_sent_rolls=ruleData.every_day_sent_rolls,
            default_question_list=ruleData.default_question_list,
        )
        tarot_rules.insert_one(rule.dict())
    except AttributeError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Invalid request: Missing or invalid field '{str(e)}'"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(e)}"},
        )

    return {"status": "ok add"}


@router.post("/api/tg/tarot_rules/update")
async def telegram_rules_update(request: TarotRules):
    try:
        ruleData = TarotRules(**request.dict())
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
    existing_rule = tarot_rules.find_one({"rule_name": ruleData.rule_name})

    if existing_rule is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Rule does not exist!"},
        )
    else:
        try:
            rule = TarotRules(
                rule_name=ruleData.rule_name,
                flip_card_deduction=ruleData.flip_card_deduction,
                roll_added_points=ruleData.roll_added_points,
                every_day_sent_rolls=ruleData.every_day_sent_rolls,
                default_question_list=ruleData.default_question_list,
            )

            tarot_rules.update_one(
                {"rule_name": ruleData.rule_name}, {"$set": rule.dict()}
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

    return {"status": "ok update"}


@router.get("/api/tg/tarot_rules/fetch")
async def telegram_rules_fetch(rule_name: str):
    if isinstance(rule_name, str):
        existing_rule = tarot_rules.find_one({"rule_name": "rule1"})
        if existing_rule is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Rule does not exist!"},
            )
        else:
            return json.loads(json.dumps(existing_rule, default=str))
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid request: Missing or invalid param"},
        )
