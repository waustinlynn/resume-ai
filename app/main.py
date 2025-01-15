from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.infrastructure.middleware.header_verification_middleware import (
    EmailHeaderMiddleware,
)
from app.infrastructure.routers import profile_router, resume_router

api_app = FastAPI()
api_app.add_middleware(EmailHeaderMiddleware)
api_app.include_router(profile_router.router, prefix="/profile", tags=["profile"])
api_app.include_router(resume_router.router, prefix="/resume", tags=["resume"])

app = FastAPI()
app.mount("/api", api_app)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    print(exc)
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={
            "error": "Validation failed",
            "details": exc.errors(),  # Detailed list of validation errors
        },
    )
