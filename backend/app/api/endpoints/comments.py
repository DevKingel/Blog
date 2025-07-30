from typing import List
from backend.app.crud.comment import (
    create_comment,
    delete_comment,
    get_all_comments,
    get_comment_by_id,
    update_comment,
)
from backend.app.db.session import get_db
from backend.app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/comments/", response_model=CommentRead)
async def create_comment_route(
    comment_in: CommentCreate, db: AsyncSession = Depends(get_db)
) -> CommentRead:
    """
    Create a new comment.

    Args:
        comment_in (CommentCreate): The comment data to create.
        db (AsyncSession): The database session.

    Returns:
        CommentRead: The created comment.
    """
    comment = await create_comment(comment_in, db)
    return comment


@router.get("/comments/{comment_id}", response_model=CommentRead)
async def get_comment_by_id_route(
    comment_id: int, db: AsyncSession = Depends(get_db)
) -> CommentRead:
    """
    Get a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.
        db (AsyncSession): The database session.

    Returns:
        CommentRead: The retrieved comment.

    Raises:
        HTTPException: If the comment is not found.
    """
    comment = await get_comment_by_id(comment_id, db)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.get("/comments/", response_model=List[CommentRead])
async def get_all_comments_route(
    db: AsyncSession = Depends(get_db),
) -> List[CommentRead]:
    """
    Get all comments.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[CommentRead]: A list of all comments.
    """
    comments = await get_all_comments(db)
    return comments


@router.put("/comments/{comment_id}", response_model=CommentRead)
async def update_comment_route(
    comment_id: int,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(get_db),
) -> CommentRead:
    """
    Update a comment.

    Args:
        comment_id (int): The ID of the comment to update.
        comment_in (CommentUpdate): The comment data to update.
        db (AsyncSession): The database session.

    Returns:
        CommentRead: The updated comment.

    Raises:
        HTTPException: If the comment is not found.
    """
    comment = await update_comment(comment_id, comment_in, db)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/comments/{comment_id}", response_model=None)
async def delete_comment_route(
    comment_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a comment.

    Args:
        comment_id (int): The ID of the comment to delete.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the comment is not found.
    """
    deleted = await delete_comment(comment_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
