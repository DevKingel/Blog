from sqlmodel import SQLModel, create_engine

from .models.comment import Comment
from .models.post import Post
from .models.user import User

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
