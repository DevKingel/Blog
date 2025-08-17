import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.roles import (
    create_new_role,
    delete_role_by_id,
    read_role_by_id,
    read_roles,
    update_existing_role,
)
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


@pytest.mark.asyncio
async def test_create_role_success():
    """Test successful role creation."""
    # Mock data
    role_data = RoleCreate(name="admin")
    mock_role = Role(id=uuid.uuid4(), name="admin")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function
    with (
        patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles,
        patch("app.api.v1.endpoints.roles.create_role") as mock_create_role,
    ):
        mock_get_all_roles.return_value = []
        mock_create_role.return_value = mock_role

        # Call the endpoint
        result = await create_new_role(role_in=role_data, db=mock_db)

        # Assertions
        assert result.name == "admin"
        assert isinstance(result.id, uuid.UUID)
        mock_get_all_roles.assert_called_once()
        mock_create_role.assert_called_once()


@pytest.mark.asyncio
async def test_create_role_duplicate_name():
    """Test role creation with duplicate name."""
    # Mock data
    role_data = RoleCreate(name="admin")
    existing_role = Role(id=uuid.uuid4(), name="admin")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function
    with patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles:
        mock_get_all_roles.return_value = [existing_role]

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await create_new_role(role_in=role_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in exc_info.value.detail
        mock_get_all_roles.assert_called_once()


@pytest.mark.asyncio
async def test_read_roles_success():
    """Test successful retrieval of all roles."""
    # Mock data
    mock_roles = [
        Role(id=uuid.uuid4(), name="admin"),
        Role(id=uuid.uuid4(), name="user"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function
    with patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles:
        mock_get_all_roles.return_value = mock_roles

        # Call the endpoint
        result = await read_roles(db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].name == "admin"
        assert result[1].name == "user"
        mock_get_all_roles.assert_called_once()


@pytest.mark.asyncio
async def test_read_roles_empty():
    """Test retrieval of roles when no roles exist."""
    # Mock data
    mock_roles = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function
    with patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles:
        mock_get_all_roles.return_value = mock_roles

        # Call the endpoint
        result = await read_roles(db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_all_roles.assert_called_once()


@pytest.mark.asyncio
async def test_read_role_by_id_success():
    """Test successful retrieval of a role by ID."""
    # Mock data
    role_id = uuid.uuid4()
    mock_role = Role(id=role_id, name="admin")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function
    with patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id:
        mock_get_role_by_id.return_value = mock_role

        # Call the endpoint
        result = await read_role_by_id(role_id=role_id, db=mock_db)

        # Assertions
        assert result.name == "admin"
        assert result.id == role_id
        mock_get_role_by_id.assert_called_once_with(role_id)


@pytest.mark.asyncio
async def test_read_role_by_id_not_found():
    """Test retrieval of a non-existent role by ID."""
    # Mock data
    role_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id:
        mock_get_role_by_id.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await read_role_by_id(role_id=role_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Role not found"
        mock_get_role_by_id.assert_called_once_with(role_id)


@pytest.mark.asyncio
async def test_update_role_success():
    """Test successful role update."""
    # Mock data
    role_id = uuid.uuid4()
    role_update_data = RoleUpdate(name="moderator")
    existing_role = Role(id=role_id, name="admin")
    updated_role = Role(id=role_id, name="moderator")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD functions
    with (
        patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id,
        patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles,
        patch("app.api.v1.endpoints.roles.update_role") as mock_update_role,
    ):
        mock_get_role_by_id.return_value = existing_role
        mock_get_all_roles.return_value = [existing_role]
        mock_update_role.return_value = updated_role

        # Call the endpoint
        result = await update_existing_role(
            role_id=role_id, role_in=role_update_data, db=mock_db
        )

        # Assertions
        assert result.name == "moderator"
        assert result.id == role_id
        mock_get_role_by_id.assert_called_once_with(role_id)
        mock_update_role.assert_called_once()


@pytest.mark.asyncio
async def test_update_role_not_found():
    """Test update of a non-existent role."""
    # Mock data
    role_id = uuid.uuid4()
    role_update_data = RoleUpdate(name="moderator")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id:
        mock_get_role_by_id.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this id does not exist in the system",
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_role(
                role_id=role_id, role_in=role_update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "does not exist" in exc_info.value.detail
        mock_get_role_by_id.assert_called_once_with(role_id)


@pytest.mark.asyncio
async def test_update_role_duplicate_name():
    """Test role update with duplicate name."""
    # Mock data
    role_id = uuid.uuid4()
    role_update_data = RoleUpdate(name="user")
    existing_role = Role(id=role_id, name="admin")
    conflicting_role = Role(id=uuid.uuid4(), name="user")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD functions
    with (
        patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id,
        patch("app.api.v1.endpoints.roles.get_all_roles") as mock_get_all_roles,
    ):
        mock_get_role_by_id.return_value = existing_role
        mock_get_all_roles.return_value = [existing_role, conflicting_role]

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_role(
                role_id=role_id, role_in=role_update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in exc_info.value.detail
        mock_get_role_by_id.assert_called_once_with(role_id)
        mock_get_all_roles.assert_called_once()


@pytest.mark.asyncio
async def test_update_role_no_data():
    """Test role update with no data provided."""
    # Mock data
    role_id = uuid.uuid4()
    role_update_data = RoleUpdate()

    # Mock dependencies
    mock_db = AsyncMock()

    # Call the endpoint and expect HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await update_existing_role(
            role_id=role_id, role_in=role_update_data, db=mock_db
        )

    # Assertions
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "No data provided" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_role_success():
    """Test successful role deletion."""
    # Mock data
    role_id = uuid.uuid4()
    mock_role = Role(id=role_id, name="admin")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD functions
    with (
        patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id,
        patch("app.api.v1.endpoints.roles.delete_role") as mock_delete_role,
    ):
        mock_get_role_by_id.return_value = mock_role
        mock_delete_role.return_value = None

        # Call the endpoint
        result = await delete_role_by_id(role_id=role_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_role_by_id.assert_called_once_with(role_id)
        mock_delete_role.assert_called_once_with(role_id)


@pytest.mark.asyncio
async def test_delete_role_not_found():
    """Test deletion of a non-existent role."""
    # Mock data
    role_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the role CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.roles.get_role_by_id") as mock_get_role_by_id:
        mock_get_role_by_id.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await delete_role_by_id(role_id=role_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Role not found"
        mock_get_role_by_id.assert_called_once_with(role_id)
