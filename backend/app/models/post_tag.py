from sqlmodel import SQLModel, Field
from uuid import UUID


class PostTag(SQLModel, table=True):
    post_id: UUID = Field(foreign_key="post.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)

    def __repr__(self):
        return f"<PostTag post_id={self.post_id} tag_id={self.tag_id}>"
