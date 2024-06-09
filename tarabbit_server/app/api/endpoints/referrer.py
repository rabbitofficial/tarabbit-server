# here should complete /api/referral, /api/referral/fetch, and /api/referral/update endpoints.

import json
from datetime import datetime
import uuid
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models.schemas import (
    User,
    ReferralRequest,
    ReferralResponse,
    ReferralFetchRequest,
    ReferralUpdateRequest,
)
from api.endpoints.telegram import users, db

router = APIRouter()

referrals = db["referrals"]


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

    return {"status": "ok update referal"}
