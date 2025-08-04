from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import category, post, tag, users
from app.db.session import engine
from app.models.user import User  # Import your models

from .core.api_key_middleware import APIKeyMiddleware
from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, create database tables
    async with engine.begin() as conn:
        # await conn.run_sync(User.metadata.drop_all) # Use this to drop tables for a fresh start
        await conn.run_sync(User.metadata.create_all)
    yield
    # On shutdown, you can add cleanup code here


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.add_middleware(APIKeyMiddleware, api_key=settings.API_KEY)

# Include the user router
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

# Include the post, category, and tag routers
app.include_router(post.router, prefix=f"{settings.API_V1_STR}", tags=["posts"])
app.include_router(
    category.router, prefix=f"{settings.API_V1_STR}", tags=["categories"]
)
app.include_router(tag.router, prefix=f"{settings.API_V1_STR}", tags=["tags"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API!"}
