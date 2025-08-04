from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create an asynchronous engine to the database
# echo=True will log all SQL statements, which is useful for debugging.
# It should be turned off in production.
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

# Create a sessionmaker for creating new AsyncSession objects
# expire_on_commit=False prevents attributes from being expired after a commit.
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator:
    """
    Dependency function that yields an an AsyncSession
    and ensures it's closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
