from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import (
    admin,
    auth,
    categories,
    comments,
    media,
    posts,
    profile,
    roles,
    search,
    stats,
    tags,
    users,
)
from app.db.session import engine
from app.models.user import User  # Import your models

from .core.api_key_middleware import APIKeyMiddleware
from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, create database tables
    async with engine.begin() as conn:
        # await conn.run_sync(User.metadata.drop_all)
        # # Use this to drop tables for a fresh start
        await conn.run_sync(User.metadata.create_all)
    yield
    # On shutdown, you can add cleanup code here


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.add_middleware(APIKeyMiddleware, api_key=settings.SECRET_KEY)

# Include the user router
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(
    profile.router, prefix=f"{settings.API_V1_STR}/profile", tags=["profile"]
)

# Include the post, category, tag, and comment routers
app.include_router(posts.router, prefix=f"{settings.API_V1_STR}", tags=["posts"])
app.include_router(
    categories.router, prefix=f"{settings.API_V1_STR}", tags=["categories"]
)
app.include_router(tags.router, prefix=f"{settings.API_V1_STR}", tags=["tags"])


app.include_router(
    comments.router, prefix=f"{settings.API_V1_STR}/comments", tags=["comments"]
)

app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["stats"])

app.include_router(
    search.router, prefix=f"{settings.API_V1_STR}/search", tags=["search"]
)

app.include_router(media.router, prefix=f"{settings.API_V1_STR}/media", tags=["media"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(roles.router, prefix=f"{settings.API_V1_STR}/roles", tags=["roles"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API!"}
