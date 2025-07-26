from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .comment import Comment
    from .post import Post


class User(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    comments: list["Comment"] = Relationship(back_populates="user")
    posts: list["Post"] = Relationship(back_populates="author")

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"
