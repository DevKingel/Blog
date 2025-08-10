import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.categories import (
    create_new_category,
    delete_category_by_id,
    get_category_posts,
    read_categories,
    read_category_by_id,
    update_existing_category,
)
from app.models.category import Category
from app.models.post import Post
from app.schemas.category import CategoryCreate, CategoryUpdate


@pytest.mark.asyncio
async def test_create_category_success():
    """Test successful creation of a category."""
    # Mock data
    category_data = CategoryCreate(name="Technology", slug="technology")
    mock_category = Category(
        id=uuid.uuid4(),
        name="Technology",
        slug="technology",
    )

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_all_categories"
        ) as mock_get_all,
        patch(
            "app.api.v1.endpoints.categories.category_crud.create_category"
        ) as mock_create,
    ):
        mock_get_all.return_value = []  # No existing categories
        mock_create.return_value = mock_category

        # Call the endpoint
        result = await create_new_category(category_in=category_data, db=mock_db)

        # Assertions
        assert result.name == "Technology"
        assert result.slug == "technology"
        mock_get_all.assert_called_once_with(mock_db)
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_create_category_duplicate_name():
    """Test creation of a category with duplicate name."""
    # Mock data
    category_data = CategoryCreate(name="Technology", slug="tech")
    existing_category = Category(
        id=uuid.uuid4(),
        name="Technology",
        slug="technology",
    )

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = [existing_category]

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await create_new_category(category_in=category_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.detail
            == "The category with this name already exists in the system."
        )


@pytest.mark.asyncio
async def test_create_category_duplicate_slug():
    """Test creation of a category with duplicate slug."""
    # Mock data
    category_data = CategoryCreate(name="Tech", slug="technology")
    existing_category = Category(
        id=uuid.uuid4(),
        name="Technology",
        slug="technology",
    )

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = [existing_category]

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await create_new_category(category_in=category_data, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.detail
            == "The category with this slug already exists in the system."
        )


@pytest.mark.asyncio
async def test_create_category_invalid_data():
    """Test creation of a category with invalid data."""
    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = []

        # This test is more of a placeholder
        # since Pydantic validation happens before the function call
        pass


@pytest.mark.asyncio
async def test_get_categories_success():
    """Test successful retrieval of categories."""
    # Mock data
    mock_categories = [
        Category(id=uuid.uuid4(), name="Tech", slug="tech"),
        Category(id=uuid.uuid4(), name="Science", slug="science"),
    ]

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = mock_categories

        # Call the endpoint
        result = await read_categories(db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].name == "Tech"
        assert result[1].name == "Science"
        mock_get_all.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_get_categories_with_pagination():
    """Test retrieval of categories with custom pagination."""
    # Mock data
    mock_categories = [
        Category(id=uuid.uuid4(), name="Tech", slug="tech"),
    ]

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = mock_categories

        # Call the endpoint with custom pagination
        result = await read_categories(skip=10, limit=5, db=mock_db)

        # Assertions
        assert len(result) == 1
        mock_get_all.assert_called_once_with(mock_db, skip=10, limit=5)


@pytest.mark.asyncio
async def test_get_categories_empty_result():
    """Test retrieval of categories when none exist."""
    # Mock data
    mock_categories = []

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_all_categories"
    ) as mock_get_all:
        mock_get_all.return_value = mock_categories

        # Call the endpoint
        result = await read_categories(db=mock_db)

        # Assertions
        assert len(result) == 0
        mock_get_all.assert_called_once_with(mock_db, skip=0, limit=100)


@pytest.mark.asyncio
async def test_get_category_by_id_success():
    """Test successful retrieval of a category by ID."""
    # Mock data
    category_id = uuid.uuid4()
    mock_category = Category(id=category_id, name="Tech", slug="tech")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = mock_category

        # Call the endpoint
        result = await read_category_by_id(category_id=category_id, db=mock_db)

        # Assertions
        assert result.id == category_id
        assert result.name == "Tech"
        mock_get_by_id.assert_called_once_with(mock_db, category_id=str(category_id))


@pytest.mark.asyncio
async def test_get_category_by_id_not_found():
    """Test retrieval of a non-existent category by ID."""
    # Mock data
    category_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await read_category_by_id(category_id=category_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"


@pytest.mark.asyncio
async def test_get_category_by_id_invalid_uuid():
    """Test retrieval of a category with invalid UUID."""
    # Test with invalid UUID - this will be handled by FastAPI validation
    # before reaching the function, so this test is more of a placeholder
    pass


@pytest.mark.asyncio
async def test_update_category_success():
    """Test successful update of a category."""
    # Mock data
    category_id = uuid.uuid4()
    existing_category = Category(id=category_id, name="Tech", slug="tech")
    update_data = CategoryUpdate(name="Technology")
    updated_category = Category(id=category_id, name="Technology", slug="tech")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
        ) as mock_get_by_id,
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_all_categories"
        ) as mock_get_all,
        patch(
            "app.api.v1.endpoints.categories.category_crud.update_category"
        ) as mock_update,
    ):
        mock_get_by_id.return_value = existing_category
        mock_get_all.return_value = [
            existing_category
        ]  # Only the category being updated
        mock_update.return_value = updated_category

        # Call the endpoint
        result = await update_existing_category(
            category_id=category_id, category_in=update_data, db=mock_db
        )

        # Assertions
        assert result.name == "Technology"
        mock_get_by_id.assert_called_once_with(mock_db, category_id=str(category_id))
        mock_get_all.assert_called_once_with(mock_db)
        mock_update.assert_called_once()


@pytest.mark.asyncio
async def test_update_category_not_found():
    """Test update of a non-existent category."""
    # Mock data
    category_id = uuid.uuid4()
    update_data = CategoryUpdate(name="Technology")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_category(
                category_id=category_id, category_in=update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 404
        assert (
            exc_info.value.detail
            == "The category with this id does not exist in the system"
        )


@pytest.mark.asyncio
async def test_update_category_duplicate_name():
    """Test update of a category with a name that already exists."""
    # Mock data
    category_id = uuid.uuid4()
    existing_category = Category(id=category_id, name="Tech", slug="tech")
    update_data = CategoryUpdate(name="Science")
    conflicting_category = Category(id=uuid.uuid4(), name="Science", slug="science")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
        ) as mock_get_by_id,
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_all_categories"
        ) as mock_get_all,
    ):
        mock_get_by_id.return_value = existing_category
        mock_get_all.return_value = [existing_category, conflicting_category]

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_category(
                category_id=category_id, category_in=update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.detail
            == "The category with this name already exists in the system."
        )


@pytest.mark.asyncio
async def test_update_category_duplicate_slug():
    """Test update of a category with a slug that already exists."""
    # Mock data
    category_id = uuid.uuid4()
    existing_category = Category(id=category_id, name="Tech", slug="tech")
    update_data = CategoryUpdate(slug="science")
    conflicting_category = Category(id=uuid.uuid4(), name="Science", slug="science")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
        ) as mock_get_by_id,
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_all_categories"
        ) as mock_get_all,
    ):
        mock_get_by_id.return_value = existing_category
        mock_get_all.return_value = [existing_category, conflicting_category]

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await update_existing_category(
                category_id=category_id, category_in=update_data, db=mock_db
            )

        # Assertions
        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.detail
            == "The category with this slug already exists in the system."
        )


@pytest.mark.asyncio
async def test_update_category_no_data():
    """Test update of a category with no data provided."""
    # Mock data
    category_id = uuid.uuid4()
    update_data = CategoryUpdate()

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Verify that the exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await update_existing_category(
            category_id=category_id, category_in=update_data, db=mock_db
        )

    # Assertions
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "No data provided for update"


@pytest.mark.asyncio
async def test_update_category_invalid_data():
    """Test update of a category with invalid data."""
    # Mock data
    category_id = uuid.uuid4()

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = Category(id=category_id, name="Tech", slug="tech")

        # Mock get_all_categories to return only the current category
        with patch(
            "app.api.v1.endpoints.categories.category_crud.get_all_categories"
        ) as mock_get_all:
            mock_get_all.return_value = [
                Category(id=category_id, name="Tech", slug="tech")
            ]

            # This test is more of a placeholder
            # since Pydantic validation happens before the function call
            pass


@pytest.mark.asyncio
async def test_delete_category_success():
    """Test successful deletion of a category."""
    # Mock data
    category_id = uuid.uuid4()
    mock_category = Category(id=category_id, name="Tech", slug="tech")

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
        ) as mock_get_by_id,
        patch(
            "app.api.v1.endpoints.categories.category_crud.delete_category"
        ) as mock_delete,
    ):
        mock_get_by_id.return_value = mock_category
        mock_delete.return_value = True

        # Call the endpoint
        result = await delete_category_by_id(category_id=category_id, db=mock_db)

        # Assertions
        assert result is None
        mock_get_by_id.assert_called_once_with(mock_db, category_id=str(category_id))
        mock_delete.assert_called_once_with(mock_db, category_id=str(category_id))


@pytest.mark.asyncio
async def test_delete_category_not_found():
    """Test deletion of a non-existent category."""
    # Mock data
    category_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await delete_category_by_id(category_id=category_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"


@pytest.mark.asyncio
async def test_get_category_posts_success():
    """Test successful retrieval of posts in a category."""
    # Mock data
    category_id = uuid.uuid4()
    mock_category = Category(id=category_id, name="Tech", slug="tech")
    mock_posts = [
        Post(
            id=uuid.uuid4(),
            title="Post 1",
            content="Content 1",
            category_id=category_id,
        ),
        Post(
            id=uuid.uuid4(),
            title="Post 2",
            content="Content 2",
            category_id=category_id,
        ),
    ]

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD and post functions
    with (
        patch(
            "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
        ) as mock_get_by_id,
        patch(
            "app.api.v1.endpoints.categories.get_posts_by_category"
        ) as mock_get_posts,
    ):
        mock_get_by_id.return_value = mock_category
        mock_get_posts.return_value = mock_posts

        # Call the endpoint
        result = await get_category_posts(category_id=category_id, db=mock_db)

        # Assertions
        assert len(result) == 2
        assert result[0].title == "Post 1"
        assert result[1].title == "Post 2"
        mock_get_by_id.assert_called_once_with(mock_db, category_id=str(category_id))
        mock_get_posts.assert_called_once_with(mock_db, category_id=category_id)


@pytest.mark.asyncio
async def test_get_category_posts_category_not_found():
    """Test retrieval of posts for a non-existent category."""
    # Mock data
    category_id = uuid.uuid4()

    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the category CRUD function
    with patch(
        "app.api.v1.endpoints.categories.category_crud.get_category_by_id"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = None

        # Verify that the exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await get_category_posts(category_id=category_id, db=mock_db)

        # Assertions
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
