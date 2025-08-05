from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_

from app.models.category import Category


async def create_category(db: AsyncSession, category_data: dict) -> Category:
    """
    Create a new category in the database.

    Args:
        db (Session): Database session.
        category_data (dict): Data for the new category.

    Returns:
        Category: The created category object.
    """
    category = Category(**category_data)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category_by_id(db: AsyncSession, category_id: str) -> Category | None:
    """
    Get a category by its ID from the database.
    """
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all_categories(
    db: AsyncSession, *, skip: int = 0, limit: int = 100
) -> list[Category]:
    """
    Get all categories with pagination.

    Args:
        db (AsyncSession): Database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[Category]: List of category objects.
    """
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


async def update_category(
    db: AsyncSession, category_id: str, category_data: dict
) -> Category | None:
    """
    Update a category in the database.

    Args:
        db (AsyncSession): Database session.
        category_id (str): ID of the category to update.
        category_data (dict): Data to update the category with.

    Returns:
        Optional[Category]: The updated category object if found, None otherwise.
    """
    category = await get_category_by_id(db, category_id)
    if not category:
        return None
    for key, value in category_data.items():
        if value:
            setattr(category, key, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: str) -> bool:
    """
    Delete a category from the database.
    """
    category = await get_category_by_id(db, category_id)
    if not category:
        return False
    await db.delete(category)
    await db.commit()
    return True


async def search_categories(
    db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
) -> tuple[list[Category], int]:
    """
    Search categories by query string (name).
    """
    # Create the search query
    search_query = select(Category).where(Category.name.ilike(f"%{query}%"))
    
    # Get total count
    count_query = select(func.count()).select_from(search_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination
    paginated_query = search_query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    categories = result.scalars().all()
    
    return categories, total
