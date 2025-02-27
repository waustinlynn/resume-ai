from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value

excluded_paths = ["/api/docs", "/api/openapi.json"]


class EmailHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in excluded_paths:
            header_value = request.headers.get("x-email-header")
            if not header_value:
                return JSONResponse(
                    content={"detail": "x-email-header is required"}, status_code=400
                )
            request.state.email_header = header_value
        response = await call_next(request)
        return response


def get_hashed_email_from_header(request: Request):
    settings = Settings()
    return hash_value(request.state.email_header, settings.hashing_secret)
