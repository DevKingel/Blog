import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import stat as stat_crud
from app.db.session import get_session
from app.schemas.stat import PostStatsRead, SiteStatsRead, UserStatsRead

router = APIRouter()


@router.get("/posts/{post_id}", response_model=PostStatsRead)
async def get_post_statistics(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get statistics for a specific post.
    """
    stat = await stat_crud.get_stat_by_post_id(db, post_id=post_id)
    return PostStatsRead(
        post_id=stat.post_id,
        views=stat.views,
        likes=stat.likes
    )


@router.get("/users/{user_id}", response_model=UserStatsRead)
async def get_user_statistics(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get statistics for a specific user.
    """
    user_stats = await stat_crud.get_user_stats(db, user_id=user_id)
    return UserStatsRead(**user_stats)


@router.get("/site", response_model=SiteStatsRead)
async def get_site_statistics(
    db: AsyncSession = Depends(get_session),
):
    """
    Get overall site statistics.
    """
    site_stats = await stat_crud.get_site_stats(db)
    return SiteStatsRead(**site_stats)


@router.post("/posts/{post_id}/view", status_code=status.HTTP_201_CREATED)
async def record_post_view(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Record a post view.
    """
    stat = await stat_crud.increment_post_views(db, post_id=post_id)
    return {"message": "View recorded successfully", "views": stat.views}


@router.post("/posts/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def record_post_like(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Record a post like.
    """
    stat = await stat_crud.increment_post_likes(db, post_id=post_id)
    return {"message": "Like recorded successfully", "likes": stat.likes}


@router.delete("/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post_like(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Remove a post like.
    """
    stat = await stat_crud.decrement_post_likes(db, post_id=post_id)
    return None
