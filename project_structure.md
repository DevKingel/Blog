```
your-blog-project/
├── .git/                      # Git version control directory
├── backend/
│   ├── Dockerfile             # Instructions to build the backend Docker image
│   ├── requirements.txt       # List of Python dependencies
│   ├── .env.example           # Template for environment variables
│   └── app/
│       ├── __init__.py
│       ├── main.py              # Main FastAPI application instance and router assembly
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py    # Reusable dependencies (get_current_user, role checks)
│       │   └── endpoints/
│       │       ├── __init__.py
│       │       ├── auth.py        # /register, /token endpoints
│       │       ├── posts.py       # CRUD endpoints for posts
│       │       ├── comments.py    # CRUD endpoints for comments
│       │       └── admin.py       # Endpoints for all admin functions (users, stats, etc.)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # Pydantic settings management (loads from .env)
│       │   └── security.py      # Password hashing and JWT functions
│       ├── db/
│       │   ├── __init__.py
│       │   ├── session.py       # SQLAlchemy engine and SessionLocal setup
│       │   ├── dependencies.py  # get_db dependency to provide sessions to endpoints
│       │   └── init_db.py       # Script to create initial database tables
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py          # User model, including roles and auth provider info
│       │   ├── post.py          # Article model, with creation/modification tracking
│       │   ├── comment.py       # Comments on articles
│       │   ├── category.py      # Category model
│       │   ├── tag.py           # Tag model
│       │   ├── article_tag.py   # Many-to-many relationship between articles and tags
│       │   └── stats.py         # View and interaction statistics
│       └── schemas/
│           ├── __init__.py
│           ├── user.py          # Pydantic schemas for User, UserCreate, UserUpdate
│           ├── post.py          # Pydantic schemas for Article CRUD
│           ├── comment.py       # Pydantic schemas for Comment creation and response
│           ├── category.py      # Pydantic schemas for categories
|           ├── tag.py           # Pydantic schemas for tags
|           ├── article_tag.py   # Pydantic schemas for the article-tag relationship
│           └── stats.py         # ArticleStats schema
├── frontend/
│   ├── Dockerfile             # Instructions to build the frontend Docker image
│   ├── package.json           # List of Node.js dependencies
│   ├── next.config.js         # Next.js configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── .env.example           # Template for frontend environment variables
│   ├── components/            # Reusable React components
│   │   ├── layout/
│   │   │   ├── Layout.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── posts/
│   │   │   ├── PostCard.tsx
│   │   │   └── ArticleBody.tsx
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   └── InputField.tsx
│   │   └── admin/
│   │       ├── DataTable.tsx
│   │       └── Chart.tsx
│   ├── lib/                   # Helper functions, API client, etc.
│   │   └── api.ts             # Functions for making calls to the backend API
│   ├── pages/                 # Application routes
│   │   ├── _app.tsx
│   │   ├── _document.tsx
│   │   ├── index.tsx          # Home page
│   │   ├── about.tsx
│   │   ├── login.tsx
│   │   ├── blog/
│   │   │   └── [slug].tsx     # Dynamic page for a single blog post
│   │   ├── admin/
│   │   │   ├── dashboard.tsx
│   │   │   └── users.tsx
│   │   └── writer/
│   │       └── dashboard.tsx
│   └── styles/
│       └── globals.css
├── .gitignore
├── docker-compose.yml             # Base Docker services definition
├── docker-compose.override.yml    # Development-specific overrides (volumes, ports)
├── docker-compose.production.yml  # Production-specific overrides
├── README.md
└── SITEMAP.xml                    # High-level plan for application structure
```
