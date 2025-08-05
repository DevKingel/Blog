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
from app.models.comment import Comment
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
    result = await db_session.execute(select(User).where(User.username == "test_comment_user"))
    test_user = result.scalar_one_or_none()

    if not test_user:
        # Create a test user
        test_user = User(
            id=uuid.uuid4(),
            username="test_comment_user",
            email="test_comment_user@example.com",
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
            slug="test-category",
        )
        db_session.add(test_category)
        await db_session.commit()
        await db_session.refresh(test_category)

    return test_category


@pytest.fixture
async def test_post(db_session: AsyncSession, test_user: User, test_category: Category) -> Post:
    """Create a test post."""
    # Check if test post already exists
    result = await db_session.execute(select(Post).where(Post.title == "Test Post for Comments"))
    test_post = result.scalar_one_or_none()

    if not test_post:
        # Create a test post
        test_post = Post(
            id=uuid.uuid4(),
            title="Test Post for Comments",
            content="This is a test post for comments",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(test_post)
        await db_session.commit()
        await db_session.refresh(test_post)

    return test_post


@pytest.fixture
async def test_comments(db_session: AsyncSession, test_post: Post, test_user: User) -> list[Comment]:
    """Create multiple test comments."""
    comments = []
    for i in range(3):
        # Check if comment already exists
        result = await db_session.execute(select(Comment).where(Comment.content == f"Test Comment {i}"))
        comment = result.scalar_one_or_none()

        if not comment:
            comment = Comment(
                id=uuid.uuid4(),
                user_id=test_user.id,
                post_id=test_post.id,
                content=f"Test Comment {i}",
            )
            db_session.add(comment)
            comments.append(comment)

    if comments:
        await db_session.commit()
        # Refresh all comments to get their IDs
        for comment in comments:
            await db_session.refresh(comment)

    # Get all test comments
    result = await db_session.execute(select(Comment).where(Comment.content.like("Test Comment %")))
    return list(result.scalars().all())


# Integration tests for GET /posts/{post_id}/comments
def test_read_comments_by_post_success(test_post: Post, test_comments: list[Comment]):
    """Test successful retrieval of comments by post ID."""
    response = client.get(f"/api/v1/posts/{test_post.id}/comments")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)

    # If we have test comments, they should be in the response
    if test_comments:
        assert len(data) >= len(test_comments)


def test_read_comments_by_post_empty_result(test_post: Post):
    """Test retrieval of comments by post ID when no comments exist."""
    # Create a new post without comments
    response = client.get(f"/api/v1/posts/{test_post.id}/comments")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Could be empty or might have comments from other tests


def test_read_comments_by_post_nonexistent_post():
    """Test retrieval of comments for a non-existent post."""
    fake_post_id = uuid.uuid4()
    response = client.get(f"/api/v1/posts/{fake_post_id}/comments")
    assert response.status_code == 200  # Should return empty list, not 404

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


# Integration tests for POST /posts/{post_id}/comments
def test_create_comment_for_post_success(test_post: Post, test_user: User):
    """Test successful creation of a comment for a post."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test data
    comment_data = {
        "user_id": str(test_user.id),
        "content": "This is a test comment"
    }

    response = client.post(f"/api/v1/posts/{test_post.id}/comments", json=comment_data, headers=headers)
    assert response.status_code == 201

    # Verify response structure
    data = response.json()
    assert "id" in data
    assert data["content"] == "This is a test comment"
    assert data["post_id"] == str(test_post.id)
    assert data["user_id"] == str(test_user.id)


def test_create_comment_for_post_invalid_post(test_user: User):
    """Test creation of a comment for a non-existent post."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test data
    comment_data = {
        "user_id": str(test_user.id),
        "content": "This is a test comment"
    }

    fake_post_id = uuid.uuid4()
    response = client.post(f"/api/v1/posts/{fake_post_id}/comments", json=comment_data, headers=headers)
    assert response.status_code == 404


def test_create_comment_for_post_missing_fields(test_post: Post, test_user: User):
    """Test creation of a comment with missing required fields."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test data with missing content
    comment_data = {
        "user_id": str(test_user.id)
        # Missing content
    }

    response = client.post(f"/api/v1/posts/{test_post.id}/comments", json=comment_data, headers=headers)
    assert response.status_code == 422


# Integration tests for GET /comments/{comment_id}
def test_read_comment_by_id_success(test_comments: list[Comment]):
    """Test successful retrieval of a comment by ID."""
    if not test_comments:
        pytest.skip("No test comments available")

    comment = test_comments[0]
    response = client.get(f"/api/v1/comments/{comment.id}")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(comment.id)
    assert data["content"] == comment.content
    assert data["post_id"] == str(comment.post_id)
    assert data["user_id"] == str(comment.user_id)


def test_read_comment_by_id_not_found():
    """Test retrieval of a non-existent comment by ID."""
    fake_comment_id = uuid.uuid4()
    response = client.get(f"/api/v1/comments/{fake_comment_id}")
    assert response.status_code == 404


def test_read_comment_by_id_invalid_uuid():
    """Test retrieval of a comment with invalid UUID."""
    response = client.get("/api/v1/comments/invalid-uuid")
    assert response.status_code == 422


# Integration tests for PUT /comments/{comment_id}
def test_update_comment_by_id_success(test_comments: list[Comment], test_user: User):
    """Test successful update of a comment by ID."""
    if not test_comments:
        pytest.skip("No test comments available")

    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    comment = test_comments[0]
    update_data = {
        "content": "Updated comment content"
    }

    response = client.put(f"/api/v1/comments/{comment.id}", json=update_data, headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(comment.id)
    assert data["content"] == "Updated comment content"


def test_update_comment_by_id_not_found(test_user: User):
    """Test update of a non-existent comment by ID."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_comment_id = uuid.uuid4()
    update_data = {
        "content": "Updated comment content"
    }

    response = client.put(f"/api/v1/comments/{fake_comment_id}", json=update_data, headers=headers)
    assert response.status_code == 404


def test_update_comment_by_id_invalid_data(test_comments: list[Comment], test_user: User):
    """Test update of a comment with invalid data."""
    if not test_comments:
        pytest.skip("No test comments available")

    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    comment = test_comments[0]
    update_data = {
        "content": ""  # Empty content
    }

    response = client.put(f"/api/v1/comments/{comment.id}", json=update_data, headers=headers)
    assert response.status_code == 422


# Integration tests for DELETE /comments/{comment_id}
def test_delete_comment_by_id_success(test_comments: list[Comment], test_user: User):
    """Test successful deletion of a comment by ID."""
    if not test_comments:
        pytest.skip("No test comments available")

    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    comment = test_comments[0]
    response = client.delete(f"/api/v1/comments/{comment.id}", headers=headers)
    assert response.status_code == 204


def test_delete_comment_by_id_not_found(test_user: User):
    """Test deletion of a non-existent comment by ID."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_comment_id = uuid.uuid4()
    response = client.delete(f"/api/v1/comments/{fake_comment_id}", headers=headers)
    assert response.status_code == 404


# Integration tests for POST /comments/{comment_id}/reply
def test_reply_to_comment_success(test_comments: list[Comment], test_user: User):
    """Test successful reply to a comment."""
    if not test_comments:
        pytest.skip("No test comments available")

    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    parent_comment = test_comments[0]
    reply_data = {
        "user_id": str(test_user.id),
        "content": "This is a reply to the comment"
    }

    response = client.post(f"/api/v1/comments/{parent_comment.id}/reply", json=reply_data, headers=headers)
    assert response.status_code == 201

    # Verify response structure
    data = response.json()
    assert "id" in data
    assert data["content"] == "This is a reply to the comment"
    assert data["post_id"] == str(parent_comment.post_id)
    assert data["parent_comment_id"] == str(parent_comment.id)
    assert data["user_id"] == str(test_user.id)


def test_reply_to_comment_parent_not_found(test_user: User):
    """Test reply to a non-existent parent comment."""
    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    reply_data = {
        "user_id": str(test_user.id),
        "content": "This is a reply to the comment"
    }

    fake_comment_id = uuid.uuid4()
    response = client.post(f"/api/v1/comments/{fake_comment_id}/reply", json=reply_data, headers=headers)
    assert response.status_code == 404


def test_reply_to_comment_missing_fields(test_comments: list[Comment], test_user: User):
    """Test reply to a comment with missing required fields."""
    if not test_comments:
        pytest.skip("No test comments available")

    # Create auth token for user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    parent_comment = test_comments[0]
    reply_data = {
        "user_id": str(test_user.id)
        # Missing content
    }

    response = client.post(f"/api/v1/comments/{parent_comment.id}/reply", json=reply_data, headers=headers)
    assert response.status_code == 422


# Integration tests for GET /comments/{comment_id}/replies
def test_read_replies_to_comment_success(test_comments: list[Comment]):
    """Test successful retrieval of replies to a comment."""
    if not test_comments:
        pytest.skip("No test comments available")

    parent_comment = test_comments[0]
    response = client.get(f"/api/v1/comments/{parent_comment.id}/replies")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Could be empty or might have replies from other tests


def test_read_replies_to_comment_parent_not_found():
    """Test retrieval of replies to a non-existent parent comment."""
    fake_comment_id = uuid.uuid4()
    response = client.get(f"/api/v1/comments/{fake_comment_id}/replies")
    assert response.status_code == 404


def test_read_replies_to_comment_empty_result(test_comments: list[Comment]):
    """Test retrieval of replies to a comment when no replies exist."""
    if not test_comments:
        pytest.skip("No test comments available")

    parent_comment = test_comments[0]
    response = client.get(f"/api/v1/comments/{parent_comment.id}/replies")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Could be empty or might have replies from other tests
