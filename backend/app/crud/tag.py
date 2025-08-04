from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.tag import Tag


async def create_tag(db: AsyncSession, tag: Tag) -> Tag:
    """
    Create a new tag.

    Args:
        db (AsyncSession): Database session.
        tag (Tag): The tag to create.

    Returns:
        Tag: The created tag.
    """
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def get_tag_by_id(db: AsyncSession, tag_id: UUID) -> Tag | None:
    """
    Get a tag by its ID.

    Args:
        db (AsyncSession): Database session.
        tag_id (UUID): The ID of the tag to retrieve.

    Returns:
        Optional[Tag]: The retrieved tag, or None if not found.
    """
    statement = select(Tag).where(Tag.id == tag_id).options(selectinload(Tag.posts))
    result = await db.execute(statement)
    return result.scalars().first()


async def get_all_tags(db: AsyncSession) -> list[Tag]:
    """
    Get all tags.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[Tag]: A list of all tags.
    """
    statement = select(Tag).options(selectinload(Tag.posts))
    result = await db.execute(statement)
    return result.scalars().all()


async def update_tag(db: AsyncSession, tag_id: UUID, updated_tag: Tag) -> Tag | None:
    """
    Update a tag.

    Args:
        db (AsyncSession): Database session.
        tag_id (UUID): The ID of the tag to update.
        updated_tag (Tag): The updated tag data.

    Returns:
        Optional[Tag]: The updated tag, or None if not found.
    """
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for key, value in updated_tag.dict(exclude_unset=True).items():
        setattr(tag, key, value)
    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(db: AsyncSession, tag_id: UUID) -> bool:
    """
    Delete a tag.

    Args:
        db (AsyncSession): Database session.
        tag_id (UUID): The ID of the tag to delete.

    Returns:
        bool: True if the tag was deleted, False if not found.
    """
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await db.delete(tag)
    await db.commit()
    return True
