from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime


class CommentBase(SQLModel):
    user_id: UUID
    post_id: UUID
    parent_comment_id: Optional[UUID] = None
    content: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CommentUpdate(SQLModel):
    content: Optional[str] = None