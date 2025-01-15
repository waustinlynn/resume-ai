from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.domain.models.resume import MissingResumeException, Resume
from app.infrastructure.factories import get_abstract_resume_persistence
from app.infrastructure.middleware.header_verification_middleware import (
    get_hashed_email_from_header,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_resume(
    abstract_resume_persistence: AbstractResumePersistence = Depends(
        get_abstract_resume_persistence
    ),
    hashed_email: str = Depends(get_hashed_email_from_header),
) -> Resume:
    try:
        resume = abstract_resume_persistence.get_resume(hashed_email)
        return resume
    except MissingResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )
