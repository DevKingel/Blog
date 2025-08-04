from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user import User

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, user_data: dict) -> User:
    """
    Creates a new user in the database.

    Args:
        db (AsyncSession): Database session.
        user_data (dict): Data for the new user.

    Returns:
        User: The created user object.
    """
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    """
    Retrieves a user by ID.

    Args:
        db (AsyncSession): Database session.
        user_id (UUID): The ID of the user to retrieve.

    Returns:
        Optional[User]: The user object if found, None otherwise.
    """
    query = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.comments),
            selectinload(User.roles),
            selectinload(User.posts),
        )
    )
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_multi_user(
    db: AsyncSession, *, skip: int = 0, limit: int = 100
) -> list[User]:
    """
    Get multiple users with pagination.
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: UUID, user_data: dict) -> User | None:
    """
    Updates a user by ID.

    Args:
        db (AsyncSession): Database session.
        user_id (UUID): The ID of the user to update.
        user_data (dict): Data to update the user with.

    Returns:
        Optional[User]: The updated user object if found, None otherwise.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    """
    Deletes a user by ID.

    Args:
        db (AsyncSession): Database session.
        user_id (UUID): The ID of the user to delete.

    Returns:
        bool: True if the user was deleted, False otherwise.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
