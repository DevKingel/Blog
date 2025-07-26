from uuid import UUID

from sqlmodel import Field, SQLModel


class PostTagBase(SQLModel):
    post_id: UUID
    tag_id: UUID


class PostTagCreate(PostTagBase):
    pass


class PostTagRead(PostTagBase):
    pass


class PostTagUpdate(SQLModel):
    pass
