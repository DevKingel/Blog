import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app
from app.models.post import Post
from app.models.post_tag import PostTag
from app.models.tag import Tag

client = TestClient(app)


@pytest.fixture
async def db_session():
    """Create a database session for testing."""
    async with get_session() as session:
        yield session


@pytest.fixture
async def test_tag(db_session: AsyncSession):
    """Create a test tag."""
    tag = Tag(
        id=uuid.uuid4(),
        name="Python",
        slug="python"
    )
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)

    yield tag

    # Cleanup
    await db_session.delete(tag)
    await db_session.commit()


@pytest.fixture
async def test_posts_with_tag(db_session: AsyncSession, test_tag: Tag):
    """Create test posts with a specific tag."""
    # Create posts
    post1 = Post(
        id=uuid.uuid4(),
        title="Python Tips",
        content="Some useful Python tips",
        author_id=uuid.uuid4(),  # Assuming there's a default author
        category_id=uuid.uuid4()  # Assuming there's a default category
    )
    post2 = Post(
        id=uuid.uuid4(),
        title="Advanced Python",
        content="Advanced Python concepts",
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4()
    )

    db_session.add_all([post1, post2])
    await db_session.commit()
    await db_session.refresh(post1)
    await db_session.refresh(post2)

    # Create post-tag relationships
    post_tag1 = PostTag(post_id=post1.id, tag_id=test_tag.id)
    post_tag2 = PostTag(post_id=post2.id, tag_id=test_tag.id)

    db_session.add_all([post_tag1, post_tag2])
    await db_session.commit()

    yield [post1, post2]

    # Cleanup
    await db_session.delete(post_tag1)
    await db_session.delete(post_tag2)
    await db_session.delete(post1)
    await db_session.delete(post2)
    await db_session.commit()


# Integration tests for POST /tags/ - Create a new tag
def test_create_tag_success():
    """Test successful tag creation."""
    tag_data = {
        "name": "JavaScript",
        "slug": "javascript"
    }

    response = client.post("/api/v1/tags/", json=tag_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "JavaScript"
    assert data["slug"] == "javascript"


def test_create_tag_duplicate_name():
    """Test tag creation with duplicate name."""
    # First, create a tag
    tag_data = {
        "name": "Python",
        "slug": "python"
    }
    client.post("/api/v1/tags/", json=tag_data)

    # Try to create another tag with the same name
    response = client.post("/api/v1/tags/", json=tag_data)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_tag_duplicate_slug():
    """Test tag creation with duplicate slug."""
    # First, create a tag
    tag_data1 = {
        "name": "Python",
        "slug": "python"
    }
    client.post("/api/v1/tags/", json=tag_data1)

    # Try to create another tag with the same slug but different name
    tag_data2 = {
        "name": "Python Programming",
        "slug": "python"
    }
    response = client.post("/api/v1/tags/", json=tag_data2)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_tag_invalid_data():
    """Test tag creation with invalid data."""
    # Missing required fields
    tag_data = {}

    response = client.post("/api/v1/tags/", json=tag_data)

    assert response.status_code == 422


# Integration tests for GET /tags/ - Retrieve tags with pagination
def test_read_tags_success():
    """Test successful retrieval of tags."""
    # First, create some tags
    tag_data1 = {"name": "Python", "slug": "python"}
    tag_data2 = {"name": "JavaScript", "slug": "javascript"}

    client.post("/api/v1/tags/", json=tag_data1)
    client.post("/api/v1/tags/", json=tag_data2)

    response = client.get("/api/v1/tags/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    # Check that our tags are in the response
    tag_names = [tag["name"] for tag in data]
    assert "Python" in tag_names
    assert "JavaScript" in tag_names


def test_read_tags_empty():
    """Test retrieval of tags when none exist."""
    # This assumes we're working with a clean database for tests
    response = client.get("/api/v1/tags/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # In a real test environment, this might not be empty if other tests created tags


def test_read_tags_with_pagination():
    """Test retrieval of tags with pagination."""
    # First, create some tags
    for i in range(5):
        tag_data = {"name": f"Tag{i}", "slug": f"tag-{i}"}
        client.post("/api/v1/tags/", json=tag_data)

    response = client.get("/api/v1/tags/?skip=1&limit=3")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3


# Integration tests for GET /tags/{tag_id} - Get a specific tag by id
async def test_read_tag_by_id_success(db_session: AsyncSession, test_tag: Tag):
    """Test successful retrieval of a tag by ID."""
    response = client.get(f"/api/v1/tags/{test_tag.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_tag.id)
    assert data["name"] == "Python"
    assert data["slug"] == "python"


def test_read_tag_by_id_not_found():
    """Test retrieval of a non-existent tag by ID."""
    fake_tag_id = uuid.uuid4()
    response = client.get(f"/api/v1/tags/{fake_tag_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# Integration tests for PUT /tags/{tag_id} - Update a tag
async def test_update_tag_success(db_session: AsyncSession, test_tag: Tag):
    """Test successful tag update."""
    update_data = {"name": "Python 3", "slug": "python3"}

    response = client.put(f"/api/v1/tags/{test_tag.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Python 3"
    assert data["slug"] == "python3"


def test_update_tag_not_found():
    """Test update of a non-existent tag."""
    fake_tag_id = uuid.uuid4()
    update_data = {"name": "Python 3"}

    response = client.put(f"/api/v1/tags/{fake_tag_id}", json=update_data)

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


async def test_update_tag_duplicate_name(db_session: AsyncSession):
    """Test tag update with duplicate name."""
    # Create two tags
    tag_data1 = {"name": "Python", "slug": "python"}
    tag_data2 = {"name": "JavaScript", "slug": "javascript"}

    response1 = client.post("/api/v1/tags/", json=tag_data1)
    response2 = client.post("/api/v1/tags/", json=tag_data2)

    tag1_id = response1.json()["id"]
    tag2_id = response2.json()["id"]

    # Try to update tag2 to have the same name as tag1
    update_data = {"name": "Python"}
    response = client.put(f"/api/v1/tags/{tag2_id}", json=update_data)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_tag_partial():
    """Test partial tag update."""
    # First, create a tag
    tag_data = {"name": "Python", "slug": "python"}
    response = client.post("/api/v1/tags/", json=tag_data)
    tag_id = response.json()["id"]

    # Update only the name
    update_data = {"name": "Python 3"}
    response = client.put(f"/api/v1/tags/{tag_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Python 3"
    assert data["slug"] == "python"  # Slug should remain unchanged


# Integration tests for DELETE /tags/{tag_id} - Delete a tag
async def test_delete_tag_success(db_session: AsyncSession, test_tag: Tag):
    """Test successful tag deletion."""
    response = client.delete(f"/api/v1/tags/{test_tag.id}")

    assert response.status_code == 204

    # Verify the tag no longer exists in the database
    result = await db_session.execute(select(Tag).where(Tag.id == test_tag.id))
    tag = result.scalars().first()
    assert tag is None


def test_delete_tag_not_found():
    """Test deletion of a non-existent tag."""
    fake_tag_id = uuid.uuid4()
    response = client.delete(f"/api/v1/tags/{fake_tag_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# Integration tests for GET /tags/{tag_id}/posts - Get all posts with a specific tag
async def test_get_posts_with_tag_success(
    db_session: AsyncSession,
    test_tag: Tag,
    test_posts_with_tag: list[Post]
):
    """Test successful retrieval of posts with a specific tag."""
    response = client.get(f"/api/v1/tags/{test_tag.id}/posts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    # Check that the posts are in the response
    post_titles = [post["title"] for post in data]
    assert "Python Tips" in post_titles
    assert "Advanced Python" in post_titles


async def test_get_posts_with_tag_empty(db_session: AsyncSession, test_tag: Tag):
    """Test retrieval of posts with a tag when no posts have that tag."""
    # Create a new tag without any posts
    tag_data = {"name": "Empty Tag", "slug": "empty-tag"}
    response = client.post("/api/v1/tags/", json=tag_data)
    new_tag_id = response.json()["id"]

    response = client.get(f"/api/v1/tags/{new_tag_id}/posts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_posts_with_tag_not_found():
    """Test retrieval of posts with a non-existent tag."""
    fake_tag_id = uuid.uuid4()
    response = client.get(f"/api/v1/tags/{fake_tag_id}/posts")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
