from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


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
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None
