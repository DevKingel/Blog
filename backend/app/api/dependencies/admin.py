from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.crud.user import get_user_by_id
from app.db.session import get_session
from app.models.user import User


async def get_current_user(token: str, db: AsyncSession = Depends(get_session)) -> User:
    """
    Get the current user from the JWT token.

    Args:
        token: JWT token from the Authorization header
        db: Database session

    Returns:
        User: The current user

    Raises:
        HTTPException: If the token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = UUID(user_id)
    except JWTError as e:
        raise credentials_exception from e

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(token: str, db: AsyncSession = Depends(get_session)) -> User:
    """
    Get the current admin user from the JWT token.

    Args:
        token: JWT token from the Authorization header
        db: Database session

    Returns:
        User: The current admin user

    Raises:
        HTTPException: If the token is invalid, user not found, or user is not admin
    """
    user = await get_current_user(token, db)

    # Check if user has admin role
    # For now, we'll check if the user has a role named "admin"
    # In a real implementation, you might want to check a specific field or relationship
    is_admin = False
    for role in user.roles:
        if role.name.lower() == "admin":
            is_admin = True
            break

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Admin privileges required.",
        )

    return user
