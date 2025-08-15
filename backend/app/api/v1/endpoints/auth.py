import uuid
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    authenticate_user,
    create_access_token,
    verify_password_reset_token,
)
from app.db.session import get_session
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    PasswordResetSuccess,
    RefreshTokenRequest,
    ResetPasswordRequest,
    Token,
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Authenticate user and return JWT token.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(logout_data: LogoutRequest) -> Any:
    """
    Logout user by invalidating the token.
    Note: In a real implementation, you would want to add the token to a blacklist.
    """
    # In a real implementation, you would want to add the token to a blacklist
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest) -> Any:
    """
    Refresh JWT token.
    Note: In a real implementation, you would want to validate the refresh token.
    """
    # In a real implementation, you would want to validate the refresh token
    # and generate a new access token
    # For now, we'll just return a new token with a new expiration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(uuid.uuid4()), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    forgot_data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Request password reset.
    Note: In a real implementation, you would send an email with a reset link.
    """
    # In a real implementation, you would:
    # 1. Check if the user exists
    # 2. Generate a password reset token
    # 3. Send an email with the reset link
    # For now, we'll just return a success message
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password", response_model=PasswordResetSuccess)
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Reset password with token.
    """
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    # In a real implementation, you would:
    # 1. Get the user by email
    # 2. Update the user's password
    # For now, we'll just return a success message
    return PasswordResetSuccess(message="Password successfully reset")
