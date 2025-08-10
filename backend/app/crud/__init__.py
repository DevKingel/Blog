# Import auth schema classes directly from schemas directory
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    PasswordResetSuccess,
    RefreshTokenRequest,
    ResetPasswordRequest,
    Token,
    TokenData,
)

# Import category schema classes directly from schemas directory
from app.schemas.category import (
    CategoryBase,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)

# Import comment schema classes directly from schemas directory
from app.schemas.comment import CommentBase, CommentCreate, CommentRead, CommentUpdate

# Import post schema classes directly from schemas directory
from app.schemas.post import PostBase, PostCreate, PostRead, PostUpdate

# Import post_tag schema classes directly from schemas directory
from app.schemas.post_tag import PostTagBase, PostTagCreate, PostTagRead, PostTagUpdate

# Import profile schema classes directly from schemas directory
from app.schemas.profile import ProfileRead, ProfileUpdate

# Import role schema classes directly from schemas directory
from app.schemas.role import RoleBase, RoleCreate, RoleRead, RoleUpdate

# Import search schema classes directly from schemas directory
from app.schemas.search import (
    CategorySearchResult,
    PostSearchResult,
    TagSearchResult,
    UserSearchResult,
)

# Import stat schema classes directly from schemas directory
from app.schemas.stat import StatBase, StatsCreate, StatsRead, StatUpdate

# Import tag schema classes directly from schemas directory
from app.schemas.tag import TagBase, TagCreate, TagRead, TagUpdate

# Import user schema classes directly from schemas directory
from app.schemas.user import UserBase, UserCreate, UserRead, UserUpdate

# Import user_role schema classes directly from schemas directory
from app.schemas.user_role import (
    UserRoleBase,
    UserRoleCreate,
    UserRoleRead,
    UserRoleUpdate,
)

# Import category CRUD functions from CRUD module
from .category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    search_categories,
    update_category,
)

# Import comment CRUD functions from CRUD module
from .comment import (
    create_comment,
    delete_comment,
    get_all_comments,
    get_comment_by_id,
    get_comments_by_post,
    get_comments_by_user,
    get_replies_by_comment,
    update_comment,
)

# Import post CRUD functions from CRUD module
from .post import (
    create_post,
    delete_post,
    get_all_posts,
    get_post_by_id,
    get_posts_by_author,
    get_posts_by_category,
    get_posts_by_tag,
    search_posts,
    update_post,
)

# Import post_tag CRUD functions from CRUD module
from .post_tag import (
    create_post_tag,
    delete_post_tag,
    get_all_post_tags,
    get_post_tag_by_ids,
    update_post_tag,
)

# Import role CRUD functions from CRUD module
from .role import (
    create_role,
    delete_role,
    get_all_roles,
    get_role_by_id,
    update_role,
)

# Import stat CRUD functions from CRUD module
from .stat import (
    create_stat,
    decrement_post_likes,
    delete_stat,
    get_all_stats,
    get_site_stats,
    get_stat_by_id,
    get_stat_by_post_id,
    get_user_stats,
    increment_post_likes,
    increment_post_views,
    update_stat,
)

# Import tag CRUD functions from CRUD module
from .tag import (
    create_tag,
    delete_tag,
    get_all_tags,
    get_tag_by_id,
    get_tag_by_name_or_slug,
    search_tags,
    update_tag,
)

# Import user CRUD functions from CRUD module
from .user import (
    create_user,
    delete_user,
    get_multi_user,
    get_password_hash,
    get_user_by_email,
    get_user_by_id,
    search_users,
    update_user,
    verify_password,
)

# Import user_role CRUD functions from CRUD module
from .user_role import (
    create_user_role,
    delete_user_role,
    get_all_user_roles,
    get_user_role_by_ids,
    update_user_role,
)

__all__ = [
    # Auth schema classes
    "ForgotPasswordRequest",
    "LoginRequest",
    "LogoutRequest",
    "PasswordResetSuccess",
    "RefreshTokenRequest",
    "ResetPasswordRequest",
    "Token",
    "TokenData",
    # Category schema classes
    "CategoryBase",
    "CategoryCreate",
    "CategoryRead",
    "CategoryUpdate",
    # Category CRUD functions
    "create_category",
    "get_category_by_id",
    "get_all_categories",
    "update_category",
    "delete_category",
    "search_categories",
    # Comment schema classes
    "CommentBase",
    "CommentCreate",
    "CommentRead",
    "CommentUpdate",
    # Comment CRUD functions
    "create_comment",
    "get_comment_by_id",
    "get_all_comments",
    "get_comments_by_post",
    "get_comments_by_user",
    "get_replies_by_comment",
    "update_comment",
    "delete_comment",
    # Post schema classes
    "PostBase",
    "PostCreate",
    "PostRead",
    "PostUpdate",
    # Post CRUD functions
    "create_post",
    "get_post_by_id",
    "get_all_posts",
    "get_posts_by_author",
    "search_posts",
    "update_post",
    "delete_post",
    "get_posts_by_category",
    "get_posts_by_tag",
    # PostTag schema classes
    "PostTagBase",
    "PostTagCreate",
    "PostTagRead",
    "PostTagUpdate",
    # PostTag CRUD functions
    "create_post_tag",
    "get_post_tag_by_ids",
    "get_all_post_tags",
    "update_post_tag",
    "delete_post_tag",
    # Profile schema classes
    "ProfileRead",
    "ProfileUpdate",
    # Role schema classes
    "RoleBase",
    "RoleCreate",
    "RoleRead",
    "RoleUpdate",
    # Role CRUD functions
    "create_role",
    "get_role_by_id",
    "get_all_roles",
    "update_role",
    "delete_role",
    # Stat schema classes
    "StatBase",
    "StatsCreate",
    "StatsRead",
    "StatUpdate",
    # Stat CRUD functions
    "create_stat",
    "get_stat_by_id",
    "get_stat_by_post_id",
    "get_all_stats",
    "update_stat",
    "delete_stat",
    "increment_post_views",
    "increment_post_likes",
    "decrement_post_likes",
    "get_site_stats",
    "get_user_stats",
    # Tag schema classes
    "TagBase",
    "TagCreate",
    "TagRead",
    "TagUpdate",
    # Tag CRUD functions
    "create_tag",
    "get_tag_by_id",
    "search_tags",
    "get_all_tags",
    "update_tag",
    "delete_tag",
    "get_tag_by_name_or_slug",
    # User schema classes
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # User CRUD functions
    "create_user",
    "get_user_by_id",
    "get_user_by_email",
    "get_multi_user",
    "update_user",
    "delete_user",
    "get_password_hash",
    "verify_password",
    "search_users",
    # UserRole schema classes
    "UserRoleBase",
    "UserRoleCreate",
    "UserRoleRead",
    "UserRoleUpdate",
    # UserRole CRUD functions
    "create_user_role",
    "get_user_role_by_ids",
    "get_all_user_roles",
    "update_user_role",
    "delete_user_role",
    # Search schema classes
    "PostSearchResult",
    "UserSearchResult",
    "CategorySearchResult",
    "TagSearchResult",
]
