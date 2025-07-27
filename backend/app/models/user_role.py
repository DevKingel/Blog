from uuid import UUID

from sqlmodel import Field, SQLModel


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"
