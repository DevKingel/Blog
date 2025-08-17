import uuid
from unittest.mock import AsyncMock, Mock

import pytest

from app.crud.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    search_categories,
    update_category,
)
from app.models.category import Category


@pytest.mark.asyncio
async def test_create_category_success():
    """Test successful creation of a new category."""
    # Mock data
    category_data = {"name": "Technology", "slug": "technology"}

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock database session operations
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await create_category(category_data, mock_db)

    # Assertions
    assert isinstance(result, Category)
    assert result.name == category_data["name"]
    assert result.slug == category_data["slug"]
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_category_db_error():
    """Test handling of database error during category creation."""
    # Mock data
    category_data = {"name": "Technology", "slug": "technology"}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock(side_effect=Exception("Database error"))

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        await create_category(category_data, mock_db)

    # Assertions
    assert str(exc_info.value) == "Database error"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_category_by_id_success():
    """Test successful retrieval of a category by ID."""
    # Mock data
    category_id = str(uuid.uuid4())
    mock_category = Category(id=uuid.UUID(category_id), name="Tech", slug="tech")

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_category
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_category_by_id(category_id, mock_db)

    # Assertions
    assert isinstance(result, Category)
    assert str(result.id) == category_id
    assert result.name == "Tech"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_category_by_id_not_found():
    """Test retrieval of a category by ID when not found."""
    # Mock data
    category_id = str(uuid.uuid4())

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_category_by_id(category_id, mock_db)

    # Assertions
    assert result is None
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_categories_success():
    """Test successful retrieval of all categories."""
    # Mock data
    mock_categories = [
        Category(id=uuid.uuid4(), name="Tech", slug="tech"),
        Category(id=uuid.uuid4(), name="Science", slug="science"),
    ]

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_categories
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_categories(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(category, Category) for category in result)
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_categories_empty_result():
    """Test retrieval of all categories when no categories exist."""
    # Mock data
    mock_categories = []

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_categories
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_categories(mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_categories_with_pagination():
    """Test retrieval of categories with pagination."""
    # Mock data
    mock_categories = [
        Category(id=uuid.uuid4(), name="Tech", slug="tech"),
    ]
    skip = 10
    limit = 5

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalars().all.return_value = mock_categories
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await get_all_categories(mock_db, skip=skip, limit=limit)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_category_success():
    """Test successful update of a category."""
    # Mock data
    category_id = str(uuid.uuid4())
    category_data = {"name": "Technology", "slug": "technology"}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_category = Category(
        id=uuid.UUID(category_id), name="Tech", slug="tech"
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_existing_category
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_category(category_id, category_data, mock_db)

    # Assertions
    assert isinstance(result, Category)
    assert result.name == "Technology"
    assert result.slug == "technology"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_category_not_found():
    """Test update of a non-existent category."""
    # Mock data
    category_id = str(uuid.uuid4())
    category_data = {"name": "Technology"}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await update_category(category_id, category_data, mock_db)

    # Assertions
    assert result is None
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_category_partial_data():
    """Test update of a category with partial data."""
    # Mock data
    category_id = str(uuid.uuid4())
    category_data = {
        "name": "Technology"
        # slug not provided, should remain unchanged
    }

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_category = Category(
        id=uuid.UUID(category_id), name="Tech", slug="tech"
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_existing_category
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_category(category_id, category_data, mock_db)

    # Assertions
    assert isinstance(result, Category)
    assert result.name == "Technology"
    assert result.slug == "tech"  # Should remain unchanged
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_category_empty_data():
    """Test update of a category with empty data."""
    # Mock data
    category_id = str(uuid.uuid4())
    category_data = {}

    # Mock dependencies
    mock_db = AsyncMock()
    mock_existing_category = Category(
        id=uuid.UUID(category_id), name="Tech", slug="tech"
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_existing_category
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Call the function
    result = await update_category(category_id, category_data, mock_db)

    # Assertions
    assert isinstance(result, Category)
    assert result.name == "Tech"  # Should remain unchanged
    assert result.slug == "tech"  # Should remain unchanged
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_category_success():
    """Test successful deletion of a category."""
    # Mock data
    category_id = str(uuid.uuid4())

    # Mock dependencies
    mock_db = AsyncMock()
    mock_category = Category(id=uuid.UUID(category_id), name="Tech", slug="tech")
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_category
    mock_db.execute.return_value = mock_result
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()

    # Call the function
    result = await delete_category(category_id, mock_db)

    # Assertions
    assert result is True
    mock_db.execute.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_category)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_category_not_found():
    """Test deletion of a non-existent category."""
    # Mock data
    category_id = str(uuid.uuid4())

    # Mock dependencies
    mock_db = AsyncMock()
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Call the function
    result = await delete_category(category_id, mock_db)

    # Assertions
    assert result is False
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_search_categories_success():
    """Test successful search of categories."""
    # Mock data
    query = "tech"
    mock_categories = [
        Category(id=uuid.uuid4(), name="Technology", slug="technology"),
        Category(id=uuid.uuid4(), name="Tech News", slug="tech-news"),
    ]
    total_count = 2

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock results for search query
    mock_search_result = Mock()
    mock_search_result.scalars().all.return_value = mock_categories

    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one.return_value = total_count

    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_search_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await search_categories(query=query, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2
    assert total == 2
    assert all(isinstance(category, Category) for category in result)
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_search_categories_empty_result():
    """Test search of categories with no matches."""
    # Mock data
    query = "nonexistent"

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock results for search query
    mock_search_result = Mock()
    mock_search_result.scalars().all.return_value = []

    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one = Mock(return_value=0)

    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_search_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await search_categories(query=query, db=mock_db)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 0
    assert total == 0
    assert mock_db.execute.call_count == 2


@pytest.mark.asyncio
async def test_search_categories_with_pagination():
    """Test search of categories with pagination."""
    # Mock data
    query = "tech"
    skip = 5
    limit = 10
    mock_categories = [
        Category(id=uuid.uuid4(), name="Technology", slug="technology"),
    ]
    total_count = 15

    # Mock dependencies
    mock_db = AsyncMock()

    # Mock results for search query
    mock_search_result = Mock()
    mock_search_result.scalars().all.return_value = mock_categories

    # Mock results for count query
    mock_count_result = Mock()
    mock_count_result.scalar_one = Mock(return_value=total_count)

    # Configure mock_db.execute to return different results based on the query
    async def execute_side_effect(query_obj):
        query_str = str(query_obj)
        if "COUNT" in query_str:
            return mock_count_result
        else:
            return mock_search_result

    mock_db.execute.side_effect = execute_side_effect

    # Call the function
    result, total = await search_categories(
        query=query, skip=skip, limit=limit, db=mock_db
    )

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert total == 15
    assert mock_db.execute.call_count == 2
