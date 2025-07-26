from uuid import UUID

from sqlmodel import Field, SQLModel


class PostTag(SQLModel, table=True):
    post_id: UUID = Field(foreign_key="post.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)

    def __repr__(self):
        return f"<PostTag post_id={self.post_id} tag_id={self.tag_id}>"
