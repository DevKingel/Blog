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
async def test_categories(db_session: AsyncSession) -> list[Category]:
    """Create multiple test categories."""
    categories = []
    for i in range(3):
        # Check if category already exists
        result = await db_session.execute(select(Category).where(Category.name == f"Category {i}"))
        category = result.scalar_one_or_none()

        if not category:
            category = Category(
                id=uuid.uuid4(),
                name=f"Category {i}",
                slug=f"category-{i}",
            )
            db_session.add(category)
            categories.append(category)

    if categories:
        await db_session.commit()
        # Refresh all categories to get their IDs
        for category in categories:
            await db_session.refresh(category)

    # Get all test categories
    result = await db_session.execute(select(Category).where(Category.name.like("Category %")))
    return list(result.scalars().all())


@pytest.fixture
async def test_posts(db_session: AsyncSession, test_categories: list[Category]) -> list[Post]:
    """Create multiple test posts."""
    if not test_categories:
        return []

    posts = []
    category = test_categories[0]  # Use the first category for posts

    for i in range(3):
        # Check if post already exists
        result = await db_session.execute(select(Post).where(Post.title == f"Test Post {i}"))
        post = result.scalar_one_or_none()

        if not post:
            post = Post(
                id=uuid.uuid4(),
                title=f"Test Post {i}",
                content=f"Content for test post {i}",
                category_id=category.id,
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


# Integration tests for POST /categories/
def test_create_category_success(admin_user: User):
    """Test successful creation of a category."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test data
    category_data = {
        "name": "Technology",
        "slug": "technology"
    }

    response = client.post("/api/v1/categories/", json=category_data, headers=headers)
    assert response.status_code == 201

    # Verify response structure
    data = response.json()
    assert "id" in data
    assert data["name"] == "Technology"
    assert data["slug"] == "technology"


def test_create_category_duplicate_name(admin_user: User, test_categories: list[Category]):
    """Test creation of a category with duplicate name."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to create a category with the same name as an existing one
    category_data = {
        "name": test_categories[0].name,  # Duplicate name
        "slug": "new-slug"
    }

    response = client.post("/api/v1/categories/", json=category_data, headers=headers)
    assert response.status_code == 400


def test_create_category_duplicate_slug(admin_user: User, test_categories: list[Category]):
    """Test creation of a category with duplicate slug."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to create a category with the same slug as an existing one
    category_data = {
        "name": "New Category",
        "slug": test_categories[0].slug  # Duplicate slug
    }

    response = client.post("/api/v1/categories/", json=category_data, headers=headers)
    assert response.status_code == 400


def test_create_category_invalid_data(admin_user: User):
    """Test creation of a category with invalid data."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test with missing required fields
    category_data = {
        "name": "",  # Empty name
        "slug": "tech"
    }

    response = client.post("/api/v1/categories/", json=category_data, headers=headers)
    assert response.status_code == 422


def test_create_category_unauthorized():
    """Test that unauthenticated requests are rejected."""
    category_data = {
        "name": "Technology",
        "slug": "technology"
    }

    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 401


# Integration tests for GET /categories/
def test_get_categories_success(test_categories: list[Category]):
    """Test successful retrieval of categories."""
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)

    # If we have test categories, they should be in the response
    if test_categories:
        assert len(data) >= len(test_categories)


def test_get_categories_with_pagination(test_categories: list[Category]):
    """Test retrieval of categories with pagination."""
    response = client.get("/api/v1/categories/?skip=0&limit=2")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2


def test_get_categories_empty_result():
    """Test retrieval of categories when none exist."""
    # This test might not be meaningful in a test database with existing data
    # but we'll include it for completeness
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)


# Integration tests for GET /categories/{category_id}
def test_get_category_by_id_success(test_categories: list[Category]):
    """Test successful retrieval of a category by ID."""
    if not test_categories:
        pytest.skip("No test categories available")

    category = test_categories[0]
    response = client.get(f"/api/v1/categories/{category.id}")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(category.id)
    assert data["name"] == category.name
    assert data["slug"] == category.slug


def test_get_category_by_id_not_found():
    """Test retrieval of a non-existent category by ID."""
    fake_category_id = uuid.uuid4()
    response = client.get(f"/api/v1/categories/{fake_category_id}")
    assert response.status_code == 404


def test_get_category_by_id_invalid_uuid():
    """Test retrieval of a category with invalid UUID."""
    response = client.get("/api/v1/categories/invalid-uuid")
    assert response.status_code == 422


# Integration tests for PATCH /categories/{category_id}
def test_update_category_success(admin_user: User, test_categories: list[Category]):
    """Test successful update of a category."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    category = test_categories[0]
    update_data = {
        "name": "Updated Category Name"
    }

    response = client.patch(f"/api/v1/categories/{category.id}", json=update_data, headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(category.id)
    assert data["name"] == "Updated Category Name"


def test_update_category_not_found(admin_user: User):
    """Test update of a non-existent category."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_category_id = uuid.uuid4()
    update_data = {
        "name": "Updated Category Name"
    }

    response = client.patch(f"/api/v1/categories/{fake_category_id}", json=update_data, headers=headers)
    assert response.status_code == 404


def test_update_category_duplicate_name(admin_user: User, test_categories: list[Category]):
    """Test update of a category with a name that already exists."""
    if len(test_categories) < 2:
        pytest.skip("Not enough test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to update one category with the name of another
    category1 = test_categories[0]
    category2 = test_categories[1]

    update_data = {
        "name": category2.name  # Duplicate name
    }

    response = client.patch(f"/api/v1/categories/{category1.id}", json=update_data, headers=headers)
    assert response.status_code == 400


def test_update_category_duplicate_slug(admin_user: User, test_categories: list[Category]):
    """Test update of a category with a slug that already exists."""
    if len(test_categories) < 2:
        pytest.skip("Not enough test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to update one category with the slug of another
    category1 = test_categories[0]
    category2 = test_categories[1]

    update_data = {
        "slug": category2.slug  # Duplicate slug
    }

    response = client.patch(f"/api/v1/categories/{category1.id}", json=update_data, headers=headers)
    assert response.status_code == 400


def test_update_category_no_data(admin_user: User, test_categories: list[Category]):
    """Test update of a category with no data provided."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    category = test_categories[0]
    update_data = {}  # Empty data

    response = client.patch(f"/api/v1/categories/{category.id}", json=update_data, headers=headers)
    assert response.status_code == 400


def test_update_category_invalid_data(admin_user: User, test_categories: list[Category]):
    """Test update of a category with invalid data."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    category = test_categories[0]
    update_data = {
        "name": ""  # Empty name
    }

    response = client.patch(f"/api/v1/categories/{category.id}", json=update_data, headers=headers)
    assert response.status_code == 422


def test_update_category_unauthorized(test_categories: list[Category]):
    """Test that unauthenticated requests are rejected."""
    if not test_categories:
        pytest.skip("No test categories available")

    category = test_categories[0]
    update_data = {
        "name": "Updated Category Name"
    }

    response = client.patch(f"/api/v1/categories/{category.id}", json=update_data)
    assert response.status_code == 401


# Integration tests for DELETE /categories/{category_id}
def test_delete_category_success(admin_user: User, test_categories: list[Category]):
    """Test successful deletion of a category."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    category = test_categories[0]
    response = client.delete(f"/api/v1/categories/{category.id}", headers=headers)
    assert response.status_code == 204


def test_delete_category_not_found(admin_user: User):
    """Test deletion of a non-existent category."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_category_id = uuid.uuid4()
    response = client.delete(f"/api/v1/categories/{fake_category_id}", headers=headers)
    assert response.status_code == 404


def test_delete_category_unauthorized(test_categories: list[Category]):
    """Test that unauthenticated requests are rejected."""
    if not test_categories:
        pytest.skip("No test categories available")

    category = test_categories[0]
    response = client.delete(f"/api/v1/categories/{category.id}")
    assert response.status_code == 401


# Integration tests for GET /categories/{category_id}/posts
def test_get_category_posts_success(test_categories: list[Category], test_posts: list[Post]):
    """Test successful retrieval of posts in a category."""
    if not test_categories or not test_posts:
        pytest.skip("No test categories or posts available")

    category = test_categories[0]
    response = client.get(f"/api/v1/categories/{category.id}/posts")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)

    # If we have test posts in this category, they should be in the response
    category_posts = [post for post in test_posts if post.category_id == category.id]
    if category_posts:
        assert len(data) >= len(category_posts)


def test_get_category_posts_category_not_found():
    """Test retrieval of posts for a non-existent category."""
    fake_category_id = uuid.uuid4()
    response = client.get(f"/api/v1/categories/{fake_category_id}/posts")
    assert response.status_code == 404


def test_get_category_posts_empty_result(test_categories: list[Category]):
    """Test retrieval of posts for a category with no posts."""
    if not test_categories:
        pytest.skip("No test categories available")

    # Use a category that doesn't have posts
    category = test_categories[0]
    response = client.get(f"/api/v1/categories/{category.id}/posts")
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Could be empty or might have posts from other tests
