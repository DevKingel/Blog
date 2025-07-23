from sqlmodel import SQLModel, create_engine
from .models.user import User
from .models.post import Post
from .models.comment import Comment

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)