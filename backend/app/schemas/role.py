from uuid import UUID

from sqlmodel import SQLModel


class RoleBase(SQLModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: UUID


class RoleUpdate(SQLModel):
    name: str | None = None
