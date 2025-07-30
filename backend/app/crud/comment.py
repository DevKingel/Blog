from backend.app.db.session import engine
from backend.app.models.comment import Comment
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, update


async def create_comment(comment: Comment) -> Comment:
    """
    Create a new comment.

    Args:
        comment (Comment): The comment object to create.

    Returns:
        Comment: The created comment object.
    """
    async with Session(engine) as session:
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment


async def get_comment_by_id(comment_id: int) -> Comment | None:
    """
    Get a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        Optional[Comment]: The retrieved comment object, or None if not found.
    """
    async with Session(engine) as session:
        statement = (
            select(Comment)
            .where(Comment.id == comment_id)
            .options(selectinload(Comment.user), selectinload(Comment.post))
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()


async def get_all_comments() -> list[Comment]:
    """
    Get all comments.

    Returns:
        List[Comment]: A list of all comment objects.
    """
    async with Session(engine) as session:
        statement = select(Comment).options(
            selectinload(Comment.user), selectinload(Comment.post)
        )
        result = await session.execute(statement)
        return result.scalars().all()


async def update_comment(comment_id: int, comment_data: dict) -> Comment | None:
    """
    Update a comment.

    Args:
        comment_id (int): The ID of the comment to update.
        comment_data (dict): The data to update the comment with.

    Returns:
        Optional[Comment]: The updated comment object, or None if not found.
    """
    async with Session(engine) as session:
        statement = (
            update(Comment).where(Comment.id == comment_id).values(**comment_data)
        )
        result = await session.execute(statement)
        if result.rowcount == 0:
            return None
        await session.commit()
        return await get_comment_by_id(comment_id)


async def delete_comment(comment_id: int) -> bool:
    """
    Delete a comment.

    Args:
        comment_id (int): The ID of the comment to delete.

    Returns:
        bool: True if the comment was deleted, False if not found.
    """
    async with Session(engine) as session:
        statement = delete(Comment).where(Comment.id == comment_id)
        result = await session.execute(statement)
        if result.rowcount == 0:
            return False
        await session.commit()
        return True
