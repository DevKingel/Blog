import uuid
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints.posts import (
    create_new_post,
    delete_post_by_id,
    publish_post,
    read_draft_posts,
    read_published_posts,
    unpublish_post,
    update_existing_post,
)
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


@pytest.mark.asyncio
async def test_create_new_post_success():
    """Test successful creation of a new post."""
    # Mock data
    post_data = PostCreate(
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Test Post",
        content="Test content",
        is_published=False,
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_created_post = Post(
        id=uuid.uuid4(),
        author_id=post_data.author_id,
        category_id=post_data.category_id,
        slug=post_data.slug,
        title=post_data.title,
        content=post_data.content,
        is_published=post_data.is_published,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.create_post") as mock_create_post:
        mock_create_post.return_value = mock_created_post

        # Call the endpoint
        result = await create_new_post(post_in=post_data, db=mock_db)

        # Assertions
        assert isinstance(result, Post)
        assert result.title == post_data.title
        assert result.content == post_data.content
        assert result.slug == post_data.slug
        mock_create_post.assert_called_once()


@pytest.mark.asyncio
async def test_create_new_post_db_error():
    """Test handling of database error during post creation."""
    # Mock data
    post_data = PostCreate(
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Test Post",
        content="Test content",
        is_published=False,
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise an exception
    with patch("app.api.v1.endpoints.posts.post_crud.create_post") as mock_create_post:
        mock_create_post.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await create_new_post(post_in=post_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while creating post"


@pytest.mark.asyncio
async def test_create_new_post_invalid_data():
    """Test creation of a new post with invalid data."""
    # Mock data with missing required fields
    post_data = PostCreate(
        # Missing author_id, category_id, slug, title, content
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Verify that the exception is raised due to validation error
    with pytest.raises(HTTPException) as exc_info:
        await create_new_post(post_in=post_data, db=mock_db)

    # Assertions
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error while creating post"


@pytest.mark.asyncio
async def test_update_existing_post_success():
    """Test successful update of an existing post."""
    # Mock data
    post_id = uuid.uuid4()
    update_data = PostUpdate(
        title="Updated Title",
        content="Updated content",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Original Title",
        content="Original content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_existing_post

        # Mock database session operations
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Call the endpoint
        result = await update_existing_post(
            post_id=post_id, post_in=update_data, db=mock_db
        )

        # Assertions
        assert isinstance(result, Post)
        assert result.title == update_data.title
        assert result.content == update_data.content
        assert result.id == post_id
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_existing_post_not_found():
    """Test update of a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()
    update_data = PostUpdate(
        title="Updated Title",
        content="Updated content",
    )

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The post with this id does not exist in the system",
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_post(post_id=post_id, post_in=update_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert (
            exc_info.value.detail
            == "The post with this id does not exist in the system"
        )


@pytest.mark.asyncio
async def test_update_existing_post_invalid_data():
    """Test update of an existing post with invalid data."""
    # Mock data
    post_id = uuid.uuid4()
    update_data = PostUpdate(
        # Invalid data - all fields are None by default
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Original Title",
        content="Original content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_existing_post

        # Mock database session operations
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Call the endpoint
        result = await update_existing_post(
            post_id=post_id, post_in=update_data, db=mock_db
        )

        # Assertions - post should remain unchanged since no update data was provided
        assert isinstance(result, Post)
        assert result.title == "Original Title"
        assert result.content == "Original content"
        mock_get_post.assert_called_once_with(mock_db, post_id)


@pytest.mark.asyncio
async def test_update_existing_post_db_error():
    """Test handling of database error during post update."""
    # Mock data
    post_id = uuid.uuid4()
    update_data = PostUpdate(
        title="Updated Title",
        content="Updated content",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Original Title",
        content="Original content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_existing_post

        # Mock database session operations to raise an exception
        mock_db.add = Mock()
        mock_db.commit = AsyncMock(side_effect=Exception("Database error"))
        mock_db.refresh = AsyncMock()

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_post(post_id=post_id, post_in=update_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while updating post"


@pytest.mark.asyncio
async def test_delete_post_by_id_success():
    """Test successful deletion of a post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Test Post",
        content="Test content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_post

        # Mock database session operations
        mock_db.delete = Mock()
        mock_db.commit = AsyncMock()

        # Call the endpoint
        result = await delete_post_by_id(post_id=post_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_db.delete.assert_called_once_with(mock_post)
        mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_post_by_id_not_found():
    """Test deletion of a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_post_by_id(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Post not found"


@pytest.mark.asyncio
async def test_delete_post_by_id_db_error():
    """Test handling of database error during post deletion."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="test-post",
        title="Test Post",
        content="Test content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_post

        # Mock database session operations to raise an exception
        mock_db.delete = Mock()
        mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_post_by_id(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while deleting post"


@pytest.mark.asyncio
async def test_read_draft_posts_success():
    """Test successful retrieval of draft posts."""
    # Mock data
    mock_draft_posts = [
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="draft-post-1",
            title="Draft Post 1",
            content="Content 1",
            is_published=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="draft-post-2",
            title="Draft Post 2",
            content="Content 2",
            is_published=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_draft_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await read_draft_posts(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(post, Post) for post in result)
    assert all(post.is_published is False for post in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_read_draft_posts_empty_result():
    """Test retrieval of draft posts when no draft posts exist."""
    # Mock data
    mock_draft_posts = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_draft_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await read_draft_posts(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_read_draft_posts_db_error():
    """Test handling of database error during draft posts retrieval."""
    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Database error")

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await read_draft_posts(db=mock_db)

    # Assertions
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error while fetching draft posts"


@pytest.mark.asyncio
async def test_read_published_posts_success():
    """Test successful retrieval of published posts."""
    # Mock data
    mock_published_posts = [
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="published-post-1",
            title="Published Post 1",
            content="Content 1",
            is_published=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            published_at=datetime.utcnow(),
        ),
        Post(
            id=uuid.uuid4(),
            author_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            slug="published-post-2",
            title="Published Post 2",
            content="Content 2",
            is_published=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            published_at=datetime.utcnow(),
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_published_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await read_published_posts(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(post, Post) for post in result)
    assert all(post.is_published is True for post in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_read_published_posts_empty_result():
    """Test retrieval of published posts when no published posts exist."""
    # Mock data
    mock_published_posts = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_published_posts
    mock_db.execute.return_value = mock_result

    # Call the endpoint
    result = await read_published_posts(db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_read_published_posts_db_error():
    """Test handling of database error during published posts retrieval."""
    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Database error")

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await read_published_posts(db=mock_db)

    # Assertions
    assert exc_info.value.status_code == 500
    assert (
        exc_info.value.detail == "Internal server error while fetching published posts"
    )


@pytest.mark.asyncio
async def test_publish_post_success():
    """Test successful publishing of a draft post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_draft_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="draft-post",
        title="Draft Post",
        content="Content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_draft_post

        # Mock database session operations
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Call the endpoint
        result = await publish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert isinstance(result, Post)
        assert result.is_published is True
        assert result.id == post_id
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_post_not_found():
    """Test publishing of a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The post with this id does not exist in the system",
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await publish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert (
            exc_info.value.detail
            == "The post with this id does not exist in the system"
        )


@pytest.mark.asyncio
async def test_publish_post_already_published():
    """Test publishing of an already published post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_published_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="published-post",
        title="Published Post",
        content="Content",
        is_published=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        published_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_published_post

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await publish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "The post is already published"


@pytest.mark.asyncio
async def test_publish_post_db_error():
    """Test handling of database error during post publishing."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_draft_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="draft-post",
        title="Draft Post",
        content="Content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_draft_post

        # Mock database session operations to raise an exception
        mock_db.add = Mock()
        mock_db.commit = AsyncMock(side_effect=Exception("Database error"))
        mock_db.refresh = AsyncMock()

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await publish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while publishing post"


@pytest.mark.asyncio
async def test_unpublish_post_success():
    """Test successful unpublishing of a published post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_published_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="published-post",
        title="Published Post",
        content="Content",
        is_published=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        published_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_published_post

        # Mock database session operations
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Call the endpoint
        result = await unpublish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert isinstance(result, Post)
        assert result.is_published is False
        assert result.id == post_id
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_unpublish_post_not_found():
    """Test unpublishing of a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The post with this id does not exist in the system",
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await unpublish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert (
            exc_info.value.detail
            == "The post with this id does not exist in the system"
        )


@pytest.mark.asyncio
async def test_unpublish_post_not_published():
    """Test unpublishing of a draft post."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_draft_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="draft-post",
        title="Draft Post",
        content="Content",
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_draft_post

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await unpublish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "The post is not published"


@pytest.mark.asyncio
async def test_unpublish_post_db_error():
    """Test handling of database error during post unpublishing."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_published_post = Post(
        id=post_id,
        author_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        slug="published-post",
        title="Published Post",
        content="Content",
        is_published=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        published_at=datetime.utcnow(),
    )

    # Mock the post CRUD function
    with patch("app.api.v1.endpoints.posts.post_crud.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = mock_published_post

        # Mock database session operations to raise an exception
        mock_db.add = Mock()
        mock_db.commit = AsyncMock(side_effect=Exception("Database error"))
        mock_db.refresh = AsyncMock()

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await unpublish_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while unpublishing post"
