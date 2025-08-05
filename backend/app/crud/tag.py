from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, or_

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


async def search_tags(
    db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
) -> tuple[list[Tag], int]:
    """
    Search tags by query string (name).
    """
    # Create the search query
    search_query = (
        select(Tag)
        .where(Tag.name.ilike(f"%{query}%"))
        .options(selectinload(Tag.posts))
    )
    
    # Get total count
    count_query = select(func.count()).select_from(search_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination
    paginated_query = search_query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    tags = result.scalars().all()
    
    return tags, total


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


async def update_tag(db: AsyncSession, tag_id: UUID, tag_update: dict) -> Tag | None:
    """
    Update a tag.

    Args:
        db (AsyncSession): Database session.
        tag_id (UUID): The ID of the tag to update.
        tag_update (dict): The updated tag data.

    Returns:
        Optional[Tag]: The updated tag, or None if not found.
    """
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for key, value in tag_update.items():
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


async def get_tag_by_name_or_slug(db: AsyncSession, name: str, slug: str) -> Tag | None:
    """
    Get a tag by its name or slug.

    Args:
        db (AsyncSession): Database session.
        name (str): The name of the tag to retrieve.
        slug (str): The slug of the tag to retrieve.

    Returns:
        Optional[Tag]: The retrieved tag, or None if not found.
    """
    statement = select(Tag).where((Tag.name == name) | (Tag.slug == slug))
    result = await db.execute(statement)
    return result.scalars().first()
