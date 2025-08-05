import uuid
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.search import (
    search_categories,
    search_posts,
    search_tags,
    search_users,
)
from app.models.category import Category
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.schemas.search import (
    CategorySearchResult,
    PostSearchResult,
    TagSearchResult,
    UserSearchResult,
)


@pytest.mark.asyncio
async def test_search_posts_success():
    """Test successful search of posts."""
    # Mock data
    mock_posts = [
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="test-post-1",
            title="Test Post 1",
            content="This is test post 1 content",
            is_published=True,
        ),
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="test-post-2",
            title="Test Post 2",
            content="This is test post 2 content",
            is_published=True,
        ),
    ]
    mock_total = 2

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.search.post_crud.search_posts") as mock_search_posts:
        mock_search_posts.return_value = (mock_posts, mock_total)

        # Call the endpoint
        result = await search_posts(query="test", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, PostSearchResult)
        assert len(result.posts) == 2
        assert result.total == 2
        mock_search_posts.assert_called_once_with(mock_db, query="test", skip=0, limit=100)


@pytest.mark.asyncio
async def test_search_posts_empty_results():
    """Test search of posts with no results."""
    # Mock data
    mock_posts = []
    mock_total = 0

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.search.post_crud.search_posts") as mock_search_posts:
        mock_search_posts.return_value = (mock_posts, mock_total)

        # Call the endpoint
        result = await search_posts(query="nonexistent", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, PostSearchResult)
        assert len(result.posts) == 0
        assert result.total == 0
        mock_search_posts.assert_called_once_with(
            mock_db, query="nonexistent", skip=0, limit=100
        )


@pytest.mark.asyncio
async def test_search_users_success():
    """Test successful search of users."""
    # Mock data
    mock_users = [
        User(
            id=uuid.uuid4(),
            username="testuser1",
            email="test1@example.com",
            hashed_password="hashed_password",
        ),
        User(
            id=uuid.uuid4(),
            username="testuser2",
            email="test2@example.com",
            hashed_password="hashed_password",
        ),
    ]
    mock_total = 2

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.search.user_crud.search_users") as mock_search_users:
        mock_search_users.return_value = (mock_users, mock_total)

        # Call the endpoint
        result = await search_users(query="test", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, UserSearchResult)
        assert len(result.users) == 2
        assert result.total == 2
        mock_search_users.assert_called_once_with(mock_db, query="test", skip=0, limit=100)


@pytest.mark.asyncio
async def test_search_users_empty_results():
    """Test search of users with no results."""
    # Mock data
    mock_users = []
    mock_total = 0

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the user CRUD function
    with patch("app.api.v1.endpoints.search.user_crud.search_users") as mock_search_users:
        mock_search_users.return_value = (mock_users, mock_total)

        # Call the endpoint
        result = await search_users(query="nonexistent", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, UserSearchResult)
        assert len(result.users) == 0
        assert result.total == 0
        mock_search_users.assert_called_once_with(
            mock_db, query="nonexistent", skip=0, limit=100
        )


@pytest.mark.asyncio
async def test_search_categories_success():
    """Test successful search of categories."""
    # Mock data
    mock_categories = [
        Category(
            id=uuid.uuid4(),
            name="Test Category 1",
            slug="test-category-1",
        ),
        Category(
            id=uuid.uuid4(),
            name="Test Category 2",
            slug="test-category-2",
        ),
    ]
    mock_total = 2

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.search.category_crud.search_categories"
    ) as mock_search_categories:
        mock_search_categories.return_value = (mock_categories, mock_total)

        # Call the endpoint
        result = await search_categories(query="test", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, CategorySearchResult)
        assert len(result.categories) == 2
        assert result.total == 2
        mock_search_categories.assert_called_once_with(
            mock_db, query="test", skip=0, limit=100
        )


@pytest.mark.asyncio
async def test_search_categories_empty_results():
    """Test search of categories with no results."""
    # Mock data
    mock_categories = []
    mock_total = 0

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.search.category_crud.search_categories"
    ) as mock_search_categories:
        mock_search_categories.return_value = (mock_categories, mock_total)

        # Call the endpoint
        result = await search_categories(query="nonexistent", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, CategorySearchResult)
        assert len(result.categories) == 0
        assert result.total == 0
        mock_search_categories.assert_called_once_with(
            mock_db, query="nonexistent", skip=0, limit=100
        )


@pytest.mark.asyncio
async def test_search_tags_success():
    """Test successful search of tags."""
    # Mock data
    mock_tags = [
        Tag(
            id=uuid.uuid4(),
            name="Test Tag 1",
            slug="test-tag-1",
        ),
        Tag(
            id=uuid.uuid4(),
            name="Test Tag 2",
            slug="test-tag-2",
        ),
    ]
    mock_total = 2

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch("app.api.v1.endpoints.search.tag_crud.search_tags") as mock_search_tags:
        mock_search_tags.return_value = (mock_tags, mock_total)

        # Call the endpoint
        result = await search_tags(query="test", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, TagSearchResult)
        assert len(result.tags) == 2
        assert result.total == 2
        mock_search_tags.assert_called_once_with(mock_db, query="test", skip=0, limit=100)


@pytest.mark.asyncio
async def test_search_tags_empty_results():
    """Test search of tags with no results."""
    # Mock data
    mock_tags = []
    mock_total = 0

    # Mock dependencies
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch("app.api.v1.endpoints.search.tag_crud.search_tags") as mock_search_tags:
        mock_search_tags.return_value = (mock_tags, mock_total)

        # Call the endpoint
        result = await search_tags(query="nonexistent", skip=0, limit=100, db=mock_db)

        # Assertions
        assert isinstance(result, TagSearchResult)
        assert len(result.tags) == 0
        assert result.total == 0
        mock_search_tags.assert_called_once_with(
            mock_db, query="nonexistent", skip=0, limit=100
        )
