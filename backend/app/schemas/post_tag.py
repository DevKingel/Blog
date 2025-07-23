from sqlmodel import SQLModel, Field
from uuid import UUID


class PostTagBase(SQLModel):
    post_id: UUID
    tag_id: UUID


class PostTagCreate(PostTagBase):
    pass


class PostTagRead(PostTagBase):
    pass


class PostTagUpdate(SQLModel):
    pass