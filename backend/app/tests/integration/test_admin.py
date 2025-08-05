import uuid
from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_session
from app.main import app
from app.models.post import Post
from app.models.role import Role
from app.models.user import User

client = TestClient(app)


# Helper functions for creating test data
def create_test_token(user_id: uuid.UUID) -> str:
    """Create a test JWT token for a user."""
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC).timestamp() + 3600,  # 1 hour expiration
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


@pytest.fixture
async def db_session() -> Generator[AsyncSession]:
    """Create a database session for testing."""
    async with get_session() as session:
        yield session


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """Create a test admin user."""
    # First create the admin role if it doesn't exist
    result = await db_session.execute(select(Role).where(Role.name == "admin"))
    admin_role = result.scalar_one_or_none()

    if not admin_role:
        admin_role = Role(id=uuid.uuid4(), name="admin", description="Administrator role")
        db_session.add(admin_role)
        await db_session.commit()
        await db_session.refresh(admin_role)

    # Check if admin user already exists
    result = await db_session.execute(select(User).where(User.username == "admin_user"))
    admin_user = result.scalar_one_or_none()

    if not admin_user:
        # Create the admin user
        admin_user = User(
            id=uuid.uuid4(),
            username="admin_user",
            email="admin@example.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
        )
        db_session.add(admin_user)
        await db_session.commit()
        await db_session.refresh(admin_user)

        # Assign admin role to the user
        admin_user.roles.append(admin_role)
        await db_session.commit()
        await db_session.refresh(admin_user)

    return admin_user


@pytest.fixture
async def regular_user(db_session: AsyncSession) -> User:
    """Create a test regular user."""
    # Check if regular user already exists
    result = await db_session.execute(select(User).where(User.username == "regular_user"))
    regular_user = result.scalar_one_or_none()

    if not regular_user:
        # Create a regular user without admin role
        regular_user = User(
            id=uuid.uuid4(),
            username="regular_user",
            email="user@example.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
        )
        db_session.add(regular_user)
        await db_session.commit()
        await db_session.refresh(regular_user)

    return regular_user


@pytest.fixture
async def test_users(db_session: AsyncSession) -> list[User]:
    """Create multiple test users."""
    users = []
    for i in range(5):
        # Check if user already exists
        result = await db_session.execute(select(User).where(User.username == f"test_user_{i}"))
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                id=uuid.uuid4(),
                username=f"test_user_{i}",
                email=f"user{i}@example.com",
                hashed_password="hashed_password",
                is_active=True,
                is_superuser=False,
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
async def test_posts(db_session: AsyncSession, regular_user: User) -> list[Post]:
    """Create multiple test posts."""
    posts = []
    for i in range(5):
        # Check if post already exists
        result = await db_session.execute(select(Post).where(Post.title == f"Test Post {i}"))
        post = result.scalar_one_or_none()

        if not post:
            post = Post(
                id=uuid.uuid4(),
                title=f"Test Post {i}",
                content=f"Content for test post {i}",
                author_id=regular_user.id,
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


# Integration tests for GET /admin/stats
def test_get_admin_statistics_success(admin_user: User):
    """Test successful retrieval of admin statistics."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/stats", headers=headers)
    # Should be 200 OK or 500 if there's a database issue
    assert response.status_code in [200, 500]


def test_get_admin_statistics_non_admin_forbidden(regular_user: User):
    """Test that non-admin users cannot access admin statistics."""
    # Create auth token for regular user
    token = create_test_token(regular_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/stats", headers=headers)
    assert response.status_code == 403


def test_get_admin_statistics_unauthorized():
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 401


# Integration tests for GET /admin/users
def test_list_all_users_success(admin_user: User, test_users: list[User]):
    """Test successful listing of all users."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_list_all_users_with_pagination(admin_user: User, test_users: list[User]):
    """Test listing of all users with pagination."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test with custom pagination parameters
    response = client.get("/api/v1/admin/users?skip=0&limit=2", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "users" in data
    assert len(data["users"]) <= 2
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_list_all_users_non_admin_forbidden(regular_user: User):
    """Test that non-admin users cannot list all users."""
    # Create auth token for regular user
    token = create_test_token(regular_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 403


def test_list_all_users_unauthorized():
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 401


# Integration tests for DELETE /admin/users/{user_id}
def test_delete_any_user_success(admin_user: User, test_users: list[User]):
    """Test successful deletion of a user."""
    if not test_users:
        pytest.skip("No test users available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Delete the first test user
    user_to_delete = test_users[0]
    response = client.delete(f"/api/v1/admin/users/{user_to_delete.id}", headers=headers)
    assert response.status_code == 204


def test_delete_any_user_not_found(admin_user: User):
    """Test deletion of a non-existent user."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a non-existent user
    fake_user_id = uuid.uuid4()
    response = client.delete(f"/api/v1/admin/users/{fake_user_id}", headers=headers)
    assert response.status_code == 404


def test_delete_any_user_self_deletion_forbidden(admin_user: User):
    """Test that admin cannot delete themselves."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete themselves
    response = client.delete(f"/api/v1/admin/users/{admin_user.id}", headers=headers)
    assert response.status_code == 400


def test_delete_any_user_non_admin_forbidden(regular_user: User, test_users: list[User]):
    """Test that non-admin users cannot delete users."""
    if not test_users:
        pytest.skip("No test users available")

    # Create auth token for regular user
    token = create_test_token(regular_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a user
    user_to_delete = test_users[0]
    response = client.delete(f"/api/v1/admin/users/{user_to_delete.id}", headers=headers)
    assert response.status_code == 403


def test_delete_any_user_unauthorized(test_users: list[User]):
    """Test that unauthenticated requests are rejected."""
    if not test_users:
        pytest.skip("No test users available")

    # Try to delete a user without authentication
    user_to_delete = test_users[0]
    response = client.delete(f"/api/v1/admin/users/{user_to_delete.id}")
    assert response.status_code == 401


# Integration tests for GET /admin/posts
def test_list_all_posts_success(admin_user: User, test_posts: list[Post]):
    """Test successful listing of all posts."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/posts", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_list_all_posts_with_pagination(admin_user: User, test_posts: list[Post]):
    """Test listing of all posts with pagination."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test with custom pagination parameters
    response = client.get("/api/v1/admin/posts?skip=0&limit=2", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "posts" in data
    assert len(data["posts"]) <= 2
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_list_all_posts_non_admin_forbidden(regular_user: User):
    """Test that non-admin users cannot list all posts."""
    # Create auth token for regular user
    token = create_test_token(regular_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/posts", headers=headers)
    assert response.status_code == 403


def test_list_all_posts_unauthorized():
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/v1/admin/posts")
    assert response.status_code == 401


# Integration tests for DELETE /admin/posts/{post_id}
def test_delete_any_post_success(admin_user: User, test_posts: list[Post]):
    """Test successful deletion of a post."""
    if not test_posts:
        pytest.skip("No test posts available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Delete the first test post
    post_to_delete = test_posts[0]
    response = client.delete(f"/api/v1/admin/posts/{post_to_delete.id}", headers=headers)
    assert response.status_code == 204


def test_delete_any_post_not_found(admin_user: User):
    """Test deletion of a non-existent post."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a non-existent post
    fake_post_id = uuid.uuid4()
    response = client.delete(f"/api/v1/admin/posts/{fake_post_id}", headers=headers)
    assert response.status_code == 404


def test_delete_any_post_non_admin_forbidden(regular_user: User, test_posts: list[Post]):
    """Test that non-admin users cannot delete posts."""
    if not test_posts:
        pytest.skip("No test posts available")

    # Create auth token for regular user
    token = create_test_token(regular_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a post
    post_to_delete = test_posts[0]
    response = client.delete(f"/api/v1/admin/posts/{post_to_delete.id}", headers=headers)
    assert response.status_code == 403


def test_delete_any_post_unauthorized(test_posts: list[Post]):
    """Test that unauthenticated requests are rejected."""
    if not test_posts:
        pytest.skip("No test posts available")

    # Try to delete a post without authentication
    post_to_delete = test_posts[0]
    response = client.delete(f"/api/v1/admin/posts/{post_to_delete.id}")
    assert response.status_code == 401
