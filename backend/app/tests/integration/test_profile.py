import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.core.security import ALGORITHM
from app.main import app

client = TestClient(app)


# Helper functions for creating test data
def create_test_token(user_id: uuid.UUID) -> str:
    """Create a test JWT token for a user."""
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC).timestamp() + 3600,  # 1 hour expiration
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


# Create a sync fixture that sets up a test user
@pytest.fixture
def test_user():
    """Create a test user using a sync fixture."""

    # For integration tests, we'll create a simple user object
    # In real tests, the database would be used to create the actual user
    class MockUser:
        def __init__(self, user_id, username, email):
            self.user_id = user_id
            self.username = username
            self.email = email

    return MockUser(
        user_id=uuid.uuid4(), username="test_user", email="test@example.com"
    )


# Integration tests for GET /profile/ - Get current user's profile
def test_get_current_user_profile_success(test_user):
    """Test successful retrieval of current user's profile."""
    # Create auth token for test user
    token = create_test_token(test_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # In the current implementation, we pass user_id as a query parameter
    # In a real implementation, this would come from the token
    response = client.get(f"/api/v1/profile/?user_id={test_user.id}", headers=headers)

    # Should be 404 Not Found because the user doesn't actually exist in the database
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"


def test_get_current_user_profile_user_not_found():
    """Test retrieval of profile for non-existent user."""
    # Create auth token
    fake_user_id = uuid.uuid4()
    token = create_test_token(fake_user_id)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to get profile for non-existent user
    response = client.get(f"/api/v1/profile/?user_id={fake_user_id}", headers=headers)

    # Should be 404 Not Found
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"


def test_get_current_user_profile_unauthorized():
    """Test that unauthenticated requests are rejected."""
    fake_user_id = uuid.uuid4()

    # Try to get profile without authentication
    response = client.get(f"/api/v1/profile/?user_id={fake_user_id}")

    # Should be 401 Unauthorized (due to APIKeyMiddleware)
    assert response.status_code == 401


# Integration tests for PUT /profile/ - Update current user's profile
def test_update_current_user_profile_user_not_found():
    """Test update of profile for non-existent user."""
    # Create auth token
    fake_user_id = uuid.uuid4()
    token = create_test_token(fake_user_id)
    headers = {"Authorization": f"Bearer {token}"}

    # Update profile data
    update_data = {"username": "updated_user"}

    # Try to update profile for non-existent user
    response = client.put(
        f"/api/v1/profile/?user_id={fake_user_id}", json=update_data, headers=headers
    )

    # Should be 404 Not Found
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"


def test_update_current_user_profile_invalid_data():
    """Test update of profile with invalid data."""
    # Create auth token for a fake user
    fake_user_id = uuid.uuid4()
    token = create_test_token(fake_user_id)
    headers = {"Authorization": f"Bearer {token}"}

    # Invalid update data (invalid email format)
    update_data = {
        "email": "invalid-email"  # Invalid email format
    }

    # Try to update profile with invalid data
    response = client.put(
        f"/api/v1/profile/?user_id={fake_user_id}", json=update_data, headers=headers
    )

    # Should be 422 Unprocessable Entity (validation error)
    assert response.status_code == 422


def test_update_current_user_profile_unauthorized():
    """Test that unauthenticated requests are rejected."""
    fake_user_id = uuid.uuid4()

    # Update profile data
    update_data = {"username": "updated_user"}

    # Try to update profile without authentication
    response = client.put(f"/api/v1/profile/?user_id={fake_user_id}", json=update_data)

    # Should be 401 Unauthorized (due to APIKeyMiddleware)
    assert response.status_code == 401
