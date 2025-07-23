from sqlmodel import SQLModel, Field
from uuid import UUID


class UserRoleBase(SQLModel):
    user_id: UUID
    role_id: UUID


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(UserRoleBase):
    pass


class UserRoleUpdate(SQLModel):
    pass