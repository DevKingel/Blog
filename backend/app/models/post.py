from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .post_tag import PostTag

if TYPE_CHECKING:
    from .category import Category
    from .comment import Comment
    from .stat import Stat
    from .tag import Tag
    from .user import User


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="users.id", nullable=False)
    category_id: UUID = Field(foreign_key="categories.id", nullable=False)
    slug: str = Field(unique=True, index=True, max_length=255, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    content: str
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    author: Optional["User"] = Relationship(back_populates="posts")
    category: Optional["Category"] = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
    tags: list["Tag"] = Relationship(back_populates="posts", link_model=PostTag)
    stat: Optional["Stat"] = Relationship(back_populates="post")
