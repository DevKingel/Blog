import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app
from app.models.post import Post
from app.models.stat import Stat
from app.models.user import User

client = TestClient(app)


@pytest.fixture
async def db_session() -> Generator[AsyncSession]:
    """Create a database session for testing."""
    async with get_session() as session:
        yield session


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    # Check if user already exists
    result = await db_session.execute(select(User).where(User.username == "test_user_stats"))
    user = result.scalar_one_or_none()

    if not user:
        # Create a test user
        user = User(
            id=uuid.uuid4(),
            username="test_user_stats",
            email="test_stats@example.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

    return user


@pytest.fixture
async def test_post(db_session: AsyncSession, test_user: User) -> Post:
    """Create a test post."""
    # Check if post already exists
    result = await db_session.execute(select(Post).where(Post.title == "Test Post for Stats"))
    post = result.scalar_one_or_none()

    if not post:
        # Create a test post
        post = Post(
            id=uuid.uuid4(),
            title="Test Post for Stats",
            content="Content for test post used in stats testing",
            author_id=test_user.id,
        )
        db_session.add(post)
        await db_session.commit()
        await db_session.refresh(post)

    return post


@pytest.fixture
async def test_stat(db_session: AsyncSession, test_post: Post) -> Stat:
    """Create a test stat."""
    # Check if stat already exists
    result = await db_session.execute(select(Stat).where(Stat.post_id == test_post.id))
    stat = result.scalar_one_or_none()

    if not stat:
        # Create a test stat
        stat = Stat(
            id=uuid.uuid4(),
            post_id=test_post.id,
            views=10,
            likes=5,
        )
        db_session.add(stat)
        await db_session.commit()
        await db_session.refresh(stat)

    return stat


# Integration tests for GET /stats/posts/{post_id} - Get statistics for a specific post
def test_get_post_statistics_success(test_stat: Stat):
    """Test successful retrieval of post statistics."""
    response = client.get(f"/api/v1/stats/posts/{test_stat.post_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["post_id"] == str(test_stat.post_id)
    assert data["views"] == 10
    assert data["likes"] == 5


def test_get_post_statistics_not_found():
    """Test retrieval of post statistics when post is not found."""
    fake_post_id = uuid.uuid4()
    response = client.get(f"/api/v1/stats/posts/{fake_post_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# Integration tests for GET /stats/users/{user_id} - Get statistics for a specific user
def test_get_user_statistics_success(test_user: User, test_post: Post, test_stat: Stat):
    """Test successful retrieval of user statistics."""
    response = client.get(f"/api/v1/stats/users/{test_user.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == str(test_user.id)
    assert data["total_posts"] == 1
    assert data["total_views"] == 10
    assert data["total_likes"] == 5


def test_get_user_statistics_not_found():
    """Test retrieval of user statistics when user is not found."""
    fake_user_id = uuid.uuid4()
    response = client.get(f"/api/v1/stats/users/{fake_user_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# Integration tests for GET /stats/site - Get overall site statistics
def test_get_site_statistics_success(test_user: User, test_post: Post, test_stat: Stat):
    """Test successful retrieval of site statistics."""
    response = client.get("/api/v1/stats/site")
    assert response.status_code == 200

    data = response.json()
    assert "total_posts" in data
    assert "total_users" in data
    assert "total_views" in data
    assert "total_likes" in data
    # Note: Actual values will depend on the state of the test database


# Integration tests for POST /stats/posts/{post_id}/view - Record a post view
def test_record_post_view_success(test_stat: Stat):
    """Test successful recording of a post view."""
    response = client.post(f"/api/v1/stats/posts/{test_stat.post_id}/view")
    assert response.status_code == 201

    data = response.json()
    assert "message" in data
    assert "views" in data
    assert data["views"] >= test_stat.views  # Should be incremented


def test_record_post_view_not_found():
    """Test recording of a post view when post is not found."""
    fake_post_id = uuid.uuid4()
    response = client.post(f"/api/v1/stats/posts/{fake_post_id}/view")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# Integration tests for POST /stats/posts/{post_id}/like - Record a post like
def test_record_post_like_success(test_stat: Stat):
    """Test successful recording of a post like."""
    response = client.post(f"/api/v1/stats/posts/{test_stat.post_id}/like")
    assert response.status_code == 201

    data = response.json()
    assert "message" in data
    assert "likes" in data
    assert data["likes"] >= test_stat.likes  # Should be incremented


def test_record_post_like_not_found():
    """Test recording of a post like when post is not found."""
    fake_post_id = uuid.uuid4()
    response = client.post(f"/api/v1/stats/posts/{fake_post_id}/like")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# Integration tests for DELETE /stats/posts/{post_id}/like - Remove a post like
def test_remove_post_like_success(test_stat: Stat):
    """Test successful removal of a post like."""
    # First ensure there's at least one like to remove
    client.post(f"/api/v1/stats/posts/{test_stat.post_id}/like")

    response = client.delete(f"/api/v1/stats/posts/{test_stat.post_id}/like")
    assert response.status_code == 204
    assert response.content == b''  # Empty response body


def test_remove_post_like_not_found():
    """Test removal of a post like when post is not found."""
    fake_post_id = uuid.uuid4()
    response = client.delete(f"/api/v1/stats/posts/{fake_post_id}/like")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
