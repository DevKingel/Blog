from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class RoleBase(SQLModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: UUID


class RoleUpdate(SQLModel):
    name: Optional[str] = None