from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


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
