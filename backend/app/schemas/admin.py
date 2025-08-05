from sqlmodel import SQLModel

from .post import PostRead
from .stat import SiteStatsRead
from .user import UserRead


class AdminStatsRead(SiteStatsRead):
    """
    Detailed admin statistics including additional metrics.
    """

    pass


class UserListRead(SQLModel):
    """
    Schema for listing users with pagination.
    """

    users: list[UserRead]
    total: int
    page: int
    size: int


class PostListRead(SQLModel):
    """
    Schema for listing posts with pagination.
    """

    posts: list[PostRead]
    total: int
    page: int
    size: int
