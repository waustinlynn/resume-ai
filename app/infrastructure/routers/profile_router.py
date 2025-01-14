from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.domain.models.profile import Profile
from app.domain.services.abstract_profile_service import (
    AbstractProfileService,
    MissingProfileError,
)
from app.infrastructure.factories import get_abstract_profile_service

router = APIRouter()


@router.get("/{profile_id}", response_model=Profile)
async def get_profile(
    profile_id: str,
    abstract_profile_service: AbstractProfileService = Depends(
        get_abstract_profile_service
    ),
) -> Profile:
    try:
        return abstract_profile_service.get_profile(profile_id)
    except MissingProfileError:
        return JSONResponse(status_code=400, content={"message": "Profile not found"})


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: Profile,
    abstract_profile_service: AbstractProfileService = Depends(
        get_abstract_profile_service
    ),
) -> Profile:
    return abstract_profile_service.create_profile(profile)
