from backend.app.crud.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)
from backend.app.db.session import get_db
from backend.app.schemas.category import Category, CategoryCreate, CategoryUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=Category)
async def create_new_category(
    category_in: CategoryCreate, db: Session = Depends(get_db)
) -> Category:
    """
    Create a new category.
    """
    category = await create_category(db=db, category=category_in)
    return category


@router.get("/{category_id}", response_model=Category)
async def read_category(category_id: str, db: Session = Depends(get_db)) -> Category:
    """
    Get a category by its ID.
    """
    category = await get_category_by_id(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/", response_model=list[Category])
async def read_all_categories(db: Session = Depends(get_db)) -> list[Category]:
    """
    Get all categories.
    """
    categories = await get_all_categories(db=db)
    return categories


@router.put("/{category_id}", response_model=Category)
async def update_existing_category(
    category_id: str, category_in: CategoryUpdate, db: Session = Depends(get_db)
) -> Category:
    """
    Update a category.
    """
    category = await update_category(
        db=db, category_id=category_id, updated_category=category_in
    )
    return category


@router.delete("/{category_id}", response_model=None)
async def delete_existing_category(
    category_id: str, db: Session = Depends(get_db)
) -> None:
    """
    Delete a category.
    """
    await delete_category(db=db, category_id=category_id)
