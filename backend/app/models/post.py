from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class Post(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
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
    comments: List["Comment"] = Relationship(back_populates="post")
