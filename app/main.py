from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.infrastructure.routers import profile_router

app = FastAPI()


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


app.include_router(profile_router.router, prefix="/profile", tags=["profile"])
