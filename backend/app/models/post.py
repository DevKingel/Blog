from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .category import Category
    from .comment import Comment
    from .user import User


class Post(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="user.id")
    category_id: UUID = Field(foreign_key="category.id")
    slug: str = Field(unique=True, index=True)
    title: str
    content: str
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: Optional["User"] = Relationship(back_populates="posts")
    category: Optional["Category"] = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
