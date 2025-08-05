from sqlmodel import SQLModel

from .category import CategoryRead
from .post import PostRead
from .tag import TagRead
from .user import UserRead


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
