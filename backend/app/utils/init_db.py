import logging

from sqlmodel import Session, SQLModel

from app.models.category import Category
from app.models.comment import Comment
from app.models.post import Post
from app.models.post_tag import PostTag
from app.models.role import Role
from app.models.stat import Stat
from app.models.tag import Tag
from app.models.user import User
from app.models.user_role import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(session)

    # Add initial data
    # Users
    user1 = User(
        username="user1", email="user1@example.com", hashed_password="hashed_password1"
    )
    user2 = User(
        username="user2", email="user2@example.com", hashed_password="hashed_password2"
    )
    session.add(user1)
    session.add(user2)
    session.commit()

    # Roles
    role1 = Role(name="admin", description="Administrator")
    role2 = Role(name="editor", description="Editor")
    session.add(role1)
    session.add(role2)
    session.commit()

    # UserRoles
    user_role1 = UserRole(user_id=user1.id, role_id=role1.id)
    user_role2 = UserRole(user_id=user2.id, role_id=role2.id)
    session.add(user_role1)
    session.add(user_role2)
    session.commit()

    # Categories
    category1 = Category(name="Technology", slug="technology")
    category2 = Category(name="Lifestyle", slug="lifestyle")
    session.add(category1)
    session.add(category2)
    session.commit()

    # Tags
    tag1 = Tag(name="Python", slug="python")
    tag2 = Tag(name="SQLModel", slug="sqlmodel")
    session.add(tag1)
    session.add(tag2)
    session.commit()

    # Posts
    post1 = Post(
        author_id=user1.id,
        category_id=category1.id,
        slug="first-post",
        title="First Post",
        content="This is the first post.",
    )
    post2 = Post(
        author_id=user2.id,
        category_id=category2.id,
        slug="second-post",
        title="Second Post",
        content="This is the second post.",
    )
    session.add(post1)
    session.add(post2)
    session.commit()

    # PostTags
    post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
    post_tag2 = PostTag(post_id=post2.id, tag_id=tag2.id)
    session.add(post_tag1)
    session.add(post_tag2)
    session.commit()

    # Comments
    comment1 = Comment(user_id=user1.id, post_id=post1.id, content="Great post!")
    comment2 = Comment(
        user_id=user2.id, post_id=post2.id, content="Thanks for sharing."
    )
    session.add(comment1)
    session.add(comment2)
    session.commit()

    # Stats
    stat1 = Stat(post_id=post1.id, views=100, likes=10)
    stat2 = Stat(post_id=post2.id, views=200, likes=20)
    session.add(stat1)
    session.add(stat2)
    session.commit()


def main() -> None:
    logger.info("Initializing service")
    with Session(engine) as session:
        init_db(session)

    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
