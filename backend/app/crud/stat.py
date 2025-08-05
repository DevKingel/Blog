from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stat import Stat
from app.models.post import Post
from app.models.user import User


async def create_stat(db: AsyncSession, stat_data: dict) -> Stat:
    """
    Create a new stat record.

    Args:
        db (AsyncSession): Database session.
        stat_data (dict): Data for the new stat record.

    Returns:
        Stat: The created stat record.
    """
    stat = Stat(**stat_data)
    db.add(stat)
    await db.commit()
    await db.refresh(stat)
    return stat


async def get_stat_by_id(db: AsyncSession, stat_id: UUID) -> Stat:
    """
    Get a stat record by ID.

    Args:
        db (AsyncSession): Database session.
        stat_id (UUID): The ID of the stat record.

    Returns:
        Stat: The stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id).options(selectinload(Stat.post))
    result = await db.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat


async def get_stat_by_post_id(db: AsyncSession, post_id: UUID) -> Stat:
    """
    Get a stat record by post ID.

    Args:
        db (AsyncSession): Database session.
        post_id (UUID): The ID of the post.

    Returns:
        Stat: The stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.post_id == post_id).options(selectinload(Stat.post))
    result = await db.execute(query)
    stat = result.scalars().first()
    if not stat:
        # Create a new stat record if it doesn't exist
        stat = await create_stat(db, {"post_id": post_id})
    return stat


async def get_all_stats(db: AsyncSession) -> list[Stat]:
    """
    Get all stat records.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[Stat]: A list of all stat records.
    """
    query = select(Stat).options(selectinload(Stat.post))
    result = await db.execute(query)
    return result.scalars().all()


async def update_stat(db: AsyncSession, stat_id: UUID, stat_data: dict) -> Stat:
    """
    Update a stat record.

    Args:
        db (AsyncSession): Database session.
        stat_id (UUID): The ID of the stat record.
        stat_data (dict): Data to update the stat record.

    Returns:
        Stat: The updated stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id)
    result = await db.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    for key, value in stat_data.items():
        setattr(stat, key, value)
    await db.commit()
    await db.refresh(stat)
    return stat


async def delete_stat(db: AsyncSession, stat_id: UUID) -> None:
    """
    Delete a stat record.

    Args:
        db (AsyncSession): Database session.
        stat_id (UUID): The ID of the stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id)
    result = await db.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    await db.delete(stat)
    await db.commit()


async def increment_post_views(db: AsyncSession, post_id: UUID) -> Stat:
    """
    Increment the view count for a post.

    Args:
        db (AsyncSession): Database session.
        post_id (UUID): The ID of the post.

    Returns:
        Stat: The updated stat record.
    """
    stat = await get_stat_by_post_id(db, post_id)
    stat.views += 1
    await db.commit()
    await db.refresh(stat)
    return stat


async def increment_post_likes(db: AsyncSession, post_id: UUID) -> Stat:
    """
    Increment the like count for a post.

    Args:
        db (AsyncSession): Database session.
        post_id (UUID): The ID of the post.

    Returns:
        Stat: The updated stat record.
    """
    stat = await get_stat_by_post_id(db, post_id)
    stat.likes += 1
    await db.commit()
    await db.refresh(stat)
    return stat


async def decrement_post_likes(db: AsyncSession, post_id: UUID) -> Stat:
    """
    Decrement the like count for a post.

    Args:
        db (AsyncSession): Database session.
        post_id (UUID): The ID of the post.

    Returns:
        Stat: The updated stat record.
    """
    stat = await get_stat_by_post_id(db, post_id)
    if stat.likes > 0:
        stat.likes -= 1
        await db.commit()
        await db.refresh(stat)
    return stat


async def get_site_stats(db: AsyncSession) -> dict:
    """
    Get overall site statistics.

    Args:
        db (AsyncSession): Database session.

    Returns:
        dict: Site statistics including total posts, users, views, and likes.
    """
    # Get total posts
    posts_query = select(Post)
    posts_result = await db.execute(posts_query)
    total_posts = len(posts_result.scalars().all())

    # Get total users
    users_query = select(User)
    users_result = await db.execute(users_query)
    total_users = len(users_result.scalars().all())

    # Get total views and likes
    stats_query = select(Stat)
    stats_result = await db.execute(stats_query)
    stats = stats_result.scalars().all()
    total_views = sum(stat.views for stat in stats)
    total_likes = sum(stat.likes for stat in stats)

    return {
        "total_posts": total_posts,
        "total_users": total_users,
        "total_views": total_views,
        "total_likes": total_likes
    }


async def get_user_stats(db: AsyncSession, user_id: UUID) -> dict:
    """
    Get statistics for a specific user.

    Args:
        db (AsyncSession): Database session.
        user_id (UUID): The ID of the user.

    Returns:
        dict: User statistics including posts count, total views, and total likes.
    """
    # Get user's posts
    posts_query = select(Post).where(Post.author_id == user_id)
    posts_result = await db.execute(posts_query)
    user_posts = posts_result.scalars().all()
    
    # Get stats for user's posts
    post_ids = [post.id for post in user_posts]
    stats_query = select(Stat).where(Stat.post_id.in_(post_ids))
    stats_result = await db.execute(stats_query)
    stats = stats_result.scalars().all()
    
    total_views = sum(stat.views for stat in stats)
    total_likes = sum(stat.likes for stat in stats)
    
    return {
        "user_id": user_id,
        "total_posts": len(user_posts),
        "total_views": total_views,
        "total_likes": total_likes
    }
