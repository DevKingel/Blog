from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    comments: List["Comment"] = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="author")

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"