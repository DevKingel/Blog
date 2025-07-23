from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional, List
from datetime import datetime


class PostBase(SQLModel):
    author_id: UUID
    category_id: UUID
    slug: str
    title: str
    content: str
    is_published: bool = False


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None