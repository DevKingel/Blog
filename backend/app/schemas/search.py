from sqlmodel import SQLModel

from .post import PostRead
from .user import UserRead
from .category import CategoryRead
from .tag import TagRead


class PostSearchResult(SQLModel):
    posts: list[PostRead]
    total: int


class UserSearchResult(SQLModel):
    users: list[UserRead]
    total: int


class CategorySearchResult(SQLModel):
    categories: list[CategoryRead]
    total: int


class TagSearchResult(SQLModel):
    tags: list[TagRead]
    total: int