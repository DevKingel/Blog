import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_session
from app.main import app
from app.models.role import Role
from app.models.user import User

client = TestClient(app)


# Helper functions for creating test data
def create_test_token(user_id: uuid.UUID) -> str:
    """Create a test JWT token for a user."""
    payload = {
        "sub": str(user_id),
        "exp": 3600,  # 1 hour expiration
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
            is_superuser=True,
        )
        db_session.add(admin_user)
        await db_session.commit()
        await db_session.refresh(admin_user)

    return admin_user


@pytest.fixture
async def test_roles(db_session: AsyncSession) -> list[Role]:
    """Create multiple test roles."""
    roles = []
    role_names = ["admin", "user", "moderator", "editor", "viewer"]

    for name in role_names:
        # Check if role already exists
        result = await db_session.execute(select(Role).where(Role.name == name))
        role = result.scalar_one_or_none()

        if not role:
            role = Role(
                id=uuid.uuid4(), name=name, description=f"{name.capitalize()} role"
            )
            db_session.add(role)
            roles.append(role)

    if roles:
        await db_session.commit()
        # Refresh all roles to get their IDs
        for role in roles:
            await db_session.refresh(role)

    # Get all test roles
    result = await db_session.execute(select(Role))
    return list(result.scalars().all())


# Integration tests for POST /roles/ - Create a new role
def test_create_role_success(admin_user: User):
    """Test successful role creation."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role_data = {"name": "new_role", "description": "A new role for testing"}

    response = client.post("/api/v1/roles/", json=role_data, headers=headers)
    assert response.status_code == 201

    # Verify response structure
    data = response.json()
    assert "id" in data
    assert data["name"] == "new_role"
    assert data["description"] == "A new role for testing"


def test_create_role_invalid_data(admin_user: User):
    """Test role creation with invalid data."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Missing required field
    role_data = {"description": "A role without a name"}

    response = client.post("/api/v1/roles/", json=role_data, headers=headers)
    assert response.status_code == 422


def test_create_role_duplicate_name(admin_user: User, test_roles: list[Role]):
    """Test role creation with duplicate name."""
    if not test_roles:
        pytest.skip("No test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to create a role with an existing name
    role_data = {"name": test_roles[0].name, "description": "Duplicate role"}

    response = client.post("/api/v1/roles/", json=role_data, headers=headers)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_role_unauthorized():
    """Test that unauthenticated requests are rejected."""
    role_data = {"name": "unauthorized_role", "description": "Should not be created"}

    response = client.post("/api/v1/roles/", json=role_data)
    assert response.status_code == 401


# Integration tests for GET /roles/ - Retrieve all roles
def test_read_roles_success(admin_user: User, test_roles: list[Role]):
    """Test successful retrieval of all roles."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/roles/", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert isinstance(data, list)
    # Should have at least the test roles
    assert len(data) >= len(test_roles)


def test_read_roles_unauthorized():
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/v1/roles/")
    assert response.status_code == 401


# Integration tests for GET /roles/{role_id} - Get a specific role by id
def test_read_role_by_id_success(admin_user: User, test_roles: list[Role]):
    """Test successful retrieval of a role by ID."""
    if not test_roles:
        pytest.skip("No test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role = test_roles[0]
    response = client.get(f"/api/v1/roles/{role.id}", headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(role.id)
    assert data["name"] == role.name
    assert data["description"] == role.description


def test_read_role_by_id_not_found(admin_user: User):
    """Test retrieval of a non-existent role by ID."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_role_id = uuid.uuid4()
    response = client.get(f"/api/v1/roles/{fake_role_id}", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_read_role_by_id_unauthorized():
    """Test that unauthenticated requests are rejected."""
    fake_role_id = uuid.uuid4()
    response = client.get(f"/api/v1/roles/{fake_role_id}")
    assert response.status_code == 401


# Integration tests for PUT /roles/{role_id} - Update a role
def test_update_role_success(admin_user: User, test_roles: list[Role]):
    """Test successful role update."""
    if not test_roles:
        pytest.skip("No test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role = test_roles[0]
    update_data = {"name": "updated_role", "description": "Updated role description"}

    response = client.put(f"/api/v1/roles/{role.id}", json=update_data, headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(role.id)
    assert data["name"] == "updated_role"
    assert data["description"] == "Updated role description"


def test_update_role_partial(admin_user: User, test_roles: list[Role]):
    """Test partial role update."""
    if not test_roles:
        pytest.skip("No test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role = test_roles[0]
    update_data = {"description": "Partially updated description"}

    response = client.put(f"/api/v1/roles/{role.id}", json=update_data, headers=headers)
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["id"] == str(role.id)
    assert data["name"] == role.name  # Should remain unchanged
    assert data["description"] == "Partially updated description"


def test_update_role_not_found(admin_user: User):
    """Test update of a non-existent role."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_role_id = uuid.uuid4()
    update_data = {"name": "updated_role"}

    response = client.put(
        f"/api/v1/roles/{fake_role_id}", json=update_data, headers=headers
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_role_duplicate_name(admin_user: User, test_roles: list[Role]):
    """Test role update with duplicate name."""
    if len(test_roles) < 2:
        pytest.skip("Not enough test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role1 = test_roles[0]
    role2 = test_roles[1]

    # Try to update role1 to have the same name as role2
    update_data = {"name": role2.name}

    response = client.put(
        f"/api/v1/roles/{role1.id}", json=update_data, headers=headers
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_role_invalid_data(admin_user: User, test_roles: list[Role]):
    """Test role update with invalid data."""
    if not test_roles:
        pytest.skip("No test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    role = test_roles[0]
    # Empty update data
    update_data = {}

    response = client.put(f"/api/v1/roles/{role.id}", json=update_data, headers=headers)
    assert response.status_code == 400
    assert "No data provided" in response.json()["detail"]


def test_update_role_unauthorized(test_roles: list[Role]):
    """Test that unauthenticated requests are rejected."""
    if not test_roles:
        pytest.skip("No test roles available")

    role = test_roles[0]
    update_data = {"name": "unauthorized_update"}

    response = client.put(f"/api/v1/roles/{role.id}", json=update_data)
    assert response.status_code == 401


# Integration tests for DELETE /roles/{role_id} - Delete a role
def test_delete_role_success(admin_user: User, test_roles: list[Role]):
    """Test successful role deletion."""
    if len(test_roles) < 2:  # Keep at least one role for other tests
        pytest.skip("Not enough test roles available")

    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Use the last role for deletion
    role_to_delete = test_roles[-1]
    response = client.delete(f"/api/v1/roles/{role_to_delete.id}", headers=headers)
    assert response.status_code == 204


def test_delete_role_not_found(admin_user: User):
    """Test deletion of a non-existent role."""
    # Create auth token for admin user
    token = create_test_token(admin_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    fake_role_id = uuid.uuid4()
    response = client.delete(f"/api/v1/roles/{fake_role_id}", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_role_unauthorized(test_roles: list[Role]):
    """Test that unauthenticated requests are rejected."""
    if not test_roles:
        pytest.skip("No test roles available")

    role = test_roles[0]
    response = client.delete(f"/api/v1/roles/{role.id}")
    assert response.status_code == 401
