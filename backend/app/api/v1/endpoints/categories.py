import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import category as category_crud
from app.crud.post import get_posts_by_category
from app.db.session import get_session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.post import PostRead

router = APIRouter()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_new_category(
    *,
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_session),
) -> Category:
    """
    Create new category.

    Args:
        category_in (CategoryCreate): The category data to create.
        db (AsyncSession): Database session.

    Returns:
        Category: The created category.
    """
    # Check if category with this name or slug already exists
    existing_category = await category_crud.get_all_categories(db)
    for cat in existing_category:
        if cat.name == category_in.name:
            raise HTTPException(
                status_code=400,
                detail="The category with this name already exists in the system.",
            )
        if cat.slug == category_in.slug:
            raise HTTPException(
                status_code=400,
                detail="The category with this slug already exists in the system.",
            )

    category_data = category_in.dict()
    category = await category_crud.create_category(db, category_data=category_data)
    return category


@router.get("/", response_model=list[CategoryRead])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
) -> list[Category]:
    """
    Retrieve categories.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (AsyncSession): Database session.

    Returns:
        list[Category]: List of categories.
    """
    categories = await category_crud.get_all_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def read_category_by_id(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Category:
    """
    Get a specific category by id.

    Args:
        category_id (uuid.UUID): The ID of the category to retrieve.
        db (AsyncSession): Database session.

    Returns:
        Category: The requested category.
    """
    category = await category_crud.get_category_by_id(db, category_id=str(category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_existing_category(
    *,
    category_id: uuid.UUID,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_session),
) -> Category:
    """
    Update a category.

    Args:
        category_id (uuid.UUID): The ID of the category to update.
        category_in (CategoryUpdate): The category data to update.
        db (AsyncSession): Database session.

    Returns:
        Category: The updated category.
    """
    category_data = category_in.dict(exclude_unset=True)
    if not category_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update",
        )

    # Check if category exists
    existing_category = await category_crud.get_category_by_id(db, category_id=str(category_id))
    if not existing_category:
        raise HTTPException(
            status_code=404,
            detail="The category with this id does not exist in the system",
        )

    # Check if updated name or slug conflicts with existing categories
    if category_data.get("name") or category_data.get("slug"):
        all_categories = await category_crud.get_all_categories(db)
        for cat in all_categories:
            # Skip the current category being updated
            if cat.id == category_id:
                continue
            if category_data.get("name") and cat.name == category_data["name"]:
                raise HTTPException(
                    status_code=400,
                    detail="The category with this name already exists in the system.",
                )
            if category_data.get("slug") and cat.slug == category_data["slug"]:
                raise HTTPException(
                    status_code=400,
                    detail="The category with this slug already exists in the system.",
                )

    category = await category_crud.update_category(
        db, category_id=str(category_id), category_data=category_data
    )
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The category with this id does not exist in the system",
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(
    *,
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Delete a category.

    Args:
        category_id (uuid.UUID): The ID of the category to delete.
        db (AsyncSession): Database session.

    Returns:
        None: Returns no content on successful deletion.
    """
    category = await category_crud.get_category_by_id(db, category_id=str(category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    success = await category_crud.delete_category(db, category_id=str(category_id))
    return None


@router.get("/{category_id}/posts", response_model=list[PostRead])
async def get_category_posts(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get all posts in a specific category.

    Args:
        category_id (uuid.UUID): The ID of the category.
        db (AsyncSession): Database session.

    Returns:
        list[PostRead]: List of posts in the category.
    """
    # Check if category exists
    category = await category_crud.get_category_by_id(db, category_id=str(category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    posts = await get_posts_by_category(db, category_id=category_id)
    return posts
