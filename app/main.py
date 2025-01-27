from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.infrastructure.middleware.header_verification_middleware import (
    EmailHeaderMiddleware,
)
from app.infrastructure.routers import curate_router, profile_router, resume_router
from app.infrastructure.settings import Settings

api_app = FastAPI()
api_app.add_middleware(EmailHeaderMiddleware)
api_app.include_router(profile_router.router, prefix="/profile", tags=["profile"])
api_app.include_router(resume_router.router, prefix="/resume", tags=["resume"])
api_app.include_router(curate_router.router, prefix="/curate", tags=["curate"])


app = FastAPI()
app.mount("/api", api_app)

print(Settings())


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={
            "error": "Validation failed",
            "details": exc.errors(),  # Detailed list of validation errors
        },
    )
