import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.role import (
    create_role,
    delete_role,
    get_all_roles,
    get_role_by_id,
    update_role,
)
from app.db.session import get_session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate

router = APIRouter()


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_new_role(
    *,
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_session),
) -> Role:
    """
    Create new role.

    Args:
        role_in (RoleCreate): The role data to create.
        db (AsyncSession): Database session.

    Returns:
        Role: The created role.
    """
    # Check if role with this name already exists
    existing_roles = await get_all_roles()
    for role in existing_roles:
        if role.name == role_in.name:
            raise HTTPException(
                status_code=400,
                detail="The role with this name already exists in the system.",
            )

    role_data = role_in.dict()
    role = Role(**role_data)
    created_role = await create_role(role)
    return created_role


@router.get("/", response_model=list[RoleRead])
async def read_roles(
    db: AsyncSession = Depends(get_session),
) -> list[Role]:
    """
    Retrieve roles.

    Args:
        db (AsyncSession): Database session.

    Returns:
        list[Role]: List of roles.
    """
    roles = await get_all_roles()
    return roles


@router.get("/{role_id}", response_model=RoleRead)
async def read_role_by_id(
    role_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Role:
    """
    Get a specific role by id.

    Args:
        role_id (uuid.UUID): The ID of the role to retrieve.
        db (AsyncSession): Database session.

    Returns:
        Role: The requested role.
    """
    try:
        role = await get_role_by_id(role_id)
        return role
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Role not found") from e


@router.put("/{role_id}", response_model=RoleRead)
async def update_existing_role(
    *,
    role_id: uuid.UUID,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_session),
) -> Role:
    """
    Update a role.

    Args:
        role_id (uuid.UUID): The ID of the role to update.
        role_in (RoleUpdate): The role data to update.
        db (AsyncSession): Database session.

    Returns:
        Role: The updated role.
    """
    role_data = role_in.dict(exclude_unset=True)
    if not role_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update",
        )

    # Check if role exists
    try:
        await get_role_by_id(role_id)
    except HTTPException:
        raise HTTPException(
            status_code=404,
            detail="The role with this id does not exist in the system",
        ) from HTTPException

    # Check if updated name conflicts with existing roles
    if role_data.get("name"):
        all_roles = await get_all_roles()
        for role in all_roles:
            # Skip the current role being updated
            if role.id == role_id:
                continue
            if role.name == role_data["name"]:
                raise HTTPException(
                    status_code=400,
                    detail="The role with this name already exists in the system.",
                )

    try:
        updated_role = await update_role(role_id, role_data)
        return updated_role
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error updating role: {str(e)}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while updating role",
        ) from e


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(
    *,
    role_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Delete a role.

    Args:
        role_id (uuid.UUID): The ID of the role to delete.
        db (AsyncSession): Database session.

    Returns:
        None: Returns no content on successful deletion.
    """
    try:
        await get_role_by_id(role_id)
    except HTTPException:
        raise HTTPException(status_code=404, detail="Role not found") from HTTPException

    await delete_role(role_id)
    return None
