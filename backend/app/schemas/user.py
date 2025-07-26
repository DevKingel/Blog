from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    hashed_password: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID
    created_at: datetime


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    hashed_password: str | None = None
