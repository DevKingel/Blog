from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .post import Post


class Stat(SQLModel, table=True):
    __tablename__ = "stats"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id", unique=True)
    views: int = Field(default=0)
    likes: int = Field(default=0)

    # Relationships
    post: "Post" = Relationship(back_populates="stat")

    def __repr__(self):
        return f"<Stat post_id={self.post_id} views={self.views} likes={self.likes}>"
