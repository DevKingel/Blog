from sqlmodel import SQLModel, Field
from uuid import UUID


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"