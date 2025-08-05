import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import comment as comment_crud
from app.db.session import get_session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate

router = APIRouter()


@router.get("/posts/{post_id}/comments", response_model=list[CommentRead])
async def read_comments_by_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> list[Comment]:
    """
    Get all comments for a specific post.
    """
    comments = await comment_crud.get_comments_by_post(db, post_id=post_id)
    return comments


@router.post("/posts/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment_for_post(
    post_id: uuid.UUID,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_session),
) -> Comment:
    """
    Add a comment to a post.
    """
    # Verify that the post exists
    from app.crud.post import get_post_by_id
    try:
        await get_post_by_id(db, post_id)
    except HTTPException:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create the comment
    comment = Comment(
        user_id=comment_in.user_id,
        post_id=post_id,  # Use the post_id from the path
        parent_comment_id=comment_in.parent_comment_id,
        content=comment_in.content
    )
    comment = await comment_crud.create_comment(db, comment)
    return comment


@router.get("/{comment_id}", response_model=CommentRead)
async def read_comment_by_id(
    comment_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Comment:
    """
    Get a specific comment by id.
    """
    comment = await comment_crud.get_comment_by_id(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment_by_id(
    comment_id: uuid.UUID,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(get_session),
) -> Comment:
    """
    Update a comment.
    """
    db_comment = await comment_crud.get_comment_by_id(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Update the comment with the new data
    update_data = comment_in.dict(exclude_unset=True)
    updated_comment = await comment_crud.update_comment(db, comment_id=comment_id, comment_data=update_data)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id(
    comment_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a comment.
    """
    comment = await comment_crud.get_comment_by_id(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    success = await comment_crud.delete_comment(db, comment_id=comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None


@router.post("/{comment_id}/reply", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def reply_to_comment(
    comment_id: uuid.UUID,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_session),
) -> Comment:
    """
    Reply to a comment.
    """
    # Verify that the parent comment exists
    parent_comment = await comment_crud.get_comment_by_id(db, comment_id=comment_id)
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    
    # Create the reply comment
    # The post_id should be the same as the parent comment's post_id
    comment = Comment(
        user_id=comment_in.user_id,
        post_id=parent_comment.post_id,
        parent_comment_id=comment_id,  # Reference to the parent comment
        content=comment_in.content
    )
    comment = await comment_crud.create_comment(db, comment)
    return comment


@router.get("/{comment_id}/replies", response_model=list[CommentRead])
async def read_replies_to_comment(
    comment_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> list[Comment]:
    """
    Get replies to a comment.
    """
    # Verify that the parent comment exists
    parent_comment = await comment_crud.get_comment_by_id(db, comment_id=comment_id)
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    
    replies = await comment_crud.get_replies_by_comment(db, comment_id=comment_id)
    return replies