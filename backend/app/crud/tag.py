from uuid import UUID
from backend.app.db.session import engine
from backend.app.models.tag import Tag
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import Session


async def create_tag(tag: Tag) -> Tag:
    """
    Create a new tag.

    Args:
        tag (Tag): The tag to create.

    Returns:
        Tag: The created tag.
    """
    async with Session(engine) as session:
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag


async def get_tag_by_id(tag_id: UUID) -> Tag | None:
    """
    Get a tag by its ID.

    Args:
        tag_id (UUID): The ID of the tag to retrieve.

    Returns:
        Optional[Tag]: The retrieved tag, or None if not found.
    """
    async with Session(engine) as session:
        statement = select(Tag).where(Tag.id == tag_id).options(selectinload(Tag.posts))
        result = await session.execute(statement)
        return result.scalars().first()


async def get_all_tags() -> list[Tag]:
    """
    Get all tags.

    Returns:
        List[Tag]: A list of all tags.
    """
    async with Session(engine) as session:
        statement = select(Tag).options(selectinload(Tag.posts))
        result = await session.execute(statement)
        return result.scalars().all()


async def update_tag(tag_id: UUID, updated_tag: Tag) -> Tag | None:
    """
    Update a tag.

    Args:
        tag_id (UUID): The ID of the tag to update.
        updated_tag (Tag): The updated tag data.

    Returns:
        Optional[Tag]: The updated tag, or None if not found.
    """
    async with Session(engine) as session:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.execute(statement)
        tag = result.scalars().first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        for key, value in updated_tag.dict(exclude_unset=True).items():
            setattr(tag, key, value)
        await session.commit()
        await session.refresh(tag)
        return tag


async def delete_tag(tag_id: UUID) -> bool:
    """
    Delete a tag.

    Args:
        tag_id (UUID): The ID of the tag to delete.

    Returns:
        bool: True if the tag was deleted, False if not found.
    """
    async with Session(engine) as session:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.execute(statement)
        tag = result.scalars().first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        await session.delete(tag)
        await session.commit()
        return True
