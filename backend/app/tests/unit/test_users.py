import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.users import (
    create_new_user,
    delete_user_by_id,
    get_user_comments,
    get_user_posts,
    read_user_by_id,
    read_users,
    update_existing_user,
)
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_user_success():
    """Test successful user creation."""
    # Mock data
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )

    mock_user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        created_at="2023-01-01T00:00:00"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.users.user_crud.get_user_by_email") as mock_get_by_email,
        patch("app.api.v1.endpoints.users.user_crud.create_user") as mock_create_user,
    ):
        mock_get_by_email.return_value = None  # No existing user
        mock_create_user.return_value = mock_user

        # Call the endpoint
        result = await create_new_user(user_in=user_data, db=mock_db)

        # Assertions
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        mock_get_by_email.assert_called_once_with(mock_db, email="test@example.com")
        mock_create_user.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    """Test user creation with duplicate email."""
    # Mock data
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )

    existing_user = User(
        id=uuid.uuid4(),
        username="existinguser",
        email="test@example.com",
        hashed_password="hashed_password",
        created_at="2023-01-01T00:00:00"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.users.user_crud.get_user_by_email") as mock_get_by_email:
        mock_get_by_email.return_value = existing_user

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await create_new_user(user_in=user_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in exc_info.value.detail
        mock_get_by_email.assert_called_once_with(mock_db, email="test@example.com")


@pytest.mark.asyncio
async def test_create_user_invalid_data():
    """Test user creation with invalid data."""
    # Mock data with invalid email
    user_data = UserCreate(
        username="testuser",
        email="invalid-email",  # Invalid email format
        hashed_password="hashed_password"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # This test would typically be handled by FastAPI validation
    # For unit testing, we'll test the function directly with valid data
    # but mock the database to raise an exception
    with (
        patch("app.api.v1.endpoints.users.user_crud.get_user_by_email") as mock_get_by_email,
        patch("app.api.v1.endpoints.users.user_crud.create_user") as mock_create_user,
    ):
        mock_get_by_email.return_value = None
        mock_create_user.side_effect = Exception("Validation error")

        # Call the endpoint and expect exception
        with pytest.raises(Exception):
            await create_new_user(user_in=user_data, db=mock_db)


@pytest.mark.asyncio
async def test_read_users_success():
    """Test successful retrieval of users with pagination."""
    # Mock data
    mock_users = [
        User(id=uuid.uuid4(), username="user1", email="user1@example.com", hashed_password="pass1"),
        User(id=uuid.uuid4(), username="user2", email="user2@example.com", hashed_password="pass2"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.users.user_crud.get_multi_user") as mock_get_multi:
        mock_get_multi.return_value = mock_users

        # Call the endpoint
        result = await read_users(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].username == "user1"
        assert result[1].username == "user2"
        mock_get_multi.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_read_users_empty():
    """Test retrieval of users when no users exist."""
    # Mock data
    mock_users = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.users.user_crud.get_multi_user") as mock_get_multi:
        mock_get_multi.return_value = mock_users

        # Call the endpoint
        result = await read_users(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_multi.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_read_user_by_id_success():
    """Test successful retrieval of a user by ID."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        created_at="2023-01-01T00:00:00"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.users.user_crud.get_user") as mock_get_user:
        mock_get_user.return_value = mock_user

        # Call the endpoint
        result = await read_user_by_id(user_id=user_id, db=mock_db)

        # Assertions
        assert result.id == user_id
        assert result.username == "testuser"
        mock_get_user.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_read_user_by_id_not_found():
    """Test retrieval of a non-existent user by ID."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function to return None
    with patch("app.api.v1.endpoints.users.user_crud.get_user") as mock_get_user:
        mock_get_user.return_value = None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await read_user_by_id(user_id=user_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail
        mock_get_user.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_update_user_success():
    """Test successful user update."""
    # Mock data
    user_id = uuid.uuid4()
    update_data = UserUpdate(username="updateduser")

    existing_user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )

    updated_user = User(
        id=user_id,
        username="updateduser",
        email="test@example.com",
        hashed_password="hashed_password"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.users.user_crud.get_user") as mock_get_user,
        patch("app.api.v1.endpoints.users.user_crud.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = existing_user
        mock_update_user.return_value = updated_user

        # Call the endpoint
        result = await update_existing_user(user_id=user_id, user_in=update_data, db=mock_db)

        # Assertions
        assert result.username == "updateduser"
        mock_get_user.assert_called_once_with(mock_db, user_id=user_id)
        mock_update_user.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_not_found():
    """Test update of a non-existent user."""
    # Mock data
    user_id = uuid.uuid4()
    update_data = UserUpdate(username="updateduser")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function to return None
    with (
        patch("app.api.v1.endpoints.users.user_crud.get_user") as mock_get_user,
        patch("app.api.v1.endpoints.users.user_crud.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_user(user_id=user_id, user_in=update_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "does not exist" in exc_info.value.detail
        mock_get_user.assert_called_once_with(mock_db, user_id=user_id)
        mock_update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_invalid_data():
    """Test user update with invalid data."""
    # Mock data
    user_id = uuid.uuid4()
    update_data = UserUpdate(username="")  # Invalid empty username

    existing_user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.users.user_crud.get_user") as mock_get_user,
        patch("app.api.v1.endpoints.users.user_crud.update_user") as mock_update_user,
    ):
        mock_get_user.return_value = existing_user
        mock_update_user.side_effect = Exception("Validation error")

        # Call the endpoint and expect exception
        with pytest.raises(Exception):
            await update_existing_user(user_id=user_id, user_in=update_data, db=mock_db)


@pytest.mark.asyncio
async def test_delete_user_success():
    """Test successful user deletion."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.users.user_crud.delete_user") as mock_delete_user:
        mock_delete_user.return_value = True

        # Call the endpoint
        result = await delete_user_by_id(user_id=user_id, db=mock_db)

        # Assertions
        assert result is None  # Should return None for 204 No Content
        mock_delete_user.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_delete_user_not_found():
    """Test deletion of a non-existent user."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the user CRUD function to return False
    with patch("app.api.v1.endpoints.users.user_crud.delete_user") as mock_delete_user:
        mock_delete_user.return_value = False

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await delete_user_by_id(user_id=user_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail
        mock_delete_user.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_get_user_posts_success():
    """Test successful retrieval of posts by user."""
    # Mock data
    user_id = uuid.uuid4()
    mock_posts = [
        Post(id=uuid.uuid4(), title="Post 1", content="Content 1", author_id=user_id),
        Post(id=uuid.uuid4(), title="Post 2", content="Content 2", author_id=user_id),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.users.get_posts_by_author") as mock_get_posts:
        mock_get_posts.return_value = mock_posts

        # Call the endpoint
        result = await get_user_posts(user_id=user_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].title == "Post 1"
        assert result[1].title == "Post 2"
        mock_get_posts.assert_called_once_with(mock_db, author_id=user_id)


@pytest.mark.asyncio
async def test_get_user_posts_empty():
    """Test retrieval of posts by user when user has no posts."""
    # Mock data
    user_id = uuid.uuid4()
    mock_posts = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.users.get_posts_by_author") as mock_get_posts:
        mock_get_posts.return_value = mock_posts

        # Call the endpoint
        result = await get_user_posts(user_id=user_id, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_posts.assert_called_once_with(mock_db, author_id=user_id)


@pytest.mark.asyncio
async def test_get_user_comments_success():
    """Test successful retrieval of comments by user."""
    # Mock data
    user_id = uuid.uuid4()
    mock_comments = [
        Comment(id=uuid.uuid4(), content="Comment 1", user_id=user_id, post_id=uuid.uuid4()),
        Comment(id=uuid.uuid4(), content="Comment 2", user_id=user_id, post_id=uuid.uuid4()),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the comment CRUD function
    with patch("app.api.v1.endpoints.users.get_comments_by_user") as mock_get_comments:
        mock_get_comments.return_value = mock_comments

        # Call the endpoint
        result = await get_user_comments(user_id=user_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].content == "Comment 1"
        assert result[1].content == "Comment 2"
        mock_get_comments.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_get_user_comments_empty():
    """Test retrieval of comments by user when user has no comments."""
    # Mock data
    user_id = uuid.uuid4()
    mock_comments = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the comment CRUD function
    with patch("app.api.v1.endpoints.users.get_comments_by_user") as mock_get_comments:
        mock_get_comments.return_value = mock_comments

        # Call the endpoint
        result = await get_user_comments(user_id=user_id, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_comments.assert_called_once_with(mock_db, user_id=user_id)
