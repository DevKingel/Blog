import uuid
from unittest.mock import AsyncMock, Mock

import pytest

from app.crud.comment import (
    create_comment,
    delete_comment,
    get_all_comments,
    get_comment_by_id,
    get_comments_by_post,
    get_comments_by_user,
    get_replies_by_comment,
    update_comment,
)
from app.models.comment import Comment


@pytest.mark.asyncio
async def test_create_comment_success():
    """Test successful creation of a new comment."""
    # Mock data
    comment_data = Comment(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await create_comment(comment_data, mock_db)

    # Assertions
    assert isinstance(result, Comment)
    assert result.id == comment_data.id
    assert result.user_id == comment_data.user_id
    assert result.post_id == comment_data.post_id
    assert result.content == comment_data.content
    mock_db.add.assert_called_once_with(comment_data)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(comment_data)


@pytest.mark.asyncio
async def test_create_comment_db_error():
    """Test handling of database error during comment creation."""
    # Mock data
    comment_data = Comment(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await create_comment(comment_data, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.add.assert_called_once_with(comment_data)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_comment_by_id_success():
    """Test successful retrieval of a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    mock_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_comment
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comment_by_id(comment_id, mock_db)

    # Assertions
    assert isinstance(result, Comment)
    assert result.id == comment_id
    assert result.content == "Test comment"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comment_by_id_not_found():
    """Test retrieval of a comment by ID when not found."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comment_by_id(comment_id, mock_db)

    # Assertions
    assert result is None
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_comments_success():
    """Test successful retrieval of all comments."""
    # Mock data
    mock_comments = [
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=uuid.uuid4(),
            content="First comment",
        ),
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=uuid.uuid4(),
            content="Second comment",
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_comments(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(comment, Comment) for comment in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_comments_empty_result():
    """Test retrieval of all comments when no comments exist."""
    # Mock data
    mock_comments = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_comments(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_by_post_success():
    """Test successful retrieval of comments by post ID."""
    # Mock data
    post_id = uuid.uuid4()
    mock_comments = [
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=post_id,
            content="First comment",
        ),
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=post_id,
            content="Second comment",
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comments_by_post(post_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(comment, Comment) for comment in result)
    assert all(comment.post_id == post_id for comment in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_by_post_empty_result():
    """Test retrieval of comments by post ID when no comments exist."""
    # Mock data
    post_id = uuid.uuid4()
    mock_comments = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comments_by_post(post_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_by_user_success():
    """Test successful retrieval of comments by user ID."""
    # Mock data
    user_id = uuid.uuid4()
    mock_comments = [
        Comment(
            id=uuid.uuid4(),
            user_id=user_id,
            post_id=uuid.uuid4(),
            content="First comment",
        ),
        Comment(
            id=uuid.uuid4(),
            user_id=user_id,
            post_id=uuid.uuid4(),
            content="Second comment",
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comments_by_user(user_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(comment, Comment) for comment in result)
    assert all(comment.user_id == user_id for comment in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_by_user_empty_result():
    """Test retrieval of comments by user ID when no comments exist."""
    # Mock data
    user_id = uuid.uuid4()
    mock_comments = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_comments
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_comments_by_user(user_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_replies_by_comment_success():
    """Test successful retrieval of replies to a comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    mock_replies = [
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=uuid.uuid4(),
            parent_comment_id=parent_comment_id,
            content="First reply",
        ),
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=uuid.uuid4(),
            parent_comment_id=parent_comment_id,
            content="Second reply",
        ),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_replies
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_replies_by_comment(parent_comment_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(comment, Comment) for comment in result)
    assert all(comment.parent_comment_id == parent_comment_id for comment in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_replies_by_comment_empty_result():
    """Test retrieval of replies to a comment when no replies exist."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    mock_replies = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_replies
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_replies_by_comment(parent_comment_id, mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_comment_success():
    """Test successful update of a comment."""
    # Mock data
    comment_id = uuid.uuid4()
    comment_data = {"content": "Updated comment"}
    existing_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Original comment",
    )
    updated_comment = Comment(
        id=comment_id,
        user_id=existing_comment.user_id,
        post_id=existing_comment.post_id,
        content="Updated comment",
    )

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.rowcount = 1
    mock_db.execute.return_value = mock_result

    # Mock get_comment_by_id to return the updated comment
    with pytest.MonkeyPatch().context() as m:
        m.setattr(
            "app.crud.comment.get_comment_by_id",
            AsyncMock(return_value=updated_comment),
        )

        # Call the function
        result = await update_comment(comment_id, comment_data, mock_db)

        # Assertions
        assert isinstance(result, Comment)
        assert result.content == "Updated comment"
        mock_db.execute.assert_called_once()
        mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_comment_not_found():
    """Test update of a non-existent comment."""
    # Mock data
    comment_id = uuid.uuid4()
    comment_data = {"content": "Updated comment"}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.rowcount = 0  # No rows affected
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await update_comment(comment_id, comment_data, mock_db)

    # Assertions
    assert result is None
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_update_comment_db_error():
    """Test handling of database error during comment update."""
    # Mock data
    comment_id = uuid.uuid4()
    comment_data = {"content": "Updated comment"}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Database error")

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await update_comment(comment_id, comment_data, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_comment_success():
    """Test successful deletion of a comment."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.rowcount = 1  # One row affected
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await delete_comment(comment_id, mock_db)

    # Assertions
    assert result is True
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_comment_not_found():
    """Test deletion of a non-existent comment."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.rowcount = 0  # No rows affected
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await delete_comment(comment_id, mock_db)

    # Assertions
    assert result is False
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_comment_db_error():
    """Test handling of database error during comment deletion."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Database error")

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await delete_comment(comment_id, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_not_called()
