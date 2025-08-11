from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Media(SQLModel, table=True):
    __tablename__ = "media"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    filename: str = Field(max_length=255, nullable=False)
    file_path: str = Field(max_length=500, nullable=False)
    content_type: str = Field(max_length=100, nullable=False)
    file_size: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    user: Optional["User"] = Relationship(back_populates="media")
