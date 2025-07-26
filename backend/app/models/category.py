from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    slug: str = Field(unique=True, index=True)

    def __repr__(self):
        return f"<Category name={self.name} slug={self.slug}>"
