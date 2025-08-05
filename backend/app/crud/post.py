import uuid
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, or_

from app.models.post import Post
from app.models.post_tag import PostTag


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


async def get_post_by_id(db: AsyncSession, post_id: uuid.UUID) -> Post | None:
    """
    Get a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (uuid.UUID): ID of the post to retrieve.

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


async def get_posts_by_author(db: AsyncSession, author_id: uuid.UUID) -> list[Post]:
    """
    Get all posts by a specific author.

    Args:
        db (AsyncSession): Database session.
        author_id (uuid.UUID): ID of the author.

    Returns:
        List[Post]: List of posts by the author.
    """
    query = (
        select(Post)
        .where(Post.author_id == author_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    return result.scalars().all()


async def search_posts(
    db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
) -> tuple[list[Post], int]:
    """
    Search posts by query string (title or content).
    """
    # Create the search query
    search_query = (
        select(Post)
        .where(
            or_(
                Post.title.ilike(f"%{query}%"),
                Post.content.ilike(f"%{query}%")
            )
        )
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    
    # Get total count
    count_query = select(func.count()).select_from(search_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination
    paginated_query = search_query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    posts = result.scalars().all()
    
    return posts, total


async def update_post(
    db: AsyncSession, post_id: uuid.UUID, updated_post: Post
) -> Post | None:
    """
    Update a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (uuid.UUID): ID of the post to update.
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


async def delete_post(db: AsyncSession, post_id: uuid.UUID) -> bool:
    """
    Delete a post by its ID.

    Args:
        db (AsyncSession): Database session.
        post_id (uuid.UUID): ID of the post to delete.

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


async def get_posts_by_category(db: AsyncSession, category_id: UUID) -> list[Post]:
    """
    Get all posts in a specific category.

    Args:
        db (AsyncSession): Database session.
        category_id (UUID): ID of the category.

    Returns:
        List[Post]: List of posts in the category.
    """
    query = (
        select(Post)
        .where(Post.category_id == category_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_posts_by_tag(db: AsyncSession, tag_id: UUID) -> list[Post]:
    """
    Get all posts with a specific tag.

    Args:
        db (AsyncSession): Database session.
        tag_id (UUID): ID of the tag.

    Returns:
        List[Post]: List of posts with the tag.
    """
    query = (
        select(Post)
        .join(Post.tags)
        .where(PostTag.tag_id == tag_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments),
            selectinload(Post.tags),
            selectinload(Post.stat),
        )
    )
    result = await db.execute(query)
    return result.scalars().all()
