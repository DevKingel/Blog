from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class CommentBase(SQLModel):
    user_id: UUID
    post_id: UUID
    parent_comment_id: UUID | None = None
    content: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CommentUpdate(SQLModel):
    content: str | None = None
