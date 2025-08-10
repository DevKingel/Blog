import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.profile import (
    get_current_user_profile,
    update_current_user_profile,
)
from app.schemas.profile import ProfileRead, ProfileUpdate


@pytest.mark.asyncio
async def test_get_current_user_profile_success():
    """Test successful retrieval of current user's profile."""
    # Mock data
    user_id = uuid.uuid4()

    # Create a proper mock user object
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.created_at = "2023-01-01T00:00:00"

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user:
        mock_get_user.return_value = mock_user

        # Call the endpoint
        result = await get_current_user_profile(user_id=user_id, db=mock_db)

        # Assertions
        assert isinstance(result, ProfileRead)
        assert result.id == user_id
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        mock_get_user.assert_called_once_with(mock_db, user_id)


@pytest.mark.asyncio
async def test_get_current_user_profile_user_not_found():
    """Test retrieval of profile for non-existent user."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user:
        mock_get_user.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_profile(user_id=user_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"
        mock_get_user.assert_called_once_with(mock_db, user_id)


@pytest.mark.asyncio
async def test_update_current_user_profile_success():
    """Test successful update of current user's profile."""
    # Mock data
    user_id = uuid.uuid4()

    # Create proper mock user objects
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.created_at = "2023-01-01T00:00:00"

    mock_updated_user = MagicMock()
    mock_updated_user.id = user_id
    mock_updated_user.username = "updateduser"
    mock_updated_user.email = "updated@example.com"
    mock_updated_user.hashed_password = "hashed_password"
    mock_updated_user.created_at = "2023-01-01T00:00:00"

    # Mock dependencies
    mock_db = AsyncMock()
    profile_update = ProfileUpdate(username="updateduser", email="updated@example.com")

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.profile.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = mock_user
        mock_update_user.return_value = mock_updated_user

        # Call the endpoint
        result = await update_current_user_profile(
            user_id=user_id, profile_update=profile_update, db=mock_db
        )

        # Assertions
        assert isinstance(result, ProfileRead)
        assert result.id == user_id
        assert result.username == "updateduser"
        assert result.email == "updated@example.com"
        mock_get_user.assert_called_once_with(mock_db, user_id)
        mock_update_user.assert_called_once_with(
            mock_db,
            user_id,
            {"username": "updateduser", "email": "updated@example.com"},
        )


@pytest.mark.asyncio
async def test_update_current_user_profile_user_not_found_get():
    """Test update of profile when user is not found during get."""
    # Mock data
    user_id = uuid.uuid4()
    profile_update = ProfileUpdate(username="updateduser")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user:
        mock_get_user.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_current_user_profile(
                user_id=user_id, profile_update=profile_update, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"
        mock_get_user.assert_called_once_with(mock_db, user_id)


@pytest.mark.asyncio
async def test_update_current_user_profile_user_not_found_update():
    """Test update of profile when user is not found during update."""
    # Mock data
    user_id = uuid.uuid4()

    # Create proper mock user object
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.created_at = "2023-01-01T00:00:00"

    # Mock dependencies
    mock_db = AsyncMock()
    profile_update = ProfileUpdate(username="updateduser")

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.profile.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = mock_user
        mock_update_user.return_value = None  # Simulate user not found during update

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_current_user_profile(
                user_id=user_id, profile_update=profile_update, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"
        mock_get_user.assert_called_once_with(mock_db, user_id)
        mock_update_user.assert_called_once_with(
            mock_db, user_id, {"username": "updateduser"}
        )


@pytest.mark.asyncio
async def test_update_current_user_profile_invalid_data():
    """Test update of profile with invalid data."""
    # Mock data
    user_id = uuid.uuid4()

    # Create proper mock user object
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.created_at = "2023-01-01T00:00:00"

    # Mock dependencies
    mock_db = AsyncMock()

    # Create invalid profile update data (this will be caught by Pydantic validation)
    with pytest.raises(ValueError):
        ProfileUpdate(email="invalid-email")  # Invalid email format

    # Test with valid data but simulate validation error in endpoint
    profile_update = ProfileUpdate(username="validuser", email="valid@example.com")

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.profile.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = mock_user
        mock_update_user.return_value = mock_user

        # Call the endpoint with valid data
        result = await update_current_user_profile(
            user_id=user_id, profile_update=profile_update, db=mock_db
        )

        # Assertions
        assert isinstance(result, ProfileRead)
        mock_get_user.assert_called_once_with(mock_db, user_id)
        mock_update_user.assert_called_once_with(
            mock_db, user_id, {"username": "validuser", "email": "valid@example.com"}
        )


@pytest.mark.asyncio
async def test_update_current_user_profile_partial_update():
    """Test partial update of current user's profile."""
    # Mock data
    user_id = uuid.uuid4()

    # Create proper mock user objects
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"  # This should remain unchanged
    mock_user.hashed_password = "hashed_password"
    mock_user.created_at = "2023-01-01T00:00:00"

    # Mock updated user data
    mock_updated_user = MagicMock()
    mock_updated_user.id = user_id
    mock_updated_user.username = "updateduser"  # This should be updated
    mock_updated_user.email = "test@example.com"  # This should remain unchanged
    mock_updated_user.hashed_password = "hashed_password"
    mock_updated_user.created_at = "2023-01-01T00:00:00"

    # Mock dependencies
    mock_db = AsyncMock()
    profile_update = ProfileUpdate(username="updateduser")  # Only update username

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.profile.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.profile.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = mock_user
        mock_update_user.return_value = mock_updated_user

        # Call the endpoint
        result = await update_current_user_profile(
            user_id=user_id, profile_update=profile_update, db=mock_db
        )

        # Assertions
        assert isinstance(result, ProfileRead)
        assert result.id == user_id
        assert result.username == "updateduser"
        assert result.email == "test@example.com"  # Should remain unchanged
        mock_get_user.assert_called_once_with(mock_db, user_id)
        mock_update_user.assert_called_once_with(
            mock_db, user_id, {"username": "updateduser"}
        )
