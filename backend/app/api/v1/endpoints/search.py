from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import category as category_crud
from app.crud import post as post_crud
from app.crud import tag as tag_crud
from app.crud import user as user_crud
from app.db.session import get_session
from app.schemas.search import (
    CategorySearchResult,
    PostSearchResult,
    TagSearchResult,
    UserSearchResult,
)

router = APIRouter()


@router.get("/posts", response_model=PostSearchResult)
async def search_posts(
    query: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
):
    """
    Search posts by query string in title or content.
    
    Args:
        query: Search query string
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        
    Returns:
        PostSearchResult: Search results with posts and total count
    """
    posts, total = await post_crud.search_posts(db, query=query, skip=skip, limit=limit)
    return PostSearchResult(posts=posts, total=total)


@router.get("/users", response_model=UserSearchResult)
async def search_users(
    query: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
):
    """
    Search users by query string in username or email.
    
    Args:
        query: Search query string
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        
    Returns:
        UserSearchResult: Search results with users and total count
    """
    users, total = await user_crud.search_users(db, query=query, skip=skip, limit=limit)
    return UserSearchResult(users=users, total=total)


@router.get("/categories", response_model=CategorySearchResult)
async def search_categories(
    query: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
):
    """
    Search categories by query string in name.
    
    Args:
        query: Search query string
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        
    Returns:
        CategorySearchResult: Search results with categories and total count
    """
    categories, total = await category_crud.search_categories(db, query=query, skip=skip, limit=limit)
    return CategorySearchResult(categories=categories, total=total)


@router.get("/tags", response_model=TagSearchResult)
async def search_tags(
    query: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
):
    """
    Search tags by query string in name.
    
    Args:
        query: Search query string
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        
    Returns:
        TagSearchResult: Search results with tags and total count
    """
    tags, total = await tag_crud.search_tags(db, query=query, skip=skip, limit=limit)
    return TagSearchResult(tags=tags, total=total)
