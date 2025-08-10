import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.admin import (
    delete_any_post,
    delete_any_user,
    get_admin_statistics,
    list_all_posts,
    list_all_users,
)
from app.models.post import Post
from app.models.user import User
from app.schemas.admin import AdminStatsRead, PostListRead, UserListRead


@pytest.mark.asyncio
async def test_get_admin_statistics_success():
    """Test successful retrieval of admin statistics."""
    # Mock data
    mock_stats_data = {
        "total_users": 100,
        "total_posts": 50,
        "total_comments": 200,
        "total_categories": 10,
        "total_tags": 25,
        "total_media": 30,
        "total_roles": 3,
    }

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.admin.stat_crud.get_site_stats") as mock_get_stats:
        mock_get_stats.return_value = mock_stats_data

        # Call the endpoint
        result = await get_admin_statistics(db=mock_db, current_admin=mock_admin_user)

        # Assertions
        assert isinstance(result, AdminStatsRead)
        assert result.total_users == 100
        assert result.total_posts == 50
        assert result.total_comments == 200
        mock_get_stats.assert_called_once_with(mock_db)


@pytest.mark.asyncio
async def test_get_admin_statistics_db_error():
    """Test handling of database error in admin statistics."""
    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the stat CRUD function to raise an exception
    with patch("app.api.v1.endpoints.admin.stat_crud.get_site_stats") as mock_get_stats:
        mock_get_stats.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await get_admin_statistics(db=mock_db, current_admin=mock_admin_user)

        # Assertions
        assert exc_info.value.status_code == 500
        assert (
            exc_info.value.detail == "Internal server error while fetching statistics"
        )


@pytest.mark.asyncio
async def test_list_all_users_success():
    """Test successful listing of all users."""
    # Mock data
    mock_users = [
        User(id=uuid.uuid4(), username="user1", email="user1@example.com"),
        User(id=uuid.uuid4(), username="user2", email="user2@example.com"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.admin.user_crud.get_multi_user") as mock_get_users:
        mock_get_users.return_value = mock_users

        # Call the endpoint
        result = await list_all_users(
            skip=0, limit=100, db=mock_db, current_admin=mock_admin_user
        )

        # Assertions
        assert isinstance(result, UserListRead)
        assert len(result.users) == 2
        assert result.total == 2
        assert result.page == 1
        assert result.size == 2
        mock_get_users.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_list_all_users_with_pagination():
    """Test listing of all users with custom pagination."""
    # Mock data
    mock_users = [
        User(id=uuid.uuid4(), username="user1", email="user1@example.com"),
        User(id=uuid.uuid4(), username="user2", email="user2@example.com"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.admin.user_crud.get_multi_user") as mock_get_users:
        mock_get_users.return_value = mock_users

        # Call the endpoint with custom pagination
        result = await list_all_users(
            skip=10, limit=5, db=mock_db, current_admin=mock_admin_user
        )

        # Assertions
        assert isinstance(result, UserListRead)
        assert len(result.users) == 2
        assert result.page == 3  # (10 // 5) + 1
        mock_get_users.assert_called_once_with(mock_db, skip=10, limit=5)


@pytest.mark.asyncio
async def test_list_all_users_empty_result():
    """Test listing of all users when no users exist."""
    # Mock data
    mock_users = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.admin.user_crud.get_multi_user") as mock_get_users:
        mock_get_users.return_value = mock_users

        # Call the endpoint
        result = await list_all_users(db=mock_db, current_admin=mock_admin_user)

        # Assertions
        assert isinstance(result, UserListRead)
        assert len(result.users) == 0
        assert result.total == 0
        assert result.page == 1
        assert result.size == 0


@pytest.mark.asyncio
async def test_delete_any_user_success():
    """Test successful deletion of a user."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user = Mock(spec=User)
    mock_user.id = user_id

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)
    mock_admin_user.id = uuid.uuid4()  # Different ID from the user being deleted

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.admin.user_crud.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.admin.user_crud.delete_user") as mock_delete_user,
    ):
        mock_get_user.return_value = mock_user
        mock_delete_user.return_value = True

        # Call the endpoint
        result = await delete_any_user(
            user_id=user_id, db=mock_db, current_admin=mock_admin_user
        )

        # Assertions
        assert result is None
        mock_get_user.assert_called_once_with(mock_db, user_id)
        mock_delete_user.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_delete_any_user_not_found():
    """Test deletion of a non-existent user."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the user CRUD function to return None
    with patch("app.api.v1.endpoints.admin.user_crud.get_user_by_id") as mock_get_user:
        mock_get_user.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_any_user(
                user_id=user_id, db=mock_db, current_admin=mock_admin_user
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_delete_any_user_db_error():
    """Test handling of database error during user deletion."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user = Mock(spec=User)
    mock_user.id = user_id

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)
    mock_admin_user.id = uuid.uuid4()  # Different ID from the user being deleted

    # Mock the user CRUD functions
    with (
        patch("app.api.v1.endpoints.admin.user_crud.get_user_by_id") as mock_get_user,
        patch("app.api.v1.endpoints.admin.user_crud.delete_user") as mock_delete_user,
    ):
        mock_get_user.return_value = mock_user
        mock_delete_user.return_value = False  # Simulate database error

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_any_user(
                user_id=user_id, db=mock_db, current_admin=mock_admin_user
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_delete_any_user_self_deletion_forbidden():
    """Test that admin cannot delete themselves."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user = Mock(spec=User)
    mock_user.id = user_id

    # Mock dependencies - same ID for both user and admin
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)
    mock_admin_user.id = user_id  # Same ID as the user being deleted

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.admin.user_crud.get_user_by_id") as mock_get_user:
        mock_get_user.return_value = mock_user

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_any_user(
                user_id=user_id, db=mock_db, current_admin=mock_admin_user
            )

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "You cannot delete yourself"


@pytest.mark.asyncio
async def test_list_all_posts_success():
    """Test successful listing of all posts."""
    # Mock data
    mock_posts = [
        Post(id=uuid.uuid4(), title="Post 1", content="Content 1"),
        Post(id=uuid.uuid4(), title="Post 2", content="Content 2"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the database execute method
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await list_all_posts(
        skip=0, limit=100, db=mock_db, current_admin=mock_admin_user
    )

    # Assertions
    assert isinstance(result, PostListRead)
    assert len(result.posts) == 2
    assert result.total == 2
    assert result.page == 1
    assert result.size == 2
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_list_all_posts_with_pagination():
    """Test listing of all posts with custom pagination."""
    # Mock data
    mock_posts = [
        Post(id=uuid.uuid4(), title="Post 1", content="Content 1"),
        Post(id=uuid.uuid4(), title="Post 2", content="Content 2"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the database execute method
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint with custom pagination
    result = await list_all_posts(
        skip=10, limit=5, db=mock_db, current_admin=mock_admin_user
    )

    # Assertions
    assert isinstance(result, PostListRead)
    assert len(result.posts) == 2
    assert result.page == 3  # (10 // 5) + 1
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_list_all_posts_empty_result():
    """Test listing of all posts when no posts exist."""
    # Mock data
    mock_posts = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the database execute method
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await list_all_posts(db=mock_db, current_admin=mock_admin_user)

    # Assertions
    assert isinstance(result, PostListRead)
    assert len(result.posts) == 0
    assert result.total == 0
    assert result.page == 1
    assert result.size == 0


@pytest.mark.asyncio
async def test_delete_any_post_success():
    """Test successful deletion of a post."""
    # Mock data
    post_id = uuid.uuid4()
    mock_post = Mock(spec=Post)
    mock_post.id = post_id

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the post CRUD functions
    with (
        patch("app.api.v1.endpoints.admin.post_crud.get_post_by_id") as mock_get_post,
        patch("app.api.v1.endpoints.admin.post_crud.delete_post") as mock_delete_post,
    ):
        mock_get_post.return_value = mock_post
        mock_delete_post.return_value = True

        # Call the endpoint
        result = await delete_any_post(
            post_id=post_id, db=mock_db, current_admin=mock_admin_user
        )

        # Assertions
        assert result is None
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_delete_post.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_delete_any_post_not_found():
    """Test deletion of a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the post CRUD function to return None
    with patch("app.api.v1.endpoints.admin.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_any_post(
                post_id=post_id, db=mock_db, current_admin=mock_admin_user
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Post not found"


@pytest.mark.asyncio
async def test_delete_any_post_db_error():
    """Test handling of database error during post deletion."""
    # Mock data
    post_id = uuid.uuid4()
    mock_post = Mock(spec=Post)
    mock_post.id = post_id

    # Mock dependencies
    mock_db = AsyncMock()
    mock_admin_user = Mock(spec=User)

    # Mock the post CRUD functions
    with (
        patch("app.api.v1.endpoints.admin.post_crud.get_post_by_id") as mock_get_post,
        patch("app.api.v1.endpoints.admin.post_crud.delete_post") as mock_delete_post,
    ):
        mock_get_post.return_value = mock_post
        mock_delete_post.return_value = False  # Simulate database error

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_any_post(
                post_id=post_id, db=mock_db, current_admin=mock_admin_user
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Post not found"
