from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class Role(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)

    def __repr__(self):
        return f"<Role name={self.name}>"