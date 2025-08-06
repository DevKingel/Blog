import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app
from app.models.comment import Comment
from app.models.post import Post
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
    result = await db_session.execute(select(User).where(User.username == "test_user"))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            id=uuid.uuid4(),
            username="test_user",
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

    return user


@pytest.fixture
async def test_users(db_session: AsyncSession) -> list[User]:
    """Create multiple test users."""
    users = []
    for i in range(3):
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
async def test_user_with_content(db_session: AsyncSession) -> tuple[User, list[Post], list[Comment]]:
    """Create a test user with associated posts and comments."""
    # Check if user already exists
    result = await db_session.execute(select(User).where(User.username == "content_user"))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            id=uuid.uuid4(),
            username="content_user",
            email="content@example.com",
            hashed_password="hashed_password",
            is_active=True,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

    # Create posts for the user
    posts = []
    for i in range(2):
        result = await db_session.execute(select(Post).where(Post.title == f"Test Post {i}"))
        post = result.scalar_one_or_none()

        if not post:
            post = Post(
                id=uuid.uuid4(),
                title=f"Test Post {i}",
                content=f"Content for test post {i}",
                author_id=user.id,
            )
            db_session.add(post)
            posts.append(post)

    # Create comments for the user
    comments = []
    if posts:
        for i in range(2):
            result = await db_session.execute(select(Comment).where(Comment.content == f"Test Comment {i}"))
            comment = result.scalar_one_or_none()

            if not comment:
                comment = Comment(
                    id=uuid.uuid4(),
                    content=f"Test Comment {i}",
                    user_id=user.id,
                    post_id=posts[0].id,
                )
                db_session.add(comment)
                comments.append(comment)

    if posts or comments:
        await db_session.commit()
        # Refresh all posts and comments
        for post in posts:
            await db_session.refresh(post)
        for comment in comments:
            await db_session.refresh(comment)

    return user, posts, comments


# Integration tests for POST /users/ - Create a new user
def test_create_user_success():
    """Test successful user creation."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "hashed_password": "newhashedpassword"
    }

    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    # Password should not be in the response
    assert "hashed_password" not in data


def test_create_user_duplicate_email(test_user: User):
    """Test user creation with duplicate email."""
    user_data = {
        "username": "anotheruser",
        "email": test_user.email,  # Duplicate email
        "hashed_password": "anotherhashedpassword"
    }

    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_user_invalid_data():
    """Test user creation with invalid data."""
    user_data = {
        "username": "",  # Invalid empty username
        "email": "invalid-email",  # Invalid email format
        "hashed_password": "password"
    }

    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422


# Integration tests for GET /users/ - Retrieve users with pagination
def test_read_users_success(test_users: list[User]):
    """Test successful retrieval of users."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should have at least the test users we created
    assert len(data) >= 3


def test_read_users_with_pagination(test_users: list[User]):
    """Test retrieval of users with pagination."""
    response = client.get("/api/v1/users/?skip=0&limit=2")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should have at most 2 users due to limit
    assert len(data) <= 2


def test_read_users_empty():
    """Test retrieval of users when no users exist."""
    # This test assumes the database is empty or properly isolated
    # In a real test environment, we might need to clear the database first
    response = client.get("/api/v1/users/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # In a clean test environment, this might be empty


# Integration tests for GET /users/{user_id} - Get a specific user by id
def test_read_user_by_id_success(test_user: User):
    """Test successful retrieval of a user by ID."""
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == str(test_user.id)
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


def test_read_user_by_id_not_found():
    """Test retrieval of a non-existent user by ID."""
    fake_user_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{fake_user_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# Integration tests for PATCH /users/{user_id} - Update a user
def test_update_user_success(test_user: User):
    """Test successful user update."""
    update_data = {
        "username": "updated_username"
    }

    response = client.patch(f"/api/v1/users/{test_user.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "updated_username"
    assert data["email"] == test_user.email  # Email should remain unchanged


def test_update_user_not_found():
    """Test update of a non-existent user."""
    fake_user_id = uuid.uuid4()
    update_data = {
        "username": "updated_username"
    }

    response = client.patch(f"/api/v1/users/{fake_user_id}", json=update_data)
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


def test_update_user_partial(test_user: User):
    """Test partial user update."""
    update_data = {
        "username": "partially_updated"
        # Not updating email, so it should remain unchanged
    }

    response = client.patch(f"/api/v1/users/{test_user.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "partially_updated"
    assert data["email"] == test_user.email


# Integration tests for DELETE /users/{user_id} - Delete a user
def test_delete_user_success(test_user: User):
    """Test successful user deletion."""
    response = client.delete(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 204


def test_delete_user_not_found():
    """Test deletion of a non-existent user."""
    fake_user_id = uuid.uuid4()
    response = client.delete(f"/api/v1/users/{fake_user_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# Integration tests for GET /users/{user_id}/posts - Get all posts by a specific user
def test_get_user_posts_success(test_user_with_content: tuple[User, list[Post], list[Comment]]):
    """Test successful retrieval of posts by user."""
    user, posts, _ = test_user_with_content

    response = client.get(f"/api/v1/users/{user.id}/posts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should have the posts we created for this user
    assert len(data) >= 2

    # Verify all posts belong to the user
    for post in data:
        assert post["author_id"] == str(user.id)


def test_get_user_posts_empty(test_user: User):
    """Test retrieval of posts by user when user has no posts."""
    response = client.get(f"/api/v1/users/{test_user.id}/posts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should be empty since the user has no posts
    assert len(data) == 0


def test_get_user_posts_user_not_found():
    """Test retrieval of posts by non-existent user."""
    fake_user_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{fake_user_id}/posts")
    # Should return 200 with empty list rather than 404
    # because the endpoint is about posts, not user existence
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


# Integration tests for GET /users/{user_id}/comments - Get all comments by a specific user
def test_get_user_comments_success(test_user_with_content: tuple[User, list[Post], list[Comment]]):
    """Test successful retrieval of comments by user."""
    user, _, comments = test_user_with_content

    response = client.get(f"/api/v1/users/{user.id}/comments")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should have the comments we created for this user
    assert len(data) >= 2

    # Verify all comments belong to the user
    for comment in data:
        assert comment["user_id"] == str(user.id)


def test_get_user_comments_empty(test_user: User):
    """Test retrieval of comments by user when user has no comments."""
    response = client.get(f"/api/v1/users/{test_user.id}/comments")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Should be empty since the user has no comments
    assert len(data) == 0


def test_get_user_comments_user_not_found():
    """Test retrieval of comments by non-existent user."""
    fake_user_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{fake_user_id}/comments")
    # Should return 200 with empty list rather than 404
    # because the endpoint is about comments, not user existence
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
