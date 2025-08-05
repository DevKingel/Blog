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
from app.models.category import Category
from app.models.post import Post
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
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    # Check if test user already exists
    result = await db_session.execute(select(User).where(User.username == "test_user"))
    test_user = result.scalar_one_or_none()

    if not test_user:
        # Create a test user
        test_user = User(
            id=uuid.uuid4(),
            username="test_user",
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

    return test_user


@pytest.fixture
async def test_category(db_session: AsyncSession) -> Category:
    """Create a test category."""
    # Check if test category already exists
    result = await db_session.execute(select(Category).where(Category.name == "Test Category"))
    test_category = result.scalar_one_or_none()

    if not test_category:
        # Create a test category
        test_category = Category(
            id=uuid.uuid4(),
            name="Test Category",
            description="A test category",
        )
        db_session.add(test_category)
        await db_session.commit()
        await db_session.refresh(test_category)

    return test_category


@pytest.fixture
async def test_post(db_session: AsyncSession, test_user: User, test_category: Category) -> Post:
    """Create a test post."""
    # Check if test post already exists
    result = await db_session.execute(select(Post).where(Post.title == "Test Post"))
    test_post = result.scalar_one_or_none()

    if not test_post:
        # Create a test post
        test_post = Post(
            id=uuid.uuid4(),
            author_id=test_user.id,
            category_id=test_category.id,
            slug="test-post",
            title="Test Post",
            content="This is a test post",
            is_published=False,
        )
        db_session.add(test_post)
        await db_session.commit()
        await db_session.refresh(test_post)

    return test_post


@pytest.fixture
async def published_post(db_session: AsyncSession, test_user: User, test_category: Category) -> Post:
    """Create a published test post."""
    # Check if published post already exists
    result = await db_session.execute(select(Post).where(Post.title == "Published Post"))
    published_post = result.scalar_one_or_none()

    if not published_post:
        # Create a published test post
        published_post = Post(
            id=uuid.uuid4(),
            author_id=test_user.id,
            category_id=test_category.id,
            slug="published-post",
            title="Published Post",
            content="This is a published test post",
            is_published=True,
            published_at=datetime.utcnow(),
        )
        db_session.add(published_post)
        await db_session.commit()
        await db_session.refresh(published_post)

    return published_post


# Integration tests for POST / - Create a new post
def test_create_new_post_success(test_user: User, test_category: Category):
    """Test successful creation of a new post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Post data
    post_data = {
        "author_id": str(test_user.id),
        "category_id": str(test_category.id),
        "slug": "new-test-post",
        "title": "New Test Post",
        "content": "This is a new test post",
        "is_published": False,
    }

    response = client.post("/api/v1/", json=post_data, headers=headers)
    assert response.status_code == 201

    # Verify response structure
    data = response.json()
    assert "id" in data
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["slug"] == post_data["slug"]
    assert data["is_published"] == post_data["is_published"]


def test_create_new_post_invalid_data(test_user: User):
    """Test creation of a new post with invalid data."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Invalid post data (missing required fields)
    post_data = {
        # Missing required fields
    }

    response = client.post("/api/v1/", json=post_data, headers=headers)
    assert response.status_code == 422


def test_create_new_post_unauthorized():
    """Test that unauthenticated requests are rejected."""
    # Post data
    post_data = {
        "author_id": str(uuid.uuid4()),
        "category_id": str(uuid.uuid4()),
        "slug": "new-test-post",
        "title": "New Test Post",
        "content": "This is a new test post",
        "is_published": False,
    }

    response = client.post("/api/v1/", json=post_data)
    assert response.status_code == 401


# Integration tests for PUT /{post_id} - Update an existing post
def test_update_existing_post_success(test_user: User, test_category: Category, test_post: Post):
    """Test successful update of an existing post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Update data
    update_data = {
        "title": "Updated Test Post",
        "content": "This is an updated test post",
    }

    response = client.put(f"/api/v1/{test_post.id}", json=update_data, headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(test_post.id)
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]


def test_update_existing_post_not_found(test_user: User):
    """Test update of a non-existent post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Update data
    update_data = {
        "title": "Updated Test Post",
        "content": "This is an updated test post",
    }

    # Try to update a non-existent post
    fake_post_id = uuid.uuid4()
    response = client.put(f"/api/v1/{fake_post_id}", json=update_data, headers=headers)
    assert response.status_code == 404


def test_update_existing_post_invalid_data(test_user: User, test_post: Post):
    """Test update of an existing post with invalid data."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Invalid update data
    update_data = {
        "title": "",  # Invalid: empty title
    }

    response = client.put(f"/api/v1/{test_post.id}", json=update_data, headers=headers)
    assert response.status_code == 422


def test_update_existing_post_unauthorized(test_post: Post):
    """Test that unauthenticated requests are rejected."""
    # Update data
    update_data = {
        "title": "Updated Test Post",
        "content": "This is an updated test post",
    }

    response = client.put(f"/api/v1/{test_post.id}", json=update_data)
    assert response.status_code == 401


# Integration tests for DELETE /{post_id} - Delete a post
def test_delete_post_by_id_success(test_user: User, test_post: Post):
    """Test successful deletion of a post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/{test_post.id}", headers=headers)
    assert response.status_code == 204


def test_delete_post_by_id_not_found(test_user: User):
    """Test deletion of a non-existent post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a non-existent post
    fake_post_id = uuid.uuid4()
    response = client.delete(f"/api/v1/{fake_post_id}", headers=headers)
    assert response.status_code == 404


def test_delete_post_by_id_unauthorized(test_post: Post):
    """Test that unauthenticated requests are rejected."""
    response = client.delete(f"/api/v1/{test_post.id}")
    assert response.status_code == 401


# Integration tests for GET /drafts - Retrieve draft posts
def test_read_draft_posts_success(test_user: User, test_post: Post):
    """Test successful retrieval of draft posts."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/drafts", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Check that our test draft post is in the response
    draft_post_titles = [post["title"] for post in data]
    assert test_post.title in draft_post_titles


def test_read_draft_posts_empty_result(test_user: User):
    """Test retrieval of draft posts when no draft posts exist."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/drafts", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)


def test_read_draft_posts_unauthorized():
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/v1/drafts")
    assert response.status_code == 401


# Integration tests for GET /published - Retrieve published posts
def test_read_published_posts_success(published_post: Post):
    """Test successful retrieval of published posts."""
    response = client.get("/api/v1/published")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Check that our test published post is in the response
    published_post_titles = [post["title"] for post in data]
    assert published_post.title in published_post_titles


def test_read_published_posts_empty_result():
    """Test retrieval of published posts when no published posts exist."""
    response = client.get("/api/v1/published")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)


# Integration tests for POST /{post_id}/publish - Publish a draft post
def test_publish_post_success(test_user: User, test_post: Post):
    """Test successful publishing of a draft post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(f"/api/v1/{test_post.id}/publish", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(test_post.id)
    assert data["is_published"] is True


def test_publish_post_not_found(test_user: User):
    """Test publishing of a non-existent post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to publish a non-existent post
    fake_post_id = uuid.uuid4()
    response = client.post(f"/api/v1/{fake_post_id}/publish", headers=headers)
    assert response.status_code == 404


def test_publish_post_already_published(test_user: User, published_post: Post):
    """Test publishing of an already published post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(f"/api/v1/{published_post.id}/publish", headers=headers)
    assert response.status_code == 400


def test_publish_post_unauthorized(test_post: Post):
    """Test that unauthenticated requests are rejected."""
    response = client.post(f"/api/v1/{test_post.id}/publish")
    assert response.status_code == 401


# Integration tests for POST /{post_id}/unpublish - Unpublish a published post
def test_unpublish_post_success(test_user: User, published_post: Post):
    """Test successful unpublishing of a published post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(f"/api/v1/{published_post.id}/unpublish", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(published_post.id)
    assert data["is_published"] is False


def test_unpublish_post_not_found(test_user: User):
    """Test unpublishing of a non-existent post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to unpublish a non-existent post
    fake_post_id = uuid.uuid4()
    response = client.post(f"/api/v1/{fake_post_id}/unpublish", headers=headers)
    assert response.status_code == 404


def test_unpublish_post_not_published(test_user: User, test_post: Post):
    """Test unpublishing of a draft post."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(f"/api/v1/{test_post.id}/unpublish", headers=headers)
    assert response.status_code == 400


def test_unpublish_post_unauthorized(published_post: Post):
    """Test that unauthenticated requests are rejected."""
    response = client.post(f"/api/v1/{published_post.id}/unpublish")
    assert response.status_code == 401
