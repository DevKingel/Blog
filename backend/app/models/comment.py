from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    post_id: UUID = Field(foreign_key="posts.id")
    parent_comment_id: UUID | None = Field(default=None, foreign_key="comments.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="comments")
    post: Optional["Post"] = Relationship(back_populates="comments")
    parent_comment: Optional["Comment"] = Relationship(
        back_populates="replies", sa_relationship_kwargs={"remote_side": "Comments.id"}
    )
    replies: list["Comment"] = Relationship(back_populates="parent_comment")
