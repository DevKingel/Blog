import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.api.dependencies.admin import get_admin_user
from app.crud import post as post_crud
from app.crud import stat as stat_crud
from app.crud import user as user_crud
from app.db.session import get_session
from app.models.post import Post
from app.models.user import User
from app.schemas.admin import AdminStatsRead, PostListRead, UserListRead
from app.schemas.post import PostRead
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/stats", response_model=AdminStatsRead)
async def get_admin_statistics(
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_admin_user),
) -> AdminStatsRead:
    """
    Get detailed admin statistics.

    Args:
        db: Database session
        current_admin: Current admin user (from dependency)

    Returns:
        AdminStatsRead: Detailed admin statistics
    """
    try:
        site_stats = await stat_crud.get_site_stats(db)
        return AdminStatsRead(**site_stats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching statistics",
        ) from e


@router.get("/users", response_model=UserListRead)
async def list_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_admin_user),
) -> UserListRead:
    """
    List all users (admin only).

    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        db: Database session
        current_admin: Current admin user (from dependency)

    Returns:
        UserListRead: List of users with pagination info
    """
    users = await user_crud.get_multi_user(db, skip=skip, limit=limit)
    total_users = len(users)

    return UserListRead(
        users=[UserRead(**user.__dict__) for user in users],
        total=total_users,
        page=skip // limit + 1,
        size=min(limit, total_users),
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_admin_user),
) -> None:
    """
    Delete any user (admin only).

    Args:
        user_id: ID of the user to delete
        db: Database session
        current_admin: Current admin user (from dependency)

    Returns:
        None
    """
    # Check if user exists
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete yourself"
        )

    # Delete the user
    success = await user_crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return None


@router.get("/posts", response_model=PostListRead)
async def list_all_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_admin_user),
) -> PostListRead:
    """
    List all posts (admin only).

    Args:
        skip: Number of posts to skip
        limit: Maximum number of posts to return
        db: Database session
        current_admin: Current admin user (from dependency)

    Returns:
        PostListRead: List of posts with pagination info
    """

    query = (
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)
    posts = result.scalars().all()
    total_posts = len(posts)

    return PostListRead(
        posts=[PostRead(**post.__dict__) for post in posts],
        total=total_posts,
        page=skip // limit + 1,
        size=min(limit, total_posts),
    )


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_admin_user),
) -> None:
    """
    Delete any post (admin only).

    Args:
        post_id: ID of the post to delete
        db: Database session
        current_admin: Current admin user (from dependency)

    Returns:
        None
    """
    # Check if post exists
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Delete the post
    success = await post_crud.delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")

    return None
