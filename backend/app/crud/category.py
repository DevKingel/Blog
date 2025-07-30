from backend.app.models.category import Category
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session


async def create_category(db: Session, category: Category) -> Category:
    """
    Create a new category in the database.
    """
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category_by_id(db: Session, category_id: str) -> Category | None:
    """
    Get a category by its ID from the database.
    """
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all_categories(db: Session) -> list[Category]:
    """
    Get all categories from the database.
    """
    query = select(Category)
    result = await db.execute(query)
    return result.scalars().all()


async def update_category(
    db: Session, category_id: str, updated_category: Category
) -> Category | None:
    """
    Update a category in the database.
    """
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for var, value in vars(updated_category).items():
        setattr(category, var, value) if value else None
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: Session, category_id: str) -> bool:
    """
    Delete a category from the database.
    """
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
    return True
