import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as user_crud
from app.crud.comment import get_comments_by_user
from app.crud.post import get_posts_by_author
from app.db.session import get_session
from app.models.user import User
from app.schemas.comment import CommentRead
from app.schemas.post import PostRead
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    *,
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
) -> User:
    """
    Create new user.
    """
    try:
        user = await user_crud.get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        user = await user_crud.create_user(db, user_in=user_in)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating user",
        ) from e


@router.get("/", response_model=list[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
) -> list[User]:
    """
    Retrieve users.
    """
    try:
        users = await user_crud.get_multi_user(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching users",
        ) from e


@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> User:
    """
    Get a specific user by id.
    """
    try:
        user = await user_crud.get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching user",
        ) from e


@router.patch("/{user_id}", response_model=UserRead)
async def update_existing_user(
    *,
    user_id: uuid.UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_session),
) -> User:
    """
    Update a user.
    """
    try:
        db_user = await user_crud.get_user(db, user_id=user_id)
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="The user with this id does not exist in the system",
            )
        user = await user_crud.update_user(db, db_user=db_user, user_in=user_in)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while updating user",
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    *,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Delete a user.
    """
    try:
        success = await user_crud.delete_user(db, user_id=user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while deleting user",
        ) from e


@router.get("/{user_id}/posts", response_model=list[PostRead])
async def get_user_posts(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get all posts by a specific user.
    """
    try:
        posts = await get_posts_by_author(db, author_id=user_id)
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching user posts",
        ) from e


@router.get("/{user_id}/comments", response_model=list[CommentRead])
async def get_user_comments(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get all comments by a specific user.
    """
    try:
        comments = await get_comments_by_user(db, user_id=user_id)
        return comments
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching user comments",
        ) from e
