from uuid import UUID

from sqlmodel import SQLModel


class StatBase(SQLModel):
    post_id: UUID
    views: int = 0
    likes: int = 0


class StatsCreate(StatBase):
    pass


class StatsRead(StatBase):
    id: UUID


class StatUpdate(SQLModel):
    views: int | None = None
    likes: int | None = None
