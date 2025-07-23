from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional

class Stat(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="post.id")
    views: int = Field(default=0)
    likes: int = Field(default=0)

    def __repr__(self):
        return f"<Stat post_id={self.post_id} views={self.views} likes={self.likes}>"