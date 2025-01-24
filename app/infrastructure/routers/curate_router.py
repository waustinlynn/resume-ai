from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from app.domain.models.chat_completion import ChatCompletion
from app.domain.models.resume import MissingResumeException
from app.infrastructure.chat.abstract_chat_completion import AbstractChatCompletion
from app.infrastructure.factories import (
    get_abstract_chat_completion,
    get_abstract_resume_persistence,
)
from app.infrastructure.middleware.header_verification_middleware import (
    get_hashed_email_from_header,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def get_resume(
    content: str = Body(..., media_type="text/plain"),
    abstract_resume_persistence: AbstractResumePersistence = Depends(
        get_abstract_resume_persistence
    ),
    abstract_chat_completion: AbstractChatCompletion = Depends(
        get_abstract_chat_completion
    ),
    hashed_email: str = Depends(get_hashed_email_from_header),
) -> str:
    try:
        resume = abstract_resume_persistence.get_resume(hashed_email)
        chat_completion_model = ChatCompletion(
            **{"resume": resume, "job_description": content}
        )
        return abstract_chat_completion.complete(
            chat_completion_model.get_chat_completion_messages()
        )
    except MissingResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )
