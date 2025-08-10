from fastapi import Request
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        # Skip API key check in local development
        if settings.ENVIRONMENT == "local":
            return await call_next(request)
        api_key = request.headers.get(API_KEY_NAME)
        if api_key != self.api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key", "status_code": 401},
            )
        response = await call_next(request)
        return response
