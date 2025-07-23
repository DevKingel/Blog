from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class CategoryBase(SQLModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    slug: Optional[str] = None