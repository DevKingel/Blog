import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from sqlmodel import select as sqlmodel_select

from app.models.comment import Comment


async def create_comment(db: AsyncSession, comment: Comment) -> Comment:
    """
    Create a new comment.

    Args:
        db (AsyncSession): Database session.
        comment (Comment): The comment object to create.

    Returns:
        Comment: The created comment object.
    """
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comment_by_id(db: AsyncSession, comment_id: uuid.UUID) -> Comment | None:
    """
    Get a comment by its ID.

    Args:
        db (AsyncSession): Database session.
        comment_id (uuid.UUID): The ID of the comment to retrieve.

    Returns:
        Optional[Comment]: The retrieved comment object, or None if not found.
    """
    statement = (
        select(Comment)
        .where(Comment.id == comment_id)
        .options(selectinload(Comment.user), selectinload(Comment.post))
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_all_comments(db: AsyncSession) -> list[Comment]:
    """
    Get all comments.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[Comment]: A list of all comment objects.
    """
    statement = select(Comment).options(
        selectinload(Comment.user), selectinload(Comment.post)
    )
    result = await db.execute(statement)
    return result.scalars().all()


async def get_comments_by_post(db: AsyncSession, post_id: uuid.UUID) -> list[Comment]:
    """
    Get all comments for a specific post.

    Args:
        db (AsyncSession): Database session.
        post_id (uuid.UUID): The ID of the post.

    Returns:
        List[Comment]: A list of comment objects for the post.
    """
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(selectinload(Comment.user), selectinload(Comment.post))
    )
    result = await db.execute(statement)
    return result.scalars().all()


async def get_comments_by_user(db: AsyncSession, user_id: uuid.UUID) -> list[Comment]:
    """
    Get all comments by a specific user.

    Args:
        db (AsyncSession): Database session.
        user_id (uuid.UUID): The ID of the user.

    Returns:
        List[Comment]: A list of comment objects by the user.
    """
    statement = (
        select(Comment)
        .where(Comment.user_id == user_id)
        .options(selectinload(Comment.user), selectinload(Comment.post))
    )
    result = await db.execute(statement)
    return result.scalars().all()


async def get_replies_by_comment(db: AsyncSession, comment_id: uuid.UUID) -> list[Comment]:
    """
    Get all replies to a specific comment.

    Args:
        db (AsyncSession): Database session.
        comment_id (uuid.UUID): The ID of the comment.

    Returns:
        List[Comment]: A list of reply comment objects.
    """
    statement = (
        select(Comment)
        .where(Comment.parent_comment_id == comment_id)
        .options(selectinload(Comment.user), selectinload(Comment.post))
    )
    result = await db.execute(statement)
    return result.scalars().all()


async def update_comment(db: AsyncSession, comment_id: uuid.UUID, comment_data: dict) -> Comment | None:
    """
    Update a comment.

    Args:
        db (AsyncSession): Database session.
        comment_id (uuid.UUID): The ID of the comment to update.
        comment_data (dict): The data to update the comment with.

    Returns:
        Optional[Comment]: The updated comment object, or None if not found.
    """
    statement = (
        update(Comment).where(Comment.id == comment_id).values(**comment_data)
    )
    result = await db.execute(statement)
    if result.rowcount == 0:
        return None
    await db.commit()
    return await get_comment_by_id(db, comment_id)


async def delete_comment(db: AsyncSession, comment_id: uuid.UUID) -> bool:
    """
    Delete a comment.

    Args:
        db (AsyncSession): Database session.
        comment_id (uuid.UUID): The ID of the comment to delete.

    Returns:
        bool: True if the comment was deleted, False if not found.
    """
    statement = delete(Comment).where(Comment.id == comment_id)
    result = await db.execute(statement)
    if result.rowcount == 0:
        return False
    await db.commit()
    return True
