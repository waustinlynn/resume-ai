from io import BytesIO

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.responses import JSONResponse

from app.domain.models.chat_completion import ChatCompletion
from app.domain.models.chat_response import ChatResponse
from app.domain.models.resume import ResumeException
from app.infrastructure.chat.abstract_chat_completion import AbstractChatCompletion
from app.infrastructure.factories import (
    get_abstract_chat_completion,
    get_abstract_document_generator,
    get_abstract_resume_persistence,
)
from app.infrastructure.middleware.header_verification_middleware import (
    get_hashed_email_from_header,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)

router = APIRouter()


def get_resume_response(
    hashed_email: str,
    abstract_resume_persistence: AbstractResumePersistence,
    abstract_chat_completion: AbstractChatCompletion,
    content: str,
) -> ChatResponse:
    resume = abstract_resume_persistence.get_resume(hashed_email)
    chat_completion_model = ChatCompletion(
        **{"resume": resume, "job_description": content}
    )
    return abstract_chat_completion.complete(
        chat_completion_model.get_chat_completion_messages()
    )


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
) -> ChatResponse:
    try:
        return get_resume_response(
            hashed_email, abstract_resume_persistence, abstract_chat_completion, content
        )
    except ResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router.post("/doc", status_code=status.HTTP_200_OK)
async def get_resume_document(
    content: str = Body(..., media_type="text/plain"),
    abstract_resume_persistence: AbstractResumePersistence = Depends(
        get_abstract_resume_persistence
    ),
    abstract_chat_completion: AbstractChatCompletion = Depends(
        get_abstract_chat_completion
    ),
    hashed_email: str = Depends(get_hashed_email_from_header),
) -> Response:
    try:
        chat_response = get_resume_response(
            hashed_email, abstract_resume_persistence, abstract_chat_completion, content
        )
        abstract_document_generator = get_abstract_document_generator()
        file_stream = BytesIO()
        abstract_document_generator.generate(chat_response, file_stream)
        file_stream.seek(0)
        return Response(
            content=file_stream.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": 'attachment; filename="resume_results.docx"'
            },
        )
    except ResumeException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )
