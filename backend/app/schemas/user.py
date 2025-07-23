from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime


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
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None