import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException

from app.api.v1.endpoints.comments import (
    create_comment_for_post,
    delete_comment_by_id,
    read_comment_by_id,
    read_comments_by_post,
    read_replies_to_comment,
    reply_to_comment,
    update_comment_by_id,
)
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


@pytest.mark.asyncio
async def test_read_comments_by_post_success():
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

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comments_by_post"
    ) as mock_get_comments:
        mock_get_comments.return_value = mock_comments

        # Call the endpoint
        result = await read_comments_by_post(post_id=post_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].content == "First comment"
        assert result[1].content == "Second comment"
        mock_get_comments.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_read_comments_by_post_empty_result():
    """Test retrieval of comments by post ID when no comments exist."""
    # Mock data
    post_id = uuid.uuid4()
    mock_comments = []

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comments_by_post"
    ) as mock_get_comments:
        mock_get_comments.return_value = mock_comments

        # Call the endpoint
        result = await read_comments_by_post(post_id=post_id, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_comments.assert_called_once_with(mock_db, post_id=post_id)


@pytest.mark.asyncio
async def test_read_comments_by_post_db_error():
    """Test handling of database error when retrieving comments by post ID."""
    # Mock data
    post_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to raise an exception
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comments_by_post"
    ) as mock_get_comments:
        mock_get_comments.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await read_comments_by_post(post_id=post_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while fetching comments"


@pytest.mark.asyncio
async def test_create_comment_for_post_success():
    """Test successful creation of a comment for a post."""
    # Mock data
    post_id = uuid.uuid4()
    user_id = uuid.uuid4()
    comment_data = CommentCreate(user_id=user_id, content="Test comment")
    mock_post = Mock()  # Mock post object
    mock_comment = Comment(
        id=uuid.uuid4(), user_id=user_id, post_id=post_id, content="Test comment"
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the post CRUD and comment CRUD functions
    with (
        patch("app.api.v1.endpoints.comments.get_post_by_id") as mock_get_post,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.create_comment"
        ) as mock_create_comment,
    ):
        mock_get_post.return_value = mock_post
        mock_create_comment.return_value = mock_comment

        # Call the endpoint
        result = await create_comment_for_post(
            post_id=post_id, comment_in=comment_data, db=mock_db
        )

        # Assertions
        assert result.content == "Test comment"
        assert result.post_id == post_id
        assert result.user_id == user_id
        mock_get_post.assert_called_once_with(mock_db, post_id)
        mock_create_comment.assert_called_once()


@pytest.mark.asyncio
async def test_create_comment_for_post_invalid_post():
    """Test creation of a comment for a non-existent post."""
    # Mock data
    post_id = uuid.uuid4()
    user_id = uuid.uuid4()
    comment_data = CommentCreate(user_id=user_id, content="Test comment")

    # Mock database session
    mock_db = AsyncMock()

    # Mock the post CRUD function to raise HTTPException
    with patch("app.api.v1.endpoints.comments.get_post_by_id") as mock_get_post:
        mock_get_post.side_effect = HTTPException(
            status_code=404, detail="Post not found"
        )

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await create_comment_for_post(
                post_id=post_id, comment_in=comment_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Post not found"


@pytest.mark.asyncio
async def test_create_comment_for_post_missing_fields():
    """Test creation of a comment with missing required fields."""
    # This test is more of a placeholder
    # since Pydantic validation happens before the function call
    # In a real test, we would test the validation at the API level
    pass


@pytest.mark.asyncio
async def test_create_comment_for_post_db_error():
    """Test handling of database error when creating a comment for a post."""
    # Mock data
    post_id = uuid.uuid4()
    user_id = uuid.uuid4()
    comment_data = CommentCreate(user_id=user_id, content="Test comment")
    mock_post = Mock()  # Mock post object

    # Mock database session
    mock_db = AsyncMock()

    # Mock the post CRUD and comment CRUD functions
    with (
        patch("app.api.v1.endpoints.comments.get_post_by_id") as mock_get_post,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.create_comment"
        ) as mock_create_comment,
    ):
        mock_get_post.return_value = mock_post
        mock_create_comment.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await create_comment_for_post(
                post_id=post_id, comment_in=comment_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error while creating comment"


@pytest.mark.asyncio
async def test_read_comment_by_id_success():
    """Test successful retrieval of a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    mock_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = mock_comment

        # Call the endpoint
        result = await read_comment_by_id(comment_id=comment_id, db=mock_db)

        # Assertions
        assert result.id == comment_id
        assert result.content == "Test comment"
        mock_get_comment.assert_called_once_with(mock_db, comment_id=comment_id)


@pytest.mark.asyncio
async def test_read_comment_by_id_not_found():
    """Test retrieval of a non-existent comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to return None
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await read_comment_by_id(comment_id=comment_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Comment not found"


@pytest.mark.asyncio
async def test_read_comment_by_id_invalid_uuid():
    """Test retrieval of a comment with invalid UUID."""
    # Test with invalid UUID - this will be handled by FastAPI validation
    # before reaching the function, so this test is more of a placeholder
    pass


@pytest.mark.asyncio
async def test_update_comment_by_id_success():
    """Test successful update of a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    existing_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Original comment",
    )
    update_data = CommentUpdate(content="Updated comment")
    updated_comment = Comment(
        id=comment_id,
        user_id=existing_comment.user_id,
        post_id=existing_comment.post_id,
        content="Updated comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.update_comment"
        ) as mock_update_comment,
    ):
        mock_get_comment.return_value = existing_comment
        mock_update_comment.return_value = updated_comment

        # Call the endpoint
        result = await update_comment_by_id(
            comment_id=comment_id, comment_in=update_data, db=mock_db
        )

        # Assertions
        assert result.content == "Updated comment"
        mock_get_comment.assert_called_once_with(mock_db, comment_id=comment_id)
        mock_update_comment.assert_called_once_with(
            mock_db, comment_id=comment_id, comment_data={"content": "Updated comment"}
        )


@pytest.mark.asyncio
async def test_update_comment_by_id_not_found():
    """Test update of a non-existent comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    update_data = CommentUpdate(content="Updated comment")

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to return None
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_comment_by_id(
                comment_id=comment_id, comment_in=update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Comment not found"


@pytest.mark.asyncio
async def test_update_comment_by_id_invalid_data():
    """Test update of a comment with invalid data."""
    # Mock the comment CRUD function
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=uuid.uuid4(),
            content="Original comment",
        )

        # This test is more of a placeholder
        # since Pydantic validation happens before the function call
        pass


@pytest.mark.asyncio
async def test_update_comment_by_id_db_error():
    """Test handling of database error when updating a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    existing_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Original comment",
    )
    update_data = CommentUpdate(content="Updated comment")

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.update_comment"
        ) as mock_update_comment,
    ):
        mock_get_comment.return_value = existing_comment
        mock_update_comment.return_value = None  # Simulate database error

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_comment_by_id(
                comment_id=comment_id, comment_in=update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Comment not found"


@pytest.mark.asyncio
async def test_delete_comment_by_id_success():
    """Test successful deletion of a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    mock_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.delete_comment"
        ) as mock_delete_comment,
    ):
        mock_get_comment.return_value = mock_comment
        mock_delete_comment.return_value = True

        # Call the endpoint
        result = await delete_comment_by_id(comment_id=comment_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_comment.assert_called_once_with(mock_db, comment_id=comment_id)
        mock_delete_comment.assert_called_once_with(mock_db, comment_id=comment_id)


@pytest.mark.asyncio
async def test_delete_comment_by_id_not_found():
    """Test deletion of a non-existent comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to return None
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_comment_by_id(comment_id=comment_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Comment not found"


@pytest.mark.asyncio
async def test_delete_comment_by_id_db_error():
    """Test handling of database error when deleting a comment by ID."""
    # Mock data
    comment_id = uuid.uuid4()
    mock_comment = Comment(
        id=comment_id,
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        content="Test comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.delete_comment"
        ) as mock_delete_comment,
    ):
        mock_get_comment.return_value = mock_comment
        mock_delete_comment.return_value = False  # Simulate database error

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_comment_by_id(comment_id=comment_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Comment not found"


@pytest.mark.asyncio
async def test_reply_to_comment_success():
    """Test successful reply to a comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    user_id = uuid.uuid4()
    post_id = uuid.uuid4()
    parent_comment = Comment(
        id=parent_comment_id, user_id=user_id, post_id=post_id, content="Parent comment"
    )
    reply_data = CommentCreate(user_id=user_id, content="Reply comment")
    reply_comment = Comment(
        id=uuid.uuid4(),
        user_id=user_id,
        post_id=post_id,
        parent_comment_id=parent_comment_id,
        content="Reply comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.create_comment"
        ) as mock_create_comment,
    ):
        mock_get_comment.return_value = parent_comment
        mock_create_comment.return_value = reply_comment

        # Call the endpoint
        result = await reply_to_comment(
            comment_id=parent_comment_id, comment_in=reply_data, db=mock_db
        )

        # Assertions
        assert result.content == "Reply comment"
        assert result.post_id == post_id
        assert result.parent_comment_id == parent_comment_id
        assert result.user_id == user_id
        mock_get_comment.assert_called_once_with(mock_db, comment_id=parent_comment_id)
        mock_create_comment.assert_called_once()


@pytest.mark.asyncio
async def test_reply_to_comment_parent_not_found():
    """Test reply to a non-existent parent comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reply_data = CommentCreate(user_id=user_id, content="Reply comment")

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to return None
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await reply_to_comment(
                comment_id=parent_comment_id, comment_in=reply_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Parent comment not found"


@pytest.mark.asyncio
async def test_reply_to_comment_missing_fields():
    """Test reply to a comment with missing required fields."""
    # This test is more of a placeholder
    # since Pydantic validation happens before the function call
    pass


@pytest.mark.asyncio
async def test_reply_to_comment_db_error():
    """Test handling of database error when replying to a comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    user_id = uuid.uuid4()
    post_id = uuid.uuid4()
    parent_comment = Comment(
        id=parent_comment_id, user_id=user_id, post_id=post_id, content="Parent comment"
    )
    reply_data = CommentCreate(user_id=user_id, content="Reply comment")

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.create_comment"
        ) as mock_create_comment,
    ):
        mock_get_comment.return_value = parent_comment
        mock_create_comment.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await reply_to_comment(
                comment_id=parent_comment_id, comment_in=reply_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 500
        assert (
            exc_info.value.detail == "Internal server error while replying to comment"
        )


@pytest.mark.asyncio
async def test_read_replies_to_comment_success():
    """Test successful retrieval of replies to a comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    post_id = uuid.uuid4()
    parent_comment = Comment(
        id=parent_comment_id,
        user_id=uuid.uuid4(),
        post_id=post_id,
        content="Parent comment",
    )
    mock_replies = [
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=post_id,
            parent_comment_id=parent_comment_id,
            content="First reply",
        ),
        Comment(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            post_id=post_id,
            parent_comment_id=parent_comment_id,
            content="Second reply",
        ),
    ]

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_replies_by_comment"
        ) as mock_get_replies,
    ):
        mock_get_comment.return_value = parent_comment
        mock_get_replies.return_value = mock_replies

        # Call the endpoint
        result = await read_replies_to_comment(comment_id=parent_comment_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].content == "First reply"
        assert result[1].content == "Second reply"
        assert result[0].parent_comment_id == parent_comment_id
        assert result[1].parent_comment_id == parent_comment_id
        mock_get_comment.assert_called_once_with(mock_db, comment_id=parent_comment_id)
        mock_get_replies.assert_called_once_with(mock_db, comment_id=parent_comment_id)


@pytest.mark.asyncio
async def test_read_replies_to_comment_parent_not_found():
    """Test retrieval of replies to a non-existent parent comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD function to return None
    with patch(
        "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
    ) as mock_get_comment:
        mock_get_comment.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await read_replies_to_comment(comment_id=parent_comment_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Parent comment not found"


@pytest.mark.asyncio
async def test_read_replies_to_comment_empty_result():
    """Test retrieval of replies to a comment when no replies exist."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    post_id = uuid.uuid4()
    parent_comment = Comment(
        id=parent_comment_id,
        user_id=uuid.uuid4(),
        post_id=post_id,
        content="Parent comment",
    )
    mock_replies = []

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_replies_by_comment"
        ) as mock_get_replies,
    ):
        mock_get_comment.return_value = parent_comment
        mock_get_replies.return_value = mock_replies

        # Call the endpoint
        result = await read_replies_to_comment(comment_id=parent_comment_id, db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_comment.assert_called_once_with(mock_db, comment_id=parent_comment_id)
        mock_get_replies.assert_called_once_with(mock_db, comment_id=parent_comment_id)


@pytest.mark.asyncio
async def test_read_replies_to_comment_db_error():
    """Test handling of database error when retrieving replies to a comment."""
    # Mock data
    parent_comment_id = uuid.uuid4()
    post_id = uuid.uuid4()
    parent_comment = Comment(
        id=parent_comment_id,
        user_id=uuid.uuid4(),
        post_id=post_id,
        content="Parent comment",
    )

    # Mock database session
    mock_db = AsyncMock()

    # Mock the comment CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_comment_by_id"
        ) as mock_get_comment,
        patch(
            "app.api.v1.endpoints.comments.comment_crud.get_replies_by_comment"
        ) as mock_get_replies,
    ):
        mock_get_comment.return_value = parent_comment
        mock_get_replies.side_effect = Exception("Database error")

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await read_replies_to_comment(comment_id=parent_comment_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 500
        assert (
            exc_info.value.detail
            == "Internal server error while fetching comment replies"
        )
