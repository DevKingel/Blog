from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class StatsBase(SQLModel):
    post_id: UUID
    views: int = 0
    likes: int = 0


class StatsCreate(StatsBase):
    pass


class StatsRead(StatsBase):
    id: UUID


class StatsUpdate(SQLModel):
    views: Optional[int] = None
    likes: Optional[int] = None