import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud import post as post_crud
from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    *,
    post_in: PostCreate,
    db: AsyncSession = Depends(get_session),
) -> Post:
    """
    Create new post.
    """
    try:
        post = Post(**post_in.model_dump())
        post = await post_crud.create_post(db, post)
        return post
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating post",
        ) from e


@router.put("/{post_id}", response_model=PostRead)
async def update_existing_post(
    *,
    post_id: uuid.UUID,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_session),
) -> Post:
    """
    Update an existing post.
    """
    try:
        db_post = await post_crud.get_post_by_id(db, post_id)
        if not db_post:
            raise HTTPException(
                status_code=404,
                detail="The post with this id does not exist in the system",
            )

        # Update the post with the new data
        update_data = post_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)

        # Update the updated_at timestamp
        db_post.updated_at = datetime.now(UTC)

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while updating post",
        ) from e


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(
    *,
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a post.
    """
    try:
        post = await post_crud.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await db.delete(post)
        await db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while deleting post",
        ) from e


@router.get("/drafts", response_model=list[PostRead])
async def read_draft_posts(
    *,
    db: AsyncSession = Depends(get_session),
) -> list[Post]:
    """
    Retrieve draft posts (for authenticated users).
    """
    try:
        query = (
            select(Post)
            .where(not Post.is_published)
            .options(
                selectinload(Post.author),
                selectinload(Post.category),
                selectinload(Post.comments),
                selectinload(Post.tags),
                selectinload(Post.stat),
            )
        )
        result = await db.execute(query)
        posts = result.scalars().all()
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching draft posts",
        ) from e


@router.get("/published", response_model=list[PostRead])
async def read_published_posts(
    *,
    db: AsyncSession = Depends(get_session),
) -> list[Post]:
    """
    Retrieve published posts.
    """
    try:
        query = (
            select(Post)
            .where(Post.is_published)
            .options(
                selectinload(Post.author),
                selectinload(Post.category),
                selectinload(Post.comments),
                selectinload(Post.tags),
                selectinload(Post.stat),
            )
        )
        result = await db.execute(query)
        posts = result.scalars().all()
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching published posts",
        ) from e


@router.post("/{post_id}/publish", response_model=PostRead)
async def publish_post(
    *,
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Post:
    """
    Publish a draft post.
    """
    try:
        db_post = await post_crud.get_post_by_id(db, post_id)
        if not db_post:
            raise HTTPException(
                status_code=404,
                detail="The post with this id does not exist in the system",
            )

        if db_post.is_published:
            raise HTTPException(
                status_code=400,
                detail="The post is already published",
            )

        # Update the post to published
        db_post.is_published = True
        db_post.published_at = datetime.now(UTC)
        db_post.updated_at = datetime.now(UTC)

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while publishing post",
        ) from e


@router.post("/{post_id}/unpublish", response_model=PostRead)
async def unpublish_post(
    *,
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
) -> Post:
    """
    Unpublish a published post.
    """
    try:
        db_post = await post_crud.get_post_by_id(db, post_id)
        if not db_post:
            raise HTTPException(
                status_code=404,
                detail="The post with this id does not exist in the system",
            )

        if not db_post.is_published:
            raise HTTPException(
                status_code=400,
                detail="The post is not published",
            )

        # Update the post to unpublished
        db_post.is_published = False
        db_post.updated_at = datetime.now(UTC)

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while unpublishing post",
        ) from e
