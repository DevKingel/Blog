from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class CategoryBase(SQLModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID


class CategoryUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
