from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.post import Post


async def create_post(db: AsyncSession, post: Post) -> Post:
    """
    Create a new post in the database.

    Args:
        db (AsyncSession): Database session.
        post (Post): Post object to be created.

    Returns:
        Post: Created post object.
    """
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    """
    Get a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (int): ID of the post to retrieve.

    Returns:
        Optional[Post]: Retrieved post object or None if not found.
    """
    query = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def get_all_posts(db: AsyncSession) -> list[Post]:
    """
    Get all posts.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[Post]: List of all posts.
    """
    query = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.category),
        selectinload(Post.comments),
        selectinload(Post.tags),
        selectinload(Post.stat),
    )
    result = await db.execute(query)
    return result.scalars().all()


async def update_post(
    db: AsyncSession, post_id: int, updated_post: Post
) -> Post | None:
    """
    Update a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (int): ID of the post to update.
        updated_post (Post): Updated post object.

    Returns:
        Optional[Post]: Updated post object or None if not found.
    """
    query = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in updated_post.dict(exclude_unset=True).items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    """
    Delete a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (int): ID of the post to delete.

    Returns:
        bool: True if the post was deleted, False if not found.
    """
    query = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return True
