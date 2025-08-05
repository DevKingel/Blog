from pydantic import BaseModel, EmailStr

from .user import UserRead


class ProfileRead(UserRead):
    pass


class ProfileUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
