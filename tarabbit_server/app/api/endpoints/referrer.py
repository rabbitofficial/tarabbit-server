# here should complete /api/referral, /api/referral/fetch, and /api/referral/update endpoints.

import json
from datetime import datetime
import uuid
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models.schemas import (
    ReferralRequest,
    ReferralUpdateRequest,
)
from api.endpoints.telegram import db
from app.core.config import point_rule

router = APIRouter()

referrals = db["referrals"]
users = db["users"]


@router.post("/api/referral")
async def referral(request: ReferralRequest):
    try:
        referral_request = ReferralRequest(**request.dict())
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

    referral_exists = referrals.find_one(
        {
            "referrer_id": referral_request.referrer_id,
            "referred_id": referral_request.referred_id,
        }
    )
    if referral_exists is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"info":"existed","detail": "Referral already exists!"},
        )
    else:
        id = str(uuid.uuid4())
        referrals.insert_one(
            {
                "id": id,
                "referrer_id": referral_request.referrer_id,
                "referred_id": referral_request.referred_id,
                "status": "pending",
                "created_at": datetime.now(),
            }
        )
        referred_user = users.find_one({"tg_id": referral_request.referrer_id})
        if referred_user:
            if referred_user["is_premium"]:
                users.update_one({"tg_id": referral_request.referrer_id},
                                 {"$inc": {"points": point_rule.INVITE_PREMIUM_USER}})
            else:
                users.update_one({"tg_id": referral_request.referrer_id},
                                 {"$inc": {"points": point_rule.INVITE_NORMAL_USER}})
        invite_user_rewards = {
            5: point_rule.INVITE_5_USER,
            20: point_rule.INVITE_20_USER,
            100: point_rule.INVITE_100_USER,
        }
        referred_user_num = referrals.count_documents({"referrer_id": referral_request.referrer_id})
        if referred_user_num in invite_user_rewards.keys():
            users.update_one({"tg_id": referral_request.referrer_id}, {"$inc": {"points": invite_user_rewards[referred_user_num]}})

        user = users.find_one({"tg_id": referral_request.referrer_id}, {'points': 1, '_id': 0, "level": 1})
        level_point_list = point_rule.LEVEL_DEFINE
        for i, level_point in enumerate(level_point_list):
            if user["points"] > level_point:
                level = 5 - i
                if user["level"] is None or int(user["level"]) < level:
                    users.update_one({"tg_id": referral_request.referrer_id},
                                     {"$set": {"level": level}})
                break
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": id,
                "referrer_id": referral_request.referrer_id,
                "referred_id": referral_request.referred_id,
                "status": "pending",
                "info": "new"
            },
        )


@router.get("/api/referral/fetch")
async def referral_fetch(referrer_id: str):
    if isinstance(referrer_id, str):
        existing_referral = referrals.find_one({"referrer_id": referrer_id})
        if existing_referral is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Referral does not exist!"},
            )
        else:
            return json.loads(json.dumps(existing_referral, default=str))
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid request: Missing or invalid param"},
        )


@router.post("/api/referral/update")
async def referral_update(request: ReferralUpdateRequest):
    try:
        referral_update_request = ReferralUpdateRequest(**request.dict())
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
    existing_referral = referrals.find_one(
        {"referrer_id": referral_update_request.referrer_id}
    )

    if existing_referral is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Referral does not exist!"},
        )
    else:
        try:
            referrals.update_one(
                {"referrer_id": referral_update_request.referrer_id},
                {"$set": {"status": referral_update_request.status}},
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

    return {"status": "ok update referral"}

@router.get("/api/referral/getInviteInfo")
async def referral_fetch(referrer_id: str):
    if isinstance(referrer_id, str):
        existing_referral = referrals.find({"referrer_id": referrer_id})
        print(99999999)
        print(existing_referral)
        if existing_referral is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Referral does not exist!"},
            )
        else:
            result = list(existing_referral)
            return json.loads(json.dumps(result, default=str))
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid request: Missing or invalid param"},
        )