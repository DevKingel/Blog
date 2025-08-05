from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class MediaBase(SQLModel):
    filename: str
    content_type: str
    file_size: int


class MediaCreate(MediaBase):
    pass


class MediaRead(MediaBase):
    id: UUID
    user_id: UUID
    file_path: str
    created_at: datetime
    updated_at: datetime


class MediaUpdate(SQLModel):
    filename: str | None = None