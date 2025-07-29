from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, text
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, Relationship, SQLModel

from .user_role import UserRole

if TYPE_CHECKING:
    from .comment import Comment
    from .post import Post
    from .role import Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50, nullable=False)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=text("NOW()")
        ),
    )

    # Relationships
    comments: list["Comment"] = Relationship(back_populates="user")
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)
    posts: list["Post"] = Relationship(back_populates="author")

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"
