from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .post_tag import PostTag

if TYPE_CHECKING:
    from .post import Post


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50, nullable=False)
    slug: str = Field(unique=True, index=True, max_length=50, nullable=False)

    # Relationships
    posts: list["Post"] = Relationship(back_populates="tags", link_model=PostTag)

    def __repr__(self):
        return f"<Tag name={self.name} slug={self.slug}>"
