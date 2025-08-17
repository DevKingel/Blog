import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.tags import (
    create_new_tag,
    delete_tag_by_id,
    get_posts_with_tag,
    read_tag_by_id,
    read_tags,
    update_existing_tag,
)
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


@pytest.mark.asyncio
async def test_create_tag_success():
    """Test successful tag creation."""
    # Create test data
    tag_in = TagCreate(name="Python", slug="python")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.tags.tag_crud.get_tag_by_name_or_slug"
        ) as mock_get_by_name_or_slug,
        patch("app.api.v1.endpoints.tags.tag_crud.create_tag") as mock_create_tag,
    ):
        # Configure mocks
        mock_get_by_name_or_slug.return_value = None  # No existing tag
        mock_create_tag.return_value = Tag(
            id=uuid.uuid4(), name="Python", slug="python"
        )

        # Call the endpoint
        result = await create_new_tag(tag_in=tag_in, db=mock_db)

        # Assertions
        assert isinstance(result, Tag)
        assert result.name == "Python"
        assert result.slug == "python"
        mock_get_by_name_or_slug.assert_called_once_with(
            mock_db, name="Python", slug="python"
        )
        mock_create_tag.assert_called_once()


@pytest.mark.asyncio
async def test_create_tag_duplicate_name():
    """Test tag creation with duplicate name."""
    # Create test data
    tag_in = TagCreate(name="Python", slug="python")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return an existing tag
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_name_or_slug"
    ) as mock_get_by_name_or_slug:
        # Configure mock to return an existing tag
        mock_get_by_name_or_slug.return_value = Tag(
            id=uuid.uuid4(), name="Python", slug="python-old"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await create_new_tag(tag_in=tag_in, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail
        mock_get_by_name_or_slug.assert_called_once_with(
            mock_db, name="Python", slug="python"
        )


@pytest.mark.asyncio
async def test_create_tag_duplicate_slug():
    """Test tag creation with duplicate slug."""
    # Create test data
    tag_in = TagCreate(name="Python Programming", slug="python")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return an existing tag
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_name_or_slug"
    ) as mock_get_by_name_or_slug:
        # Configure mock to return an existing tag with same slug
        mock_get_by_name_or_slug.return_value = Tag(
            id=uuid.uuid4(), name="Python", slug="python"
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await create_new_tag(tag_in=tag_in, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail
        mock_get_by_name_or_slug.assert_called_once_with(
            mock_db, name="Python Programming", slug="python"
        )


@pytest.mark.asyncio
async def test_read_tags_success():
    """Test successful retrieval of all tags."""
    # Create mock tags
    mock_tags = [
        Tag(id=uuid.uuid4(), name="Python", slug="python"),
        Tag(id=uuid.uuid4(), name="JavaScript", slug="javascript"),
    ]

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch("app.api.v1.endpoints.tags.tag_crud.get_all_tags") as mock_get_all_tags:
        mock_get_all_tags.return_value = mock_tags

        # Call the endpoint
        result = await read_tags(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].name == "Python"
        assert result[1].name == "JavaScript"
        mock_get_all_tags.assert_called_once_with(mock_db)


@pytest.mark.asyncio
async def test_read_tags_empty():
    """Test retrieval of tags when none exist."""
    # Create empty mock tags list
    mock_tags = []

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch("app.api.v1.endpoints.tags.tag_crud.get_all_tags") as mock_get_all_tags:
        mock_get_all_tags.return_value = mock_tags

        # Call the endpoint
        result = await read_tags(skip=0, limit=100, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_all_tags.assert_called_once_with(mock_db)


@pytest.mark.asyncio
async def test_read_tag_by_id_success():
    """Test successful retrieval of a tag by ID."""
    # Create a tag ID and mock tag
    tag_id = uuid.uuid4()
    mock_tag = Tag(id=tag_id, name="Python", slug="python")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_id"
    ) as mock_get_tag_by_id:
        mock_get_tag_by_id.return_value = mock_tag

        # Call the endpoint
        result = await read_tag_by_id(tag_id=tag_id, db=mock_db)

        # Assertions
        assert isinstance(result, Tag)
        assert result.id == tag_id
        assert result.name == "Python"
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_read_tag_by_id_not_found():
    """Test retrieval of a non-existent tag by ID."""
    # Create a tag ID
    tag_id = uuid.uuid4()

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return None
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_id"
    ) as mock_get_tag_by_id:
        mock_get_tag_by_id.return_value = None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await read_tag_by_id(tag_id=tag_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_update_tag_success():
    """Test successful tag update."""
    # Create test data
    tag_id = uuid.uuid4()
    tag_update = TagUpdate(name="Python 3")

    # Create mock tags
    existing_tag = Tag(id=tag_id, name="Python", slug="python")
    updated_tag = Tag(id=tag_id, name="Python 3", slug="python")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD functions
    with (
        patch("app.api.v1.endpoints.tags.tag_crud.get_tag_by_id") as mock_get_tag_by_id,
        patch(
            "app.api.v1.endpoints.tags.tag_crud.get_tag_by_name_or_slug"
        ) as mock_get_by_name_or_slug,
        patch("app.api.v1.endpoints.tags.tag_crud.update_tag") as mock_update_tag,
    ):
        # Configure mocks
        mock_get_tag_by_id.return_value = existing_tag
        mock_get_by_name_or_slug.return_value = None  # No conflicts
        mock_update_tag.return_value = updated_tag

        # Call the endpoint
        result = await update_existing_tag(tag_id=tag_id, tag_in=tag_update, db=mock_db)

        # Assertions
        assert isinstance(result, Tag)
        assert result.name == "Python 3"
        assert result.slug == "python"
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)
        mock_get_by_name_or_slug.assert_called_once_with(
            mock_db, name="Python 3", slug="python"
        )
        mock_update_tag.assert_called_once()


@pytest.mark.asyncio
async def test_update_tag_not_found():
    """Test update of a non-existent tag."""
    # Create test data
    tag_id = uuid.uuid4()
    tag_update = TagUpdate(name="Python 3")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return None
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_id"
    ) as mock_get_tag_by_id:
        mock_get_tag_by_id.return_value = None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_tag(tag_id=tag_id, tag_in=tag_update, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert "does not exist" in exc_info.value.detail
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_update_tag_duplicate_name():
    """Test tag update with duplicate name."""
    # Create test data
    tag_id = uuid.uuid4()
    tag_update = TagUpdate(name="JavaScript")

    # Create mock tags
    existing_tag = Tag(id=tag_id, name="Python", slug="python")
    conflicting_tag = Tag(id=uuid.uuid4(), name="JavaScript", slug="javascript")

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD functions
    with (
        patch("app.api.v1.endpoints.tags.tag_crud.get_tag_by_id") as mock_get_tag_by_id,
        patch(
            "app.api.v1.endpoints.tags.tag_crud.get_tag_by_name_or_slug"
        ) as mock_get_by_name_or_slug,
    ):
        # Configure mocks
        mock_get_tag_by_id.return_value = existing_tag
        mock_get_by_name_or_slug.return_value = (
            conflicting_tag  # Conflict with existing tag
        )

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_tag(tag_id=tag_id, tag_in=tag_update, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)
        mock_get_by_name_or_slug.assert_called_once_with(
            mock_db, name="JavaScript", slug="python"
        )


@pytest.mark.asyncio
async def test_delete_tag_success():
    """Test successful tag deletion."""
    # Create a tag ID
    tag_id = uuid.uuid4()

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function
    with patch("app.api.v1.endpoints.tags.tag_crud.delete_tag") as mock_delete_tag:
        mock_delete_tag.return_value = True

        # Call the endpoint
        result = await delete_tag_by_id(tag_id=tag_id, db=mock_db)

        # Assertions
        assert result is None
        mock_delete_tag.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_delete_tag_not_found():
    """Test deletion of a non-existent tag."""
    # Create a tag ID
    tag_id = uuid.uuid4()

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return False
    with patch("app.api.v1.endpoints.tags.tag_crud.delete_tag") as mock_delete_tag:
        mock_delete_tag.return_value = False

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await delete_tag_by_id(tag_id=tag_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail
        mock_delete_tag.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_get_posts_with_tag_success():
    """Test successful retrieval of posts with a specific tag."""
    # Create a tag ID and mock data
    tag_id = uuid.uuid4()
    mock_tag = Tag(id=tag_id, name="Python", slug="python")
    mock_posts = [
        Post(id=uuid.uuid4(), title="Post 1", content="Content 1"),
        Post(id=uuid.uuid4(), title="Post 2", content="Content 2"),
    ]

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD functions
    with (
        patch("app.api.v1.endpoints.tags.tag_crud.get_tag_by_id") as mock_get_tag_by_id,
        patch("app.api.v1.endpoints.tags.get_posts_by_tag") as mock_get_posts_by_tag,
    ):
        # Configure mocks
        mock_get_tag_by_id.return_value = mock_tag
        mock_get_posts_by_tag.return_value = mock_posts

        # Call the endpoint
        result = await get_posts_with_tag(tag_id=tag_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].title == "Post 1"
        assert result[1].title == "Post 2"
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)
        mock_get_posts_by_tag.assert_called_once_with(mock_db, tag_id=tag_id)


@pytest.mark.asyncio
async def test_get_posts_with_tag_not_found():
    """Test retrieval of posts with a non-existent tag."""
    # Create a tag ID
    tag_id = uuid.uuid4()

    # Create a mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the tag CRUD function to return None
    with patch(
        "app.api.v1.endpoints.tags.tag_crud.get_tag_by_id"
    ) as mock_get_tag_by_id:
        mock_get_tag_by_id.return_value = None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_posts_with_tag(tag_id=tag_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail
        mock_get_tag_by_id.assert_called_once_with(mock_db, tag_id=tag_id)
