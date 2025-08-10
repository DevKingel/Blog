import os
import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, UploadFile, status

from app.api.v1.endpoints.media import delete_media, list_media, upload_media
from app.models.media import Media


@pytest.mark.asyncio
async def test_upload_media_success():
    """Test successful media upload."""
    # Create a mock file
    mock_file = Mock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "test.jpg"
    mock_file.file = Mock()
    mock_file.file.seek = Mock()
    mock_file.file.tell = Mock(return_value=1024 * 1024)  # 1MB
    mock_file.read = AsyncMock(return_value=b"fake image data")

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function
    with patch(
        "app.api.v1.endpoints.media.media_crud.create_media"
    ) as mock_create_media:
        mock_create_media.return_value = Media(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            filename="test.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test.jpg",
        )

        # Mock file writing
        with patch("app.api.v1.endpoints.media.open", Mock()):
            # Call the endpoint
            result = await upload_media(file=mock_file, db=mock_db)

            # Assertions
            assert result.filename == "test.jpg"
            assert result.content_type == "image/jpeg"
            assert result.file_size == 1024 * 1024
            mock_create_media.assert_called_once()
            mock_file.file.seek.assert_any_call(0, os.SEEK_END)
            mock_file.file.seek.assert_any_call(0)


@pytest.mark.asyncio
async def test_upload_media_invalid_content_type():
    """Test media upload with invalid content type."""
    # Create a mock file with invalid content type
    mock_file = Mock(spec=UploadFile)
    mock_file.content_type = "application/exe"
    mock_file.filename = "malicious.exe"

    # Create a mock database session
    mock_db = AsyncMock()

    # Call the endpoint and expect HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await upload_media(file=mock_file, db=mock_db)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "not allowed" in exc_info.value.detail


@pytest.mark.asyncio
async def test_upload_media_file_too_large():
    """Test media upload with file that exceeds size limit."""
    # Create a mock file that's too large
    mock_file = Mock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "large.jpg"
    mock_file.file = Mock()
    mock_file.file.seek = Mock()
    mock_file.file.tell = Mock(
        return_value=15 * 1024 * 1024
    )  # 15MB (exceeds 10MB limit)

    # Create a mock database session
    mock_db = AsyncMock()

    # Call the endpoint and expect HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await upload_media(file=mock_file, db=mock_db)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert "exceeds limit" in exc_info.value.detail


@pytest.mark.asyncio
async def test_upload_media_db_error():
    """Test media upload when database operation fails."""
    # Create a mock file
    mock_file = Mock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "test.jpg"
    mock_file.file = Mock()
    mock_file.file.seek = Mock()
    mock_file.file.tell = Mock(return_value=1024 * 1024)  # 1MB
    mock_file.read = AsyncMock(return_value=b"fake image data")

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function to raise an exception
    with patch(
        "app.api.v1.endpoints.media.media_crud.create_media"
    ) as mock_create_media:
        mock_create_media.side_effect = Exception("Database error")

        # Mock file writing
        with patch("app.api.v1.endpoints.media.open", Mock()):
            # Mock file removal
            with patch("app.api.v1.endpoints.media.os.remove") as mock_remove:
                # Call the endpoint and expect exception
                with pytest.raises(HTTPException) as exc_info:
                    await upload_media(file=mock_file, db=mock_db)

                # Assertions
                assert exc_info.value.status_code == 500
                assert (
                    exc_info.value.detail
                    == "Internal server error while uploading media"
                )

                # Verify file cleanup occurred
                mock_remove.assert_called_once()


@pytest.mark.asyncio
async def test_upload_media_file_write_error():
    """Test media upload when file writing fails."""
    # Create a mock file
    mock_file = Mock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "test.jpg"
    mock_file.file = Mock()
    mock_file.file.seek = Mock()
    mock_file.file.tell = Mock(return_value=1024 * 1024)  # 1MB
    mock_file.read = AsyncMock(return_value=b"fake image data")

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock file writing to raise an exception
    with patch("app.api.v1.endpoints.media.open") as mock_open:
        mock_open.side_effect = Exception("File write error")

        # Call the endpoint and expect exception
        with pytest.raises(HTTPException) as exc_info:
            await upload_media(file=mock_file, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while uploading media"


@pytest.mark.asyncio
async def test_list_media_success():
    """Test successful listing of media."""
    # Create mock media items
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
        Media(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            filename="test2.png",
            content_type="image/png",
            file_size=2 * 1024 * 1024,
            file_path="media/test2.png",
        ),
    ]

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function
    with patch(
        "app.api.v1.endpoints.media.media_crud.get_all_media"
    ) as mock_get_all_media:
        mock_get_all_media.return_value = (mock_media, 2)

        # Call the endpoint
        result = await list_media(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].filename == "test1.jpg"
        assert result[1].filename == "test2.png"
        mock_get_all_media.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_list_media_with_pagination():
    """Test listing of media with custom pagination."""
    # Create mock media items
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
    ]

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function
    with patch(
        "app.api.v1.endpoints.media.media_crud.get_all_media"
    ) as mock_get_all_media:
        mock_get_all_media.return_value = (mock_media, 1)

        # Call the endpoint with custom pagination
        result = await list_media(skip=10, limit=5, db=mock_db)

        # Assertions
        assert len(result) == 1
        mock_get_all_media.assert_called_once_with(mock_db, skip=10, limit=5)


@pytest.mark.asyncio
async def test_list_media_empty_result():
    """Test listing of media when no media exists."""
    # Create empty mock media list
    mock_media = []

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function
    with patch(
        "app.api.v1.endpoints.media.media_crud.get_all_media"
    ) as mock_get_all_media:
        mock_get_all_media.return_value = (mock_media, 0)

        # Call the endpoint
        result = await list_media(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_all_media.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_list_media_db_error():
    """Test handling of database error in media listing."""
    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function to raise an exception
    with patch(
        "app.api.v1.endpoints.media.media_crud.get_all_media"
    ) as mock_get_all_media:
        mock_get_all_media.side_effect = Exception("Database error")

        # Call the endpoint and expect exception
        with pytest.raises(HTTPException) as exc_info:
            await list_media(skip=0, limit=100, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while listing media"


@pytest.mark.asyncio
async def test_delete_media_success():
    """Test successful deletion of media."""
    # Create a mock media item
    media_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=uuid.uuid4(),
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.media.media_crud.get_media_by_id"
        ) as mock_get_media,
        patch(
            "app.api.v1.endpoints.media.media_crud.delete_media"
        ) as mock_delete_media,
        patch("app.api.v1.endpoints.media.os.path.exists") as mock_exists,
        patch("app.api.v1.endpoints.media.os.remove") as mock_remove,
    ):
        mock_get_media.return_value = mock_media
        mock_exists.return_value = True
        mock_delete_media.return_value = True

        # Call the endpoint
        result = await delete_media(media_id=media_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_media.assert_called_once_with(mock_db, media_id)
        mock_delete_media.assert_called_once_with(mock_db, media_id)
        mock_remove.assert_called_once()


@pytest.mark.asyncio
async def test_delete_media_not_found():
    """Test deletion of non-existent media."""
    # Create a media ID
    media_id = uuid.uuid4()

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD function to raise HTTPException
    with patch(
        "app.api.v1.endpoints.media.media_crud.get_media_by_id"
    ) as mock_get_media:
        mock_get_media.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await delete_media(media_id=media_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Media not found"


@pytest.mark.asyncio
async def test_delete_media_file_not_found():
    """Test deletion of media when file does not exist."""
    # Create a mock media item
    media_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=uuid.uuid4(),
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.media.media_crud.get_media_by_id"
        ) as mock_get_media,
        patch(
            "app.api.v1.endpoints.media.media_crud.delete_media"
        ) as mock_delete_media,
        patch("app.api.v1.endpoints.media.os.path.exists") as mock_exists,
    ):
        mock_get_media.return_value = mock_media
        mock_exists.return_value = False  # File does not exist
        mock_delete_media.return_value = True

        # Call the endpoint
        result = await delete_media(media_id=media_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_media.assert_called_once_with(mock_db, media_id)
        mock_delete_media.assert_called_once_with(mock_db, media_id)


@pytest.mark.asyncio
async def test_delete_media_file_deletion_error():
    """Test deletion of media when file deletion fails."""
    # Create a mock media item
    media_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=uuid.uuid4(),
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.media.media_crud.get_media_by_id"
        ) as mock_get_media,
        patch(
            "app.api.v1.endpoints.media.media_crud.delete_media"
        ) as mock_delete_media,
        patch("app.api.v1.endpoints.media.os.path.exists") as mock_exists,
        patch("app.api.v1.endpoints.media.os.remove") as mock_remove,
        patch("app.api.v1.endpoints.media.print") as mock_print,
    ):
        mock_get_media.return_value = mock_media
        mock_exists.return_value = True
        mock_delete_media.return_value = True
        mock_remove.side_effect = Exception("Permission denied")  # File deletion fails

        # Call the endpoint
        result = await delete_media(media_id=media_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_media.assert_called_once_with(mock_db, media_id)
        mock_delete_media.assert_called_once_with(mock_db, media_id)
        mock_remove.assert_called_once()
        mock_print.assert_called_once()  # Error should be logged


@pytest.mark.asyncio
async def test_delete_media_db_error():
    """Test handling of database error during media deletion."""
    # Create a mock media item
    media_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=uuid.uuid4(),
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Create a mock database session
    mock_db = AsyncMock()

    # Mock the media CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.media.media_crud.get_media_by_id"
        ) as mock_get_media,
        patch(
            "app.api.v1.endpoints.media.media_crud.delete_media"
        ) as mock_delete_media,
        patch("app.api.v1.endpoints.media.os.path.exists") as mock_exists,
        patch("app.api.v1.endpoints.media.os.remove") as mock_remove,
    ):
        mock_get_media.return_value = mock_media
        mock_exists.return_value = True
        mock_remove.return_value = None
        mock_delete_media.side_effect = Exception("Database error")

        # Call the endpoint and expect exception
        with pytest.raises(HTTPException) as exc_info:
            await delete_media(media_id=media_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while deleting media"

        # Verify file was deleted but exception was raised
        mock_remove.assert_called_once()
