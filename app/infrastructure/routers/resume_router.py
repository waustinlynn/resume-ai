from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.domain.models.resume import Resume, ResumeException
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
    except ResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_resume(
    resume_dict: dict,
    abstract_resume_persistence: AbstractResumePersistence = Depends(
        get_abstract_resume_persistence
    ),
    hashed_email: str = Depends(get_hashed_email_from_header),
) -> Resume:
    try:
        resume_dict["id"] = hashed_email
        resume = Resume(**resume_dict)
        resume = abstract_resume_persistence.create_resume(resume)
        return resume
    except ResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router.put("/", status_code=status.HTTP_200_OK)
async def update_resume(
    resume: Resume,
    abstract_resume_persistence: AbstractResumePersistence = Depends(
        get_abstract_resume_persistence
    ),
) -> Resume:
    try:
        print(resume)
        resume = abstract_resume_persistence.update_resume(resume)
        return resume
    except ResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )
