import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import tag as tag_crud
from app.crud.post import get_posts_by_tag
from app.db.session import get_session
from app.models.tag import Tag
from app.schemas.post import PostRead
from app.schemas.tag import TagCreate, TagRead, TagUpdate

router = APIRouter()


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_new_tag(
    *,
    tag_in: TagCreate,
    db: AsyncSession = Depends(get_session),
) -> Tag:
    """
    Create a new tag.
    """
    # Check if tag with this name or slug already exists
    existing_tag = await tag_crud.get_tag_by_name_or_slug(
        db, name=tag_in.name, slug=tag_in.slug
    )
    if existing_tag:
        raise HTTPException(
            status_code=400,
            detail="A tag with this name or slug already exists.",
        )

    # Create the tag
    tag = Tag(**tag_in.model_dump())
    tag = await tag_crud.create_tag(db, tag=tag)
    return tag


@router.get("/", response_model=list[TagRead])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
) -> list[Tag]:
    """
    Retrieve tags.
    """
    tags = await tag_crud.get_all_tags(db)
    return tags[skip : skip + limit]


@router.get("/{tag_id}", response_model=TagRead)
async def read_tag_by_id(
    tag_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Tag:
    """
    Get a specific tag by id.
    """
    tag = await tag_crud.get_tag_by_id(db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagRead)
async def update_existing_tag(
    *,
    tag_id: uuid.UUID,
    tag_in: TagUpdate,
    db: AsyncSession = Depends(get_session),
) -> Tag:
    """
    Update a tag.
    """
    # Check if tag exists
    db_tag = await tag_crud.get_tag_by_id(db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(
            status_code=404,
            detail="The tag with this id does not exist in the system",
        )

    # Check if another tag with the same name or slug already exists
    if tag_in.name or tag_in.slug:
        existing_tag = await tag_crud.get_tag_by_name_or_slug(
            db, name=tag_in.name or db_tag.name, slug=tag_in.slug or db_tag.slug
        )
        if existing_tag and existing_tag.id != tag_id:
            raise HTTPException(
                status_code=400,
                detail="A tag with this name or slug already exists.",
            )

    # Update the tag
    tag_data = tag_in.model_dump(exclude_unset=True)
    tag = await tag_crud.update_tag(db, tag_id=tag_id, tag_update=tag_data)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag_by_id(
    *,
    tag_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Delete a tag.
    """
    success = await tag_crud.delete_tag(db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None


@router.get("/{tag_id}/posts", response_model=list[PostRead])
async def get_posts_with_tag(
    tag_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Get all posts with a specific tag.
    """
    # Check if tag exists
    tag = await tag_crud.get_tag_by_id(db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Get posts with this tag
    posts = await get_posts_by_tag(db, tag_id=tag_id)
    return posts
