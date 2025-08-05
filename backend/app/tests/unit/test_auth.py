import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.auth import (
    forgot_password,
    login,
    logout,
    refresh_token,
    reset_password,
)
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
)


@pytest.mark.asyncio
async def test_login_success():
    """Test successful user login."""
    # Mock data
    user_id = uuid.uuid4()
    mock_user = Mock(spec=User)
    mock_user.id = user_id

    # Mock request data
    login_data = LoginRequest(email="test@example.com", password="password123")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the authenticate_user and create_access_token functions
    with (
        patch("app.api.v1.endpoints.auth.authenticate_user") as mock_authenticate,
        patch("app.api.v1.endpoints.auth.create_access_token") as mock_create_token,
    ):
        mock_authenticate.return_value = mock_user
        mock_create_token.return_value = "fake_access_token"

        # Call the endpoint
        result = await login(login_data=login_data, db=mock_db)

        # Assertions
        assert result.access_token == "fake_access_token"
        assert result.token_type == "bearer"
        mock_authenticate.assert_called_once_with(mock_db, "test@example.com", "password123")
        mock_create_token.assert_called_once()


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    # Mock request data
    login_data = LoginRequest(email="test@example.com", password="wrongpassword")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the authenticate_user function to return None
    with patch("app.api.v1.endpoints.auth.authenticate_user") as mock_authenticate:
        mock_authenticate.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await login(login_data=login_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect email or password"
        assert "WWW-Authenticate" in exc_info.value.headers
        mock_authenticate.assert_called_once_with(mock_db, "test@example.com", "wrongpassword")


@pytest.mark.asyncio
async def test_logout_success():
    """Test successful user logout."""
    # Mock request data
    logout_data = LogoutRequest(token="fake_token")

    # Call the endpoint
    result = await logout(logout_data=logout_data)

    # Assertions
    assert result["message"] == "Successfully logged out"


@pytest.mark.asyncio
async def test_refresh_token_success():
    """Test successful token refresh."""
    # Mock request data
    refresh_data = RefreshTokenRequest(refresh_token="fake_refresh_token")

    # Mock the create_access_token function
    with patch("app.api.v1.endpoints.auth.create_access_token") as mock_create_token:
        mock_create_token.return_value = "new_access_token"

        # Call the endpoint
        result = await refresh_token(refresh_data=refresh_data)

        # Assertions
        assert result.access_token == "new_access_token"
        assert result.token_type == "bearer"
        mock_create_token.assert_called_once()


@pytest.mark.asyncio
async def test_forgot_password_success():
    """Test successful password reset request."""
    # Mock request data
    forgot_data = ForgotPasswordRequest(email="test@example.com")

    # Mock dependencies
    mock_db = AsyncMock()

    # Call the endpoint
    result = await forgot_password(forgot_data=forgot_data, db=mock_db)

    # Assertions
    assert result["message"] == "If the email exists, a password reset link has been sent"


@pytest.mark.asyncio
async def test_forgot_password_user_not_found():
    """Test password reset request for non-existent user."""
    # Mock request data
    forgot_data = ForgotPasswordRequest(email="nonexistent@example.com")

    # Mock dependencies
    mock_db = AsyncMock()

    # Call the endpoint
    result = await forgot_password(forgot_data=forgot_data, db=mock_db)

    # Assertions
    assert result["message"] == "If the email exists, a password reset link has been sent"


@pytest.mark.asyncio
async def test_reset_password_success():
    """Test successful password reset."""
    # Mock request data
    reset_data = ResetPasswordRequest(token="fake_reset_token", new_password="newpassword123")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the verify_password_reset_token function
    with patch("app.api.v1.endpoints.auth.verify_password_reset_token") as mock_verify_token:
        mock_verify_token.return_value = "test@example.com"

        # Call the endpoint
        result = await reset_password(reset_data=reset_data, db=mock_db)

        # Assertions
        assert result.message == "Password successfully reset"
        mock_verify_token.assert_called_once_with("fake_reset_token")


@pytest.mark.asyncio
async def test_reset_password_invalid_token():
    """Test password reset with invalid token."""
    # Mock request data
    reset_data = ResetPasswordRequest(token="invalid_token", new_password="newpassword123")

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the verify_password_reset_token function to return None
    with patch("app.api.v1.endpoints.auth.verify_password_reset_token") as mock_verify_token:
        mock_verify_token.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await reset_password(reset_data=reset_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "Invalid or expired token"
        mock_verify_token.assert_called_once_with("invalid_token")
