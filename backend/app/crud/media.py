import uuid
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


async def create_media(
    media: MediaCreate, user_id: UUID, db: AsyncSession = Depends(get_session)
) -> Media:
    """
    Create a new media entry in the database.

    Args:
        db (AsyncSession): Database session.
        media (MediaCreate): Media object to be created.
        user_id (UUID): ID of the user who owns the media.

    Returns:
        Media: Created media object.
    """
    db_media = Media(**media.model_dump(), user_id=user_id)
    db.add(db_media)
    await db.commit()
    await db.refresh(db_media)
    return db_media


async def get_media_by_id(
    media_id: uuid.UUID, db: AsyncSession = Depends(get_session)
) -> Media | None:
    """
    Get a media entry by its ID.

    Args:
        db (AsyncSession): Database session.
        media_id (uuid.UUID): ID of the media to retrieve.

    Returns:
        Optional[Media]: Retrieved media object or None if not found.
    """
    query = select(Media).where(Media.id == media_id).options(selectinload(Media.user))
    result = await db.execute(query)
    media = result.scalars().first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


async def get_all_media(
    *, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
) -> tuple[list[Media], int]:
    """
    Get all media entries with pagination.

    Args:
        db (AsyncSession): Database session.
        skip (int): Number of entries to skip.
        limit (int): Maximum number of entries to return.

    Returns:
        Tuple[List[Media], int]: List of media entries and total count.
    """
    # Create the query for media entries
    query = select(Media).options(selectinload(Media.user))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Apply pagination
    paginated_query = query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    media = result.scalars().all()

    return media, total


async def get_media_by_user(
    user_id: uuid.UUID,
    *,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
) -> tuple[list[Media], int]:
    """
    Get all media entries for a specific user with pagination.

    Args:
        db (AsyncSession): Database session.
        user_id (uuid.UUID): ID of the user.
        skip (int): Number of entries to skip.
        limit (int): Maximum number of entries to return.

    Returns:
        Tuple[List[Media], int]: List of media entries and total count.
    """
    # Create the query for media entries
    query = (
        select(Media).where(Media.user_id == user_id).options(selectinload(Media.user))
    )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Apply pagination
    paginated_query = query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    media = result.scalars().all()

    return media, total


async def update_media(
    media_id: uuid.UUID,
    updated_media: MediaUpdate,
    db: AsyncSession = Depends(get_session),
) -> Media | None:
    """
    Update a media entry by its ID.

    Args:
        db (AsyncSession): Database session.
        media_id (uuid.UUID): ID of the media to update.
        updated_media (MediaUpdate): Updated media object.

    Returns:
        Optional[Media]: Updated media object or None if not found.
    """
    query = select(Media).where(Media.id == media_id).options(selectinload(Media.user))
    result = await db.execute(query)
    media = result.scalars().first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    for key, value in updated_media.model_dump(exclude_unset=True).items():
        setattr(media, key, value)
    await db.commit()
    await db.refresh(media)
    return media


async def delete_media(
    media_id: uuid.UUID, db: AsyncSession = Depends(get_session)
) -> bool:
    """
    Delete a media entry by its ID.

    Args:
        db (AsyncSession): Database session.
        media_id (uuid.UUID): ID of the media to delete.

    Returns:
        bool: True if the media was deleted, False if not found.
    """
    query = select(Media).where(Media.id == media_id).options(selectinload(Media.user))
    result = await db.execute(query)
    media = result.scalars().first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    await db.delete(media)
    await db.commit()
    return True
