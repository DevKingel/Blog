from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Comment(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    post_id: UUID = Field(foreign_key="post.id")
    parent_comment_id: Optional[UUID] = Field(default=None, foreign_key="comment.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="comments")
    post: Optional["Post"] = Relationship(back_populates="comments")
    parent_comment: Optional["Comment"] = Relationship(back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"})
    replies: list["Comment"] = Relationship(back_populates="parent_comment")