from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class TagBase(SQLModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: UUID


class TagUpdate(SQLModel):
    name: Optional[str] = None
    slug: Optional[str] = None