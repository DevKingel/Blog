import uuid
from collections.abc import Generator
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM, get_password_hash
from app.db.session import get_session
from app.main import app
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
    result = await db_session.execute(select(User).where(User.email == "test@example.com"))
    test_user = result.scalar_one_or_none()

    if not test_user:
        # Create a test user
        test_user = User(
            id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=False,
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

    return test_user


# Integration tests for POST /auth/login
def test_login_success(test_user: User):
    """Test successful user login."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify the token can be decoded
    token = data["access_token"]
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == str(test_user.id)


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

    # Verify error response
    data = response.json()
    assert data["detail"] == "Incorrect email or password"


def test_login_missing_fields():
    """Test login with missing required fields."""
    response = client.post("/api/v1/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422


# Integration tests for POST /auth/logout
def test_logout_success():
    """Test successful user logout."""
    response = client.post(
        "/api/v1/auth/logout",
        json={"token": "fake_token"}
    )
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["message"] == "Successfully logged out"


def test_logout_missing_token():
    """Test logout with missing token."""
    response = client.post("/api/v1/auth/logout", json={})
    assert response.status_code == 422


# Integration tests for POST /auth/refresh
def test_refresh_token_success():
    """Test successful token refresh."""
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "fake_refresh_token"}
    )
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_missing_fields():
    """Test refresh token with missing required fields."""
    response = client.post("/api/v1/auth/refresh", json={})
    assert response.status_code == 422


# Integration tests for POST /auth/forgot-password
def test_forgot_password_success(test_user: User):
    """Test successful password reset request."""
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["message"] == "If the email exists, a password reset link has been sent"


def test_forgot_password_user_not_found():
    """Test password reset request for non-existent user."""
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "nonexistent@example.com"}
    )
    assert response.status_code == 200

    # For security reasons, we return the same message even if user doesn't exist
    data = response.json()
    assert data["message"] == "If the email exists, a password reset link has been sent"


def test_forgot_password_invalid_email():
    """Test password reset request with invalid email format."""
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "invalid-email"}
    )
    assert response.status_code == 422


# Integration tests for POST /auth/reset-password
def test_reset_password_success():
    """Test successful password reset."""
    # Create a valid reset token
    email = "test@example.com"
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(UTC)
    expires = now + delta
    exp = expires.timestamp()
    token = jwt.encode(
        {"exp": exp, "nbf": now.timestamp(), "sub": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "newpassword123"}
    )
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert data["message"] == "Password successfully reset"


def test_reset_password_invalid_token():
    """Test password reset with invalid token."""
    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": "invalid_token", "new_password": "newpassword123"}
    )
    assert response.status_code == 400

    # Verify error response
    data = response.json()
    assert data["detail"] == "Invalid or expired token"


def test_reset_password_missing_fields():
    """Test password reset with missing required fields."""
    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": "fake_token"}
    )
    assert response.status_code == 422
