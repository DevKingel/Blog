import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import media as media_crud
from app.db.session import get_session
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaRead, MediaUpdate

# Create the media directory if it doesn't exist
MEDIA_DIR = Path(__file__).parent.parent.parent.parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

# Define allowed file types and size limits
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
    "text/plain",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter()


@router.post("/", response_model=MediaRead, status_code=status.HTTP_201_CREATED)
async def upload_media(
    *,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
) -> Media:
    """
    Upload a new media file.

    Args:
        file (UploadFile): The file to upload.
        db (AsyncSession): Database session.

    Returns:
        Media: Created media object.

    Raises:
        HTTPException: If file type is not allowed or file size exceeds limit.
    """
    # Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Allowed types: {ALLOWED_CONTENT_TYPES}",
        )

    # Validate file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds limit of {MAX_FILE_SIZE} bytes",
        )

    # Generate a unique filename
    file_extension = Path(file.filename).suffix if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = MEDIA_DIR / unique_filename

    # Save the file
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # Read in 1MB chunks
            buffer.write(chunk)

    # Create media record in database
    # Store relative path from backend/app directory
    relative_path = f"media/{unique_filename}"
    media_in = MediaCreate(
        filename=file.filename or unique_filename,
        content_type=file.content_type,
        file_size=file_size,
        file_path=relative_path,
    )
    
    # For now, we'll use a placeholder user_id
    # In a real implementation, this would come from the authenticated user
    user_id = uuid.uuid4()  # Placeholder
    
    media = await media_crud.create_media(db, media_in, user_id)
    return media


@router.get("/", response_model=List[MediaRead])
async def list_media(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
) -> List[Media]:
    """
    List all uploaded media with pagination.

    Args:
        skip (int): Number of entries to skip.
        limit (int): Maximum number of entries to return.
        db (AsyncSession): Database session.

    Returns:
        List[Media]: List of media entries.
    """
    media, total = await media_crud.get_all_media(db, skip=skip, limit=limit)
    return media


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    *,
    media_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a media entry and its associated file.

    Args:
        media_id (uuid.UUID): ID of the media to delete.
        db (AsyncSession): Database session.

    Raises:
        HTTPException: If media entry is not found.
    """
    # Get the media entry to get the file path
    media = await media_crud.get_media_by_id(db, media_id)
    
    # Delete the file from storage
    try:
        # Construct full path from backend/app directory
        full_path = Path(__file__).parent.parent.parent.parent / media.file_path
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        # Log the error but continue with database deletion
        print(f"Error deleting file {media.file_path}: {e}")
    
    # Delete the media entry from database
    await media_crud.delete_media(db, media_id)
    return None