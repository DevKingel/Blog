from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class StatBase(SQLModel):
    post_id: UUID
    views: int = 0
    likes: int = 0


class StatsCreate(StatBase):
    pass


class StatsRead(StatBase):
    id: UUID


class StatUpdate(SQLModel):
    views: Optional[int] = None
    likes: Optional[int] = None