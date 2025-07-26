from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RoleBase(SQLModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: UUID


class RoleUpdate(SQLModel):
    name: str | None = None
