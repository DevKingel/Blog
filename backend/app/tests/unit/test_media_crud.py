import uuid
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.crud.media import (
    create_media,
    delete_media,
    get_all_media,
    get_media_by_id,
    get_media_by_user,
    update_media,
)
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


@pytest.mark.asyncio
async def test_create_media_success():
    """Test successful creation of a new media entry."""
    # Mock data
    user_id = uuid.uuid4()
    media_data = MediaCreate(
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
    )
    mock_created_media = Media(
        id=uuid.uuid4(),
        user_id=user_id,
        filename=media_data.filename,
        content_type=media_data.content_type,
        file_size=media_data.file_size,
        file_path=f"media/{media_data.filename}",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await create_media(media_data, user_id, mock_db)

    # Assertions
    assert isinstance(result, Media)
    assert result.filename == media_data.filename
    assert result.content_type == media_data.content_type
    assert result.file_size == media_data.file_size
    assert result.user_id == user_id
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_media_db_error():
    """Test handling of database error during media creation."""
    # Mock data
    user_id = uuid.uuid4()
    media_data = MediaCreate(
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await create_media(media_data, user_id, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_media_by_id_success():
    """Test successful retrieval of a media entry by ID."""
    # Mock data
    media_id = uuid.uuid4()
    user_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=user_id,
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_media
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_media_by_id(media_id, mock_db)

    # Assertions
    assert isinstance(result, Media)
    assert result.id == media_id
    assert result.filename == "test.jpg"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_media_by_id_not_found():
    """Test retrieval of a media entry by ID when not found."""
    # Mock data
    media_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        await get_media_by_id(media_id, mock_db)

    # Assertions
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Media not found"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_media_success():
    """Test successful retrieval of all media entries."""
    # Mock data
    user_id = uuid.uuid4()
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test2.png",
            content_type="image/png",
            file_size=2 * 1024 * 1024,
            file_path="media/test2.png",
        ),
    ]
    total_count = 2

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_all_media(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert total == total_count
    assert all(isinstance(media, Media) for media in result)
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_get_all_media_empty_result():
    """Test retrieval of all media entries when no media exists."""
    # Mock data
    mock_media = []
    total_count = 0

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_all_media(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    assert total == total_count
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_get_all_media_with_pagination():
    """Test retrieval of media entries with pagination."""
    # Mock data
    user_id = uuid.uuid4()
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
    ]
    total_count = 15
    skip = 10
    limit = 5

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_all_media(skip=skip, limit=limit, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert total == total_count
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_get_media_by_user_success():
    """Test successful retrieval of media entries by user ID."""
    # Mock data
    user_id = uuid.uuid4()
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test2.png",
            content_type="image/png",
            file_size=2 * 1024 * 1024,
            file_path="media/test2.png",
        ),
    ]
    total_count = 2

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_media_by_user(user_id, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert total == total_count
    assert all(isinstance(media, Media) for media in result)
    assert all(media.user_id == user_id for media in result)
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_get_media_by_user_empty_result():
    """Test retrieval of media entries by user ID when no media exists."""
    # Mock data
    user_id = uuid.uuid4()
    mock_media = []
    total_count = 0

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_media_by_user(user_id, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    assert total == total_count
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_get_media_by_user_with_pagination():
    """Test retrieval of media entries by user ID with pagination."""
    # Mock data
    user_id = uuid.uuid4()
    mock_media = [
        Media(
            id=uuid.uuid4(),
            user_id=user_id,
            filename="test1.jpg",
            content_type="image/jpeg",
            file_size=1024 * 1024,
            file_path="media/test1.jpg",
        ),
    ]
    total_count = 15
    skip = 10
    limit = 5

    # Mock dependencies
    mock_db = AsyncMock()
    
    # Mock results for media query
    mock_media_result = Mock()
    mock_media_result.scalars().all.return_value = mock_media
    
    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count
    
    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_media_result
    
    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await get_media_by_user(user_id, skip=skip, limit=limit, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert total == total_count
    assert all(media.user_id == user_id for media in result)
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_update_media_success():
    """Test successful update of a media entry."""
    # Mock data
    media_id = uuid.uuid4()
    user_id = uuid.uuid4()
    update_data = MediaUpdate(filename="updated_test.jpg")
    existing_media = Media(
        id=media_id,
        user_id=user_id,
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )
    updated_media = Media(
        id=media_id,
        user_id=user_id,
        filename="updated_test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = existing_media
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_media(media_id, update_data, mock_db)

    # Assertions
    assert isinstance(result, Media)
    assert result.filename == "updated_test.jpg"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_media_not_found():
    """Test update of a non-existent media entry."""
    # Mock data
    media_id = uuid.uuid4()
    update_data = MediaUpdate(filename="updated_test.jpg")

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        await update_media(media_id, update_data, mock_db)

    # Assertions
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Media not found"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_update_media_partial_data():
    """Test update of a media entry with partial data."""
    # Mock data
    media_id = uuid.uuid4()
    user_id = uuid.uuid4()
    update_data = MediaUpdate()  # Empty update
    existing_media = Media(
        id=media_id,
        user_id=user_id,
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = existing_media
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_media(media_id, update_data, mock_db)

    # Assertions
    assert isinstance(result, Media)
    assert result.filename == "test.jpg"  # Should remain unchanged
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_media_db_error():
    """Test handling of database error during media update."""
    # Mock data
    media_id = uuid.uuid4()
    update_data = MediaUpdate(filename="updated_test.jpg")

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Database error")

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await update_media(media_id, update_data, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_media_success():
    """Test successful deletion of a media entry."""
    # Mock data
    media_id = uuid.uuid4()
    user_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=user_id,
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_media
    mock_db.execute.return_value = mock_result
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()

    # Call the function
    result = await delete_media(media_id, mock_db)

    # Assertions
    assert result is True
    mock_db.execute.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_media)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_media_not_found():
    """Test deletion of a non-existent media entry."""
    # Mock data
    media_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    # Verify that the HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        await delete_media(media_id, mock_db)

    # Assertions
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Media not found"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_media_db_error():
    """Test handling of database error during media deletion."""
    # Mock data
    media_id = uuid.uuid4()
    user_id = uuid.uuid4()
    mock_media = Media(
        id=media_id,
        user_id=user_id,
        filename="test.jpg",
        content_type="image/jpeg",
        file_size=1024 * 1024,
        file_path="media/test.jpg",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().first.return_value = mock_media
    mock_db.execute.return_value = mock_result
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await delete_media(media_id, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.execute.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_media)
    mock_db.commit.assert_awaited_once()
