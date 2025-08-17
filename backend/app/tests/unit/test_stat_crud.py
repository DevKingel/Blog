import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from app.crud.stat import (
    create_stat,
    decrement_post_likes,
    delete_stat,
    get_all_stats,
    get_site_stats,
    get_stat_by_id,
    get_stat_by_post_id,
    get_user_stats,
    increment_post_likes,
    increment_post_views,
    update_stat,
)
from app.models.post import Post
from app.models.stat import Stat
from app.models.user import User


@pytest.mark.asyncio
async def test_create_stat_success():
    """Test successful creation of a new stat record."""
    # Mock data
    stat_data = {"post_id": uuid.uuid4(), "views": 0, "likes": 0}

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock database session operations
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await create_stat(stat_data, mock_db)

    # Assertions
    assert isinstance(result, Stat)
    assert result.post_id == stat_data["post_id"]
    assert result.views == stat_data["views"]
    assert result.likes == stat_data["likes"]
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_stat_db_error():
    """Test handling of database error during stat creation."""
    # Mock data
    stat_data = {"post_id": uuid.uuid4(), "views": 0, "likes": 0}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await create_stat(stat_data, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_stat_by_id_success():
    """Test successful retrieval of a stat by ID."""
    # Mock data
    stat_id = uuid.uuid4()
    mock_stat = Stat(id=stat_id, post_id=uuid.uuid4(), views=10, likes=5)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_stat
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_stat_by_id(stat_id, mock_db)

    # Assertions
    assert isinstance(result, Stat)
    assert result.id == stat_id
    assert result.views == 10
    assert result.likes == 5
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_stat_by_id_not_found():
    """Test retrieval of a stat by ID when not found."""
    # Mock data
    stat_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await get_stat_by_id(stat_id, mock_db)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Stat not found"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_stat_by_post_id_success():
    """Test successful retrieval of a stat by post ID."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(id=uuid.uuid4(), post_id=post_id, views=10, likes=5)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_stat
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_stat_by_post_id(post_id, mock_db)

    # Assertions
    assert isinstance(result, Stat)
    assert result.post_id == post_id
    assert result.views == 10
    assert result.likes == 5
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_stat_by_post_id_not_found():
    """Test retrieval of a stat by post ID when not found (creates new stat)."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Mock the create_stat function
    with patch("app.crud.stat.create_stat") as mock_create_stat:
        mock_create_stat.return_value = Stat(
            id=uuid.uuid4(), post_id=post_id, views=0, likes=0
        )

        # Call the function
        result = await get_stat_by_post_id(post_id, mock_db)

        # Assertions
        assert isinstance(result, Stat)
        assert result.post_id == post_id
        assert result.views == 0
        assert result.likes == 0
        mock_db.execute.assert_called_once()
        mock_create_stat.assert_called_once_with({"post_id": post_id}, mock_db)


@pytest.mark.asyncio
async def test_get_all_stats_success():
    """Test successful retrieval of all stats."""
    # Mock data
    mock_stats = [
        Stat(id=uuid.uuid4(), post_id=uuid.uuid4(), views=10, likes=5),
        Stat(id=uuid.uuid4(), post_id=uuid.uuid4(), views=20, likes=15),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_stats
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_stats(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(stat, Stat) for stat in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_stats_empty_result():
    """Test retrieval of all stats when no stats exist."""
    # Mock data
    mock_stats = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_stats
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_stats(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_stat_success():
    """Test successful update of a stat record."""
    # Mock data
    stat_id = uuid.uuid4()
    stat_data = {"views": 15, "likes": 8}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_stat = Stat(id=stat_id, post_id=uuid.uuid4(), views=10, likes=5)
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_existing_stat
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_stat(stat_id, stat_data, mock_db)

    # Assertions
    assert isinstance(result, Stat)
    assert result.views == 15
    assert result.likes == 8
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_stat_not_found():
    """Test update of a non-existent stat record."""
    # Mock data
    stat_id = uuid.uuid4()
    stat_data = {"views": 15, "likes": 8}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await update_stat(stat_id, stat_data, mock_db)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Stat not found"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_stat_partial_data():
    """Test update of a stat record with partial data."""
    # Mock data
    stat_id = uuid.uuid4()
    stat_data = {
        "views": 15
        # likes not provided, should remain unchanged
    }

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_stat = Stat(id=stat_id, post_id=uuid.uuid4(), views=10, likes=5)
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_existing_stat
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_stat(stat_id, stat_data, mock_db)

    # Assertions
    assert isinstance(result, Stat)
    assert result.views == 15
    assert result.likes == 5  # Should remain unchanged
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_stat_success():
    """Test successful deletion of a stat record."""
    # Mock data
    stat_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_stat = Stat(id=stat_id, post_id=uuid.uuid4(), views=10, likes=5)
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_stat
    mock_db.execute.return_value = mock_result
    mock_db.delete = AsyncMock()  # Changed to AsyncMock
    mock_db.commit = AsyncMock()

    # Call the function
    result = await delete_stat(stat_id, mock_db)

    # Assertions
    assert result is None
    mock_db.execute.assert_called_once()
    mock_db.delete.assert_awaited_once_with(mock_stat)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_stat_not_found():
    """Test deletion of a non-existent stat record."""
    # Mock data
    stat_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await delete_stat(stat_id, mock_db)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Stat not found"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_increment_post_views_success():
    """Test successful increment of post views."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(id=uuid.uuid4(), post_id=post_id, views=10, likes=5)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Mock the get_stat_by_post_id function
    with patch("app.crud.stat.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.return_value = mock_stat

        # Call the function
        result = await increment_post_views(post_id, mock_db)

        # Assertions
        assert isinstance(result, Stat)
        assert result.views == 11  # Incremented from 10 to 11
        assert result.likes == 5  # Should remain unchanged
        mock_get_stat.assert_called_once_with(post_id, mock_db)
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_increment_post_likes_success():
    """Test successful increment of post likes."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(id=uuid.uuid4(), post_id=post_id, views=10, likes=5)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Mock the get_stat_by_post_id function
    with patch("app.crud.stat.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.return_value = mock_stat

        # Call the function
        result = await increment_post_likes(post_id, mock_db)

        # Assertions
        assert isinstance(result, Stat)
        assert result.views == 10  # Should remain unchanged
        assert result.likes == 6  # Incremented from 5 to 6
        mock_get_stat.assert_called_once_with(post_id, mock_db)
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_decrement_post_likes_success():
    """Test successful decrement of post likes."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(id=uuid.uuid4(), post_id=post_id, views=10, likes=5)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Mock the get_stat_by_post_id function
    with patch("app.crud.stat.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.return_value = mock_stat

        # Call the function
        result = await decrement_post_likes(post_id, mock_db)

        # Assertions
        assert isinstance(result, Stat)
        assert result.views == 10  # Should remain unchanged
        assert result.likes == 4  # Decremented from 5 to 4
        mock_get_stat.assert_called_once_with(post_id, mock_db)
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_decrement_post_likes_zero_likes():
    """Test decrement of post likes when likes are already zero."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(id=uuid.uuid4(), post_id=post_id, views=10, likes=0)

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Mock the get_stat_by_post_id function
    with patch("app.crud.stat.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.return_value = mock_stat

        # Call the function
        result = await decrement_post_likes(post_id, mock_db)

        # Assertions
        assert isinstance(result, Stat)
        assert result.views == 10  # Should remain unchanged
        assert result.likes == 0  # Should remain zero
        mock_get_stat.assert_called_once_with(post_id, mock_db)
        # commit and refresh should not be called when likes don't change
        mock_db.commit.assert_not_awaited()
        mock_db.refresh.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_site_stats_success():
    """Test successful retrieval of site statistics."""
    # Mock data
    mock_posts = [
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="post-1",
            title="Post 1",
            content="Content 1",
            is_published=True,
        ),
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="post-2",
            title="Post 2",
            content="Content 2",
            is_published=True,
        ),
    ]

    mock_users = [
        User(
            id=uuid.uuid4(),
            username="user1",
            email="user1@example.com",
            hashed_password="hashed_password_1",
        ),
        User(
            id=uuid.uuid4(),
            username="user2",
            email="user2@example.com",
            hashed_password="hashed_password_2",
        ),
        User(
            id=uuid.uuid4(),
            username="user3",
            email="user3@example.com",
            hashed_password="hashed_password_3",
        ),
    ]

    mock_stats = [
        Stat(id=uuid.uuid4(), post_id=mock_posts[0].id, views=10, likes=5),
        Stat(id=uuid.uuid4(), post_id=mock_posts[1].id, views=20, likes=15),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock results for posts query
    mock_posts_result = Mock()
    mock_posts_result.scalars.return_value.all.return_value = mock_posts

    # Mock results for users query
    mock_users_result = Mock()
    mock_users_result.scalars.return_value.all.return_value = mock_users

    # Mock results for stats query
    mock_stats_result = Mock()
    mock_stats_result.scalars.return_value.all.return_value = mock_stats

    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query):
        query_str = str(query)
        if "posts" in query_str:
            return mock_posts_result
        elif "users" in query_str:
            return mock_users_result
        elif "stats" in query_str:
            return mock_stats_result
        else:
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = []
            return mock_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result = await get_site_stats(mock_db)

    # Assertions
    assert isinstance(result, dict)
    assert result["total_posts"] == 2
    assert result["total_users"] == 3
    assert result["total_views"] == 30  # 10 + 20
    assert result["total_likes"] == 20  # 5 + 15


@pytest.mark.asyncio
async def test_get_site_stats_empty_data():
    """Test retrieval of site statistics when no data exists."""
    # Mock data
    mock_posts = []
    mock_users = []
    mock_stats = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock results for posts query
    mock_posts_result = Mock()
    mock_posts_result.scalars.return_value.all.return_value = mock_posts

    # Mock results for users query
    mock_users_result = Mock()
    mock_users_result.scalars.return_value.all.return_value = mock_users

    # Mock results for stats query
    mock_stats_result = Mock()
    mock_stats_result.scalars.return_value.all.return_value = mock_stats

    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query):
        query_str = str(query)
        if "posts" in query_str:
            return mock_posts_result
        elif "users" in query_str:
            return mock_users_result
        elif "stats" in query_str:
            return mock_stats_result
        else:
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = []
            return mock_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result = await get_site_stats(mock_db)

    # Assertions
    assert isinstance(result, dict)
    assert result["total_posts"] == 0
    assert result["total_users"] == 0
    assert result["total_views"] == 0
    assert result["total_likes"] == 0


@pytest.mark.asyncio
async def test_get_user_stats_success():
    """Test successful retrieval of user statistics."""
    # Mock data
    user_id = uuid.uuid4()

    mock_posts = [
        Post(
            id=uuid.uuid4(),
            author_id=user_id,
            category_id=uuid.uuid4(),
            slug="post-1",
            title="Post 1",
            content="Content 1",
            is_published=True,
        ),
        Post(
            id=uuid.uuid4(),
            author_id=user_id,
            category_id=uuid.uuid4(),
            slug="post-2",
            title="Post 2",
            content="Content 2",
            is_published=True,
        ),
    ]

    mock_stats = [
        Stat(id=uuid.uuid4(), post_id=mock_posts[0].id, views=10, likes=5),
        Stat(id=uuid.uuid4(), post_id=mock_posts[1].id, views=20, likes=15),
    ]

    # Mock dependencies
    mock_db = AsyncMock()

    # Create mock results
    mock_posts_result = Mock()
    mock_posts_result.scalars.return_value.all.return_value = mock_posts

    mock_stats_result = Mock()
    mock_stats_result.scalars.return_value.all.return_value = mock_stats

    # Set up the execute side effect to return the correct results
    call_count = 0

    async def execute_side_effect(query):
        nonlocal call_count
        call_count += 1

        # First call is for posts
        if call_count == 1:
            return mock_posts_result
        # Second call is for stats
        elif call_count == 2:
            return mock_stats_result
        else:
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = []
            return mock_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result = await get_user_stats(user_id, mock_db)

    # Assertions
    assert isinstance(result, dict)
    assert result["user_id"] == user_id
    assert result["total_posts"] == 2
    assert result["total_views"] == 30  # 10 + 20
    assert result["total_likes"] == 20  # 5 + 15


@pytest.mark.asyncio
async def test_get_user_stats_no_posts():
    """Test retrieval of user statistics when user has no posts."""
    # Mock data
    user_id = uuid.uuid4()
    mock_posts = []
    mock_stats = []

    # Mock dependencies
    mock_db = AsyncMock()

    # Create mock results
    mock_posts_result = Mock()
    mock_posts_result.scalars.return_value.all.return_value = mock_posts

    mock_stats_result = Mock()
    mock_stats_result.scalars.return_value.all.return_value = mock_stats

    # Set up the execute side effect to return the correct results
    call_count = 0

    async def execute_side_effect(query):
        nonlocal call_count
        call_count += 1

        # First call is for posts
        if call_count == 1:
            return mock_posts_result
        # Second call is for stats
        elif call_count == 2:
            return mock_stats_result
        else:
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = []
            return mock_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result = await get_user_stats(user_id, mock_db)

    # Assertions
    assert isinstance(result, dict)
    assert result["user_id"] == user_id
    assert result["total_posts"] == 0
    assert result["total_views"] == 0
    assert result["total_likes"] == 0
