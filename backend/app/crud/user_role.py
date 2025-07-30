from uuid import UUID
from backend.app.db.session import db_session
from backend.app.models.user_role import UserRole
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_user_role(user_id: UUID, role_id: UUID) -> UserRole:
    """
    Create a new user role association.
    """
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db_session.add(user_role)
    await db_session.commit()
    await db_session.refresh(user_role)
    return user_role


async def get_user_role_by_ids(user_id: UUID, role_id: UUID) -> UserRole | None:
    """
    Get a user role association by user and role IDs.
    """
    query = (
        select(UserRole)
        .where(UserRole.user_id == user_id, UserRole.role_id == role_id)
        .options(selectinload(UserRole.user), selectinload(UserRole.role))
    )
    result = await db_session.execute(query)
    return result.scalars().first()


async def get_all_user_roles() -> list[UserRole]:
    """
    Get all user role associations.
    """
    query = select(UserRole).options(
        selectinload(UserRole.user), selectinload(UserRole.role)
    )
    result = await db_session.execute(query)
    return result.scalars().all()


async def update_user_role(
    user_id: UUID, role_id: UUID, new_role_id: UUID
) -> UserRole | None:
    """
    Update a user role association.
    """
    user_role = await get_user_role_by_ids(user_id, role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    user_role.role_id = new_role_id
    await db_session.commit()
    await db_session.refresh(user_role)
    return user_role


async def delete_user_role(user_id: UUID, role_id: UUID) -> None:
    """
    Delete a user role association.
    """
    user_role = await get_user_role_by_ids(user_id, role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    await db_session.delete(user_role)
    await db_session.commit()
