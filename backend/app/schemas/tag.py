from uuid import UUID

from sqlmodel import SQLModel


class TagBase(SQLModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: UUID


class TagUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
