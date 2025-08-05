from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import engine
from app.models.post_tag import PostTag


async def create_post_tag(post_id: UUID, tag_id: UUID) -> PostTag:
    """
    Create a new post-tag relationship.
    """
    post_tag = PostTag(post_id=post_id, tag_id=tag_id)
    engine.add(post_tag)
    await engine.commit()
    await engine.refresh(post_tag)
    return post_tag


async def get_post_tag_by_ids(post_id: UUID, tag_id: UUID) -> PostTag | None:
    """
    Get a post-tag relationship by post and tag IDs.
    """
    query = (
        select(PostTag)
        .where(PostTag.post_id == post_id, PostTag.tag_id == tag_id)
        .options(selectinload(PostTag.post), selectinload(PostTag.tag))
    )
    result = await engine.execute(query)
    return result.scalars().first()


async def get_all_post_tags() -> list[PostTag]:
    """
    Get all post-tag relationships.
    """
    query = select(PostTag).options(
        selectinload(PostTag.post), selectinload(PostTag.tag)
    )
    result = await engine.execute(query)
    return result.scalars().all()


async def update_post_tag(
    post_id: UUID, tag_id: UUID, new_post_id: UUID, new_tag_id: UUID
) -> PostTag | None:
    """
    Update a post-tag relationship.
    """
    post_tag = await get_post_tag_by_ids(post_id, tag_id)
    if not post_tag:
        raise HTTPException(status_code=404, detail="PostTag not found")
    post_tag.post_id = new_post_id
    post_tag.tag_id = new_tag_id
    await engine.commit()
    await engine.refresh(post_tag)
    return post_tag


async def delete_post_tag(post_id: UUID, tag_id: UUID) -> bool:
    """
    Delete a post-tag relationship.
    """
    post_tag = await get_post_tag_by_ids(post_id, tag_id)
    if not post_tag:
        raise HTTPException(status_code=404, detail="PostTag not found")
    await engine.delete(post_tag)
    await engine.commit()
    return True
