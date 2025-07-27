from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .user_role import UserRole

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=20, nullable=False)
    description: str | None = Field(max_length=100, nullable=True)

    # Relationships
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)

    def __repr__(self):
        return f"<Role name={self.name}>"
