from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import engine
from app.models.role import Role


async def create_role(role: Role) -> Role:
    """
    Creates a new role.
    """
    engine.add(role)
    await engine.commit()
    await engine.refresh(role)
    return role


async def get_role_by_id(role_id: UUID) -> Role | None:
    """
    Retrieves a role by its ID.
    """
    query = select(Role).where(Role.id == role_id).options(selectinload(Role.users))
    result = await engine.execute(query)
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


async def get_all_roles() -> list[Role]:
    """
    Retrieves all roles.
    """
    query = select(Role).options(selectinload(Role.users))
    result = await engine.execute(query)
    return result.scalars().all()


async def update_role(role_id: UUID, role_data: dict) -> Role | None:
    """
    Updates a role.
    """
    query = select(Role).where(Role.id == role_id)
    result = await engine.execute(query)
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    for key, value in role_data.items():
        setattr(role, key, value)
    await engine.commit()
    await engine.refresh(role)
    return role


async def delete_role(role_id: UUID) -> None:
    """
    Deletes a role.
    """
    query = select(Role).where(Role.id == role_id)
    result = await engine.execute(query)
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await engine.delete(role)
    await engine.commit()
