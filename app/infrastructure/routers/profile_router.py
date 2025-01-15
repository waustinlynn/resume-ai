from fastapi import APIRouter, Depends, status

from app.domain.models.profile import Profile
from app.domain.models.resume import Resume
from app.infrastructure.factories import get_abstract_resume_persistence
from app.infrastructure.middleware.header_verification_middleware import (
    get_hashed_email_from_header,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: Profile,
    hashed_email: str = Depends(get_hashed_email_from_header),
    abstract_resume_persistence=Depends(get_abstract_resume_persistence),
) -> Resume:
    resume = Resume(**{"id": hashed_email, "profile": profile})
    abstract_resume_persistence.create_resume(resume)
    return resume
