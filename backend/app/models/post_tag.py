from uuid import UUID

from sqlmodel import Field, SQLModel


class PostTag(SQLModel, table=True):
    __tablename__ = "post_tags"

    post_id: UUID = Field(foreign_key="posts.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True)

    def __repr__(self):
        return f"<PostTag post_id={self.post_id} tag_id={self.tag_id}>"
