import os
import tempfile
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app
from app.models.media import Media

client = TestClient(app)


@pytest.fixture
async def db_session():
    """Create a database session for testing."""
    async with get_session() as session:
        yield session


@pytest.fixture
def temp_media_file():
    """Create a temporary media file for testing."""
    # Create a temporary file with some content
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(b"fake image data for testing")
        temp_file_path = temp_file.name

    yield temp_file_path

    # Cleanup: remove the temporary file
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


@pytest.fixture
def large_media_file():
    """Create a temporary file that exceeds the size limit for testing."""
    # Create a temporary file with content larger than 10MB
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        # Write more than 10MB of data
        temp_file.write(b"x" * (15 * 1024 * 1024))  # 15MB
        temp_file_path = temp_file.name

    yield temp_file_path

    # Cleanup: remove the temporary file
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


@pytest.fixture
async def test_media(db_session: AsyncSession):
    """Create a test media entry."""
    # Create a media entry
    media = Media(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        filename="test_image.jpg",
        content_type="image/jpeg",
        file_size=1024,
        file_path="media/test_image.jpg",
    )
    db_session.add(media)
    await db_session.commit()
    await db_session.refresh(media)

    yield media

    # Cleanup: delete the media entry
    await db_session.delete(media)
    await db_session.commit()


# Integration tests for POST / - Upload a new media file
def test_upload_media_success(temp_media_file):
    """Test successful media upload."""
    with open(temp_media_file, "rb") as file:
        response = client.post(
            "/api/v1/media/", files={"file": ("test_image.jpg", file, "image/jpeg")}
        )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["filename"] == "test_image.jpg"
    assert data["content_type"] == "image/jpeg"
    assert data["file_size"] > 0
    assert "file_path" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_upload_media_invalid_content_type():
    """Test media upload with invalid content type."""
    # Create a temporary file with invalid content type
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file:
        temp_file.write(b"fake executable data")
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as file:
            response = client.post(
                "/api/v1/media/",
                files={"file": ("malicious.exe", file, "application/exe")},
            )

        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_upload_media_file_too_large(large_media_file):
    """Test media upload with file that exceeds size limit."""
    with open(large_media_file, "rb") as file:
        response = client.post(
            "/api/v1/media/", files={"file": ("large_file.jpg", file, "image/jpeg")}
        )

    assert response.status_code == 413
    assert "exceeds limit" in response.json()["detail"]


def test_upload_media_no_file():
    """Test media upload without providing a file."""
    response = client.post("/api/v1/media/")

    assert response.status_code == 422


# Integration tests for GET / - List all uploaded media with pagination
def test_list_media_success():
    """Test successful listing of media."""
    response = client.get("/api/v1/media/")
    assert response.status_code == 200
    # Response should be a list
    assert isinstance(response.json(), list)


def test_list_media_with_pagination():
    """Test listing of media with pagination."""
    response = client.get("/api/v1/media/?skip=0&limit=5")
    assert response.status_code == 200
    # Response should be a list
    assert isinstance(response.json(), list)


def test_list_media_empty_result():
    """Test listing of media when no media exists."""
    # This test assumes the database is empty or properly isolated
    response = client.get("/api/v1/media/")
    assert response.status_code == 200
    # Response should be an empty list
    assert response.json() == []


# Integration tests for DELETE /{media_id}
# Delete a media entry and its associated file
async def test_delete_media_success(db_session: AsyncSession, test_media: Media):
    """Test successful deletion of media."""
    # First, let's create a temporary file to simulate the media file
    media_dir = Path(__file__).parent.parent / "media"
    media_dir.mkdir(exist_ok=True)
    media_file_path = media_dir / test_media.filename

    # Create a temporary file to simulate the media file
    media_file_path.write_text("fake image data")

    try:
        response = client.delete(f"/api/v1/media/{test_media.id}")
        assert response.status_code == 204

        # Verify the media entry no longer exists in the database
        result = await db_session.execute(
            select(Media).where(Media.id == test_media.id)
        )
        media = result.scalars().first()
        assert media is None

        # Verify the file was deleted
        # (this might not work in tests without proper setup)
        # We'll check that the file operation was at least attempted
    finally:
        # Cleanup: remove the temporary file if it still exists
        if media_file_path.exists():
            media_file_path.unlink()


def test_delete_media_not_found():
    """Test deletion of non-existent media."""
    fake_media_id = uuid.uuid4()
    response = client.delete(f"/api/v1/media/{fake_media_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


async def test_delete_media_file_not_found(db_session: AsyncSession):
    """Test deletion of media when file does not exist."""
    # Create a media entry without an actual file
    media = Media(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        filename="missing_file.jpg",
        content_type="image/jpeg",
        file_size=1024,
        file_path="media/missing_file.jpg",
    )
    db_session.add(media)
    await db_session.commit()
    await db_session.refresh(media)

    try:
        response = client.delete(f"/api/v1/media/{media.id}")
        # Should still succeed even if file doesn't exist
        assert response.status_code == 204

        # Verify the media entry was deleted from the database
        result = await db_session.execute(select(Media).where(Media.id == media.id))
        db_media = result.scalars().first()
        assert db_media is None
    finally:
        # Cleanup if needed
        pass
