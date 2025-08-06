import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.stats import (
    get_post_statistics,
    get_site_statistics,
    get_user_statistics,
    record_post_like,
    record_post_view,
    remove_post_like,
)
from app.models.stat import Stat
from app.schemas.stat import PostStatsRead, SiteStatsRead, UserStatsRead


@pytest.mark.asyncio
async def test_get_post_statistics_success():
    """Test successful retrieval of post statistics."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(
        id=uuid.uuid4(),
        post_id=post_id,
        views=10,
        likes=5
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.return_value = mock_stat

        # Call the endpoint
        result = await get_post_statistics(post_id=post_id, db=mock_db)

        # Assertions
        assert isinstance(result, PostStatsRead)
        assert result.post_id == post_id
        assert result.views == 10
        assert result.likes == 5
        mock_get_stat.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_get_post_statistics_not_found():
    """Test retrieval of post statistics when post is not found."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.stats.stat_crud.get_stat_by_post_id") as mock_get_stat:
        mock_get_stat.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stat not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_post_statistics(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Stat not found"


@pytest.mark.asyncio
async def test_get_user_statistics_success():
    """Test successful retrieval of user statistics."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user_stats = {
        "user_id": user_id,
        "total_posts": 5,
        "total_views": 100,
        "total_likes": 50
    }

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.get_user_stats") as mock_get_user_stats:
        mock_get_user_stats.return_value = mock_user_stats

        # Call the endpoint
        result = await get_user_statistics(user_id=user_id, db=mock_db)

        # Assertions
        assert isinstance(result, UserStatsRead)
        assert result.user_id == user_id
        assert result.total_posts == 5
        assert result.total_views == 100
        assert result.total_likes == 50
        mock_get_user_stats.assert_called_once_with(mock_db, user_id=user_id)


@pytest.mark.asyncio
async def test_get_user_statistics_not_found():
    """Test retrieval of user statistics when user is not found."""
    # Mock data
    user_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.stats.stat_crud.get_user_stats") as mock_get_user_stats:
        mock_get_user_stats.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_user_statistics(user_id=user_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_get_site_statistics_success():
    """Test successful retrieval of site statistics."""
    # Mock data
    mock_site_stats = {
        "total_posts": 100,
        "total_users": 50,
        "total_views": 1000,
        "total_likes": 500
    }

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.get_site_stats") as mock_get_site_stats:
        mock_get_site_stats.return_value = mock_site_stats

        # Call the endpoint
        result = await get_site_statistics(db=mock_db)

        # Assertions
        assert isinstance(result, SiteStatsRead)
        assert result.total_posts == 100
        assert result.total_users == 50
        assert result.total_views == 1000
        assert result.total_likes == 500
        mock_get_site_stats.assert_called_once_with(mock_db)


@pytest.mark.asyncio
async def test_record_post_view_success():
    """Test successful recording of a post view."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(
        id=uuid.uuid4(),
        post_id=post_id,
        views=11,  # Incremented from 10 to 11
        likes=5
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.increment_post_views") as mock_increment_views:
        mock_increment_views.return_value = mock_stat

        # Call the endpoint
        result = await record_post_view(post_id=post_id, db=mock_db)

        # Assertions
        assert result["message"] == "View recorded successfully"
        assert result["views"] == 11
        mock_increment_views.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_record_post_view_not_found():
    """Test recording of a post view when post is not found."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.stats.stat_crud.increment_post_views") as mock_increment_views:
        mock_increment_views.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stat not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await record_post_view(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Stat not found"


@pytest.mark.asyncio
async def test_record_post_like_success():
    """Test successful recording of a post like."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(
        id=uuid.uuid4(),
        post_id=post_id,
        views=10,
        likes=6  # Incremented from 5 to 6
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.increment_post_likes") as mock_increment_likes:
        mock_increment_likes.return_value = mock_stat

        # Call the endpoint
        result = await record_post_like(post_id=post_id, db=mock_db)

        # Assertions
        assert result["message"] == "Like recorded successfully"
        assert result["likes"] == 6
        mock_increment_likes.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_record_post_like_not_found():
    """Test recording of a post like when post is not found."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.stats.stat_crud.increment_post_likes") as mock_increment_likes:
        mock_increment_likes.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stat not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await record_post_like(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Stat not found"


@pytest.mark.asyncio
async def test_remove_post_like_success():
    """Test successful removal of a post like."""
    # Mock data
    post_id = uuid.uuid4()
    mock_stat = Stat(
        id=uuid.uuid4(),
        post_id=post_id,
        views=10,
        likes=4  # Decremented from 5 to 4
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function
    with patch("app.api.v1.endpoints.stats.stat_crud.decrement_post_likes") as mock_decrement_likes:
        mock_decrement_likes.return_value = mock_stat

        # Call the endpoint
        result = await remove_post_like(post_id=post_id, db=mock_db)

        # Assertions
        assert result is None
        mock_decrement_likes.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_remove_post_like_not_found():
    """Test removal of a post like when post is not found."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the stat CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.stats.stat_crud.decrement_post_likes") as mock_decrement_likes:
        mock_decrement_likes.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stat not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await remove_post_like(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Stat not found"
