import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app
from app.models.category import Category
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User

client = TestClient(app)


@pytest.fixture
async def db_session() -> Generator[AsyncSession]:
    """Create a database session for testing."""
    async with get_session() as session:
        yield session


@pytest.fixture
async def test_posts(db_session: AsyncSession) -> list[Post]:
    """Create multiple test posts."""
    posts = []
    for i in range(3):
        # Check if post already exists
        result = await db_session.execute(select(Post).where(Post.title == f"Test Post {i}"))
        post = result.scalar_one_or_none()

        if not post:
            post = Post(
                id=uuid.uuid4(),
                title=f"Test Post {i}",
                content=f"Content for test post {i} with some unique text",
                author_id=uuid.uuid4(),  # Using a fake author ID for testing
                category_id=uuid.uuid4(),  # Using a fake category ID for testing
                slug=f"test-post-{i}",
                is_published=True,
            )
            db_session.add(post)
            posts.append(post)

    if posts:
        await db_session.commit()
        # Refresh all posts to get their IDs
        for post in posts:
            await db_session.refresh(post)

    # Get all test posts
    result = await db_session.execute(select(Post).where(Post.title.like("Test Post %")))
    return list(result.scalars().all())


@pytest.fixture
async def test_users(db_session: AsyncSession) -> list[User]:
    """Create multiple test users."""
    users = []
    for i in range(3):
        # Check if user already exists
        result = await db_session.execute(
            select(User).where(User.username == f"test_user_{i}")
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                id=uuid.uuid4(),
                username=f"test_user_{i}",
                email=f"user{i}@example.com",
                hashed_password="hashed_password",
            )
            db_session.add(user)
            users.append(user)

    if users:
        await db_session.commit()
        # Refresh all users to get their IDs
        for user in users:
            await db_session.refresh(user)

    # Get all test users
    result = await db_session.execute(select(User).where(User.username.like("test_user_%")))
    return list(result.scalars().all())


@pytest.fixture
async def test_categories(db_session: AsyncSession) -> list[Category]:
    """Create multiple test categories."""
    categories = []
    for i in range(3):
        # Check if category already exists
        result = await db_session.execute(
            select(Category).where(Category.name == f"Test Category {i}")
        )
        category = result.scalar_one_or_none()

        if not category:
            category = Category(
                id=uuid.uuid4(),
                name=f"Test Category {i}",
                slug=f"test-category-{i}",
            )
            db_session.add(category)
            categories.append(category)

    if categories:
        await db_session.commit()
        # Refresh all categories to get their IDs
        for category in categories:
            await db_session.refresh(category)

    # Get all test categories
    result = await db_session.execute(
        select(Category).where(Category.name.like("Test Category %"))
    )
    return list(result.scalars().all())


@pytest.fixture
async def test_tags(db_session: AsyncSession) -> list[Tag]:
    """Create multiple test tags."""
    tags = []
    for i in range(3):
        # Check if tag already exists
        result = await db_session.execute(select(Tag).where(Tag.name == f"Test Tag {i}"))
        tag = result.scalar_one_or_none()

        if not tag:
            tag = Tag(
                id=uuid.uuid4(),
                name=f"Test Tag {i}",
                slug=f"test-tag-{i}",
            )
            db_session.add(tag)
            tags.append(tag)

    if tags:
        await db_session.commit()
        # Refresh all tags to get their IDs
        for tag in tags:
            await db_session.refresh(tag)

    # Get all test tags
    result = await db_session.execute(select(Tag).where(Tag.name.like("Test Tag %")))
    return list(result.scalars().all())


# Integration tests for GET /search/posts
def test_search_posts_success(test_posts: list[Post]):
    """Test successful search of posts."""
    response = client.get("/api/v1/search/posts?query=Test")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert isinstance(data["posts"], list)
    assert isinstance(data["total"], int)


def test_search_posts_empty_results():
    """Test search of posts with no results."""
    response = client.get("/api/v1/search/posts?query=nonexistent")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert isinstance(data["posts"], list)
    assert len(data["posts"]) == 0
    assert data["total"] == 0


def test_search_posts_missing_query():
    """Test search of posts without query parameter."""
    response = client.get("/api/v1/search/posts")
    assert response.status_code == 422


def test_search_posts_short_query():
    """Test search of posts with query shorter than minimum length."""
    response = client.get("/api/v1/search/posts?query=")
    assert response.status_code == 422


def test_search_posts_pagination(test_posts: list[Post]):
    """Test search of posts with pagination."""
    response = client.get("/api/v1/search/posts?query=Test&skip=0&limit=2")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert isinstance(data["posts"], list)
    assert len(data["posts"]) <= 2
    assert isinstance(data["total"], int)


# Integration tests for GET /search/users
def test_search_users_success(test_users: list[User]):
    """Test successful search of users."""
    response = client.get("/api/v1/search/users?query=test")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert isinstance(data["users"], list)
    assert isinstance(data["total"], int)


def test_search_users_empty_results():
    """Test search of users with no results."""
    response = client.get("/api/v1/search/users?query=nonexistent")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) == 0
    assert data["total"] == 0


def test_search_users_missing_query():
    """Test search of users without query parameter."""
    response = client.get("/api/v1/search/users")
    assert response.status_code == 422


def test_search_users_short_query():
    """Test search of users with query shorter than minimum length."""
    response = client.get("/api/v1/search/users?query=")
    assert response.status_code == 422


def test_search_users_pagination(test_users: list[User]):
    """Test search of users with pagination."""
    response = client.get("/api/v1/search/users?query=test&skip=0&limit=2")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) <= 2
    assert isinstance(data["total"], int)


# Integration tests for GET /search/categories
def test_search_categories_success(test_categories: list[Category]):
    """Test successful search of categories."""
    response = client.get("/api/v1/search/categories?query=Test")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "categories" in data
    assert "total" in data
    assert isinstance(data["categories"], list)
    assert isinstance(data["total"], int)


def test_search_categories_empty_results():
    """Test search of categories with no results."""
    response = client.get("/api/v1/search/categories?query=nonexistent")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "categories" in data
    assert "total" in data
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) == 0
    assert data["total"] == 0


def test_search_categories_missing_query():
    """Test search of categories without query parameter."""
    response = client.get("/api/v1/search/categories")
    assert response.status_code == 422


def test_search_categories_short_query():
    """Test search of categories with query shorter than minimum length."""
    response = client.get("/api/v1/search/categories?query=")
    assert response.status_code == 422


def test_search_categories_pagination(test_categories: list[Category]):
    """Test search of categories with pagination."""
    response = client.get("/api/v1/search/categories?query=Test&skip=0&limit=2")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "categories" in data
    assert "total" in data
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) <= 2
    assert isinstance(data["total"], int)


# Integration tests for GET /search/tags
def test_search_tags_success(test_tags: list[Tag]):
    """Test successful search of tags."""
    response = client.get("/api/v1/search/tags?query=Test")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "tags" in data
    assert "total" in data
    assert isinstance(data["tags"], list)
    assert isinstance(data["total"], int)


def test_search_tags_empty_results():
    """Test search of tags with no results."""
    response = client.get("/api/v1/search/tags?query=nonexistent")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "tags" in data
    assert "total" in data
    assert isinstance(data["tags"], list)
    assert len(data["tags"]) == 0
    assert data["total"] == 0


def test_search_tags_missing_query():
    """Test search of tags without query parameter."""
    response = client.get("/api/v1/search/tags")
    assert response.status_code == 422


def test_search_tags_short_query():
    """Test search of tags with query shorter than minimum length."""
    response = client.get("/api/v1/search/tags?query=")
    assert response.status_code == 422


def test_search_tags_pagination(test_tags: list[Tag]):
    """Test search of tags with pagination."""
    response = client.get("/api/v1/search/tags?query=Test&skip=0&limit=2")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "tags" in data
    assert "total" in data
    assert isinstance(data["tags"], list)
    assert len(data["tags"]) <= 2
    assert isinstance(data["total"], int)
