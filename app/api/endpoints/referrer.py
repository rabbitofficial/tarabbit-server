# here should complete /api/referral, /api/referral/fetch, and /api/referral/update endpoints.

import json
from uuid import UUID
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.models.schemas import User, ReferralRequest, ReferralResponse, ReferralFetchRequest, ReferralUpdateRequest
from app.api.endpoints.telegram import users, db

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

    referral_exists = referrals.find_one( {"referrer_id": referral_request.referrer_id, 
                                           "referred_id": referral_request.referred_id} )
    if referral_exists is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Referral already exists!"},
        )
    else:
        id = UUID().hex
        referrals.insert_one( {"id": id, 
                               "referrer_id": referral_request.referrer_id, 
                               "referred_id": referral_request.referred_id, 
                               "status": "pending"} )
        return JSONResponse( status_code=status.HTTP_201_CREATED, content={"id": id,
                                                                            "referrer_id": referral_request.referrer_id,
                                                                            "referred_id": referral_request.referred_id,
                                                                            "status": "pending"} )


@router.post("/api/referral/fetch")
async def referral_fetch(request: ReferralFetchRequest):
    referral_fetch_request = ReferralFetchRequest(**request.dict())
    return json.loads(json.dumps("", default=str))

@router.post("/api/referral/update")
async def referral_update(request: ReferralUpdateRequest):
    referral_update_request = ReferralUpdateRequest(**request.dict())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str("")}"},
    )