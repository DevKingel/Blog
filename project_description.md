# 📘 Project Blueprint Template

## 1. 📝 Project Overview
- **Name:** `FullStackBlog`
- **Description:** `A robust platform for creating, publishing, and interacting with blog posts, designed for scalability and modern development practices.`
- **Version:** ``
- **Start Date:** `2025-07-09`
- **Repository URL:** `<Git repo URL>`
- **License:** `MIT`
- **Authors:**
  - Name: `<Author Name>`
  - Role: `<e.g., Lead Engineer>`
  - Email: `<email@example.com>`

---

## 2. 🎯 Project Purpose
- **What is being built?** `A scalable and responsive full-stack blog platform`
- **Why is it being built?** `To provide a modern and flexible blog engine for content creators and readers`
- **Who is it for?** `Writers, developers, and content teams`
- **What problems does it solve?** `Lack of modern, easily extendable, and performant blog platforms`
- **Success Metrics:** `Number of active users, post engagement rate, performance metrics`

---

## 3. 🧹 Tasks & Priorities

| ID | Title                                  | Priority | Description                                          | Status |
|----|----------------------------------------|----------|------------------------------------------------------|--------|
| T01 | Set up PostgreSQL DB                  | High     | Create DB container with schema                      | To Do  |
| T02 | Initialize FastAPI backend project    | High     | Project scaffolding, dependencies, and structure     | To Do  |
| T03 | Define SQLAlchemy models              | High     | User, BlogPost, Comment, Tag, PostTags               | To Do  |
| T04 | Create Alembic migrations             | High     | Generate and apply DB schema                         | To Do  |
| T05 | Implement registration API            | High     | POST /auth/register with validation and hashing      | To Do  |
| T06 | Implement login API                   | High     | POST /auth/login, JWT return                         | To Do  |
| T07 | Create protected route example        | Medium   | GET /auth/me to test JWT auth                        | To Do  |
| T08 | CRUD endpoints for blog posts         | High     | Create, read, update, delete posts                   | To Do  |
| T09 | Implement tags endpoints              | Medium   | GET /tags, POST /tags                                | To Do  |
| T10 | Add comment endpoints                 | Medium   | GET/POST comments per post                           | To Do  |
| T11 | Implement Redis cache logic           | Medium   | Cache post lists and details                         | To Do  |
| T12 | Set up FastAPI exception handling     | Medium   | Custom error responses and logging                   | To Do  |
| T13 | Setup Dockerfile for backend          | High     | Dockerfile, Poetry/pip, .env                         | To Do  |
| T14 | Setup Dockerfile for frontend         | High     | Dockerfile for Next.js app                           | To Do  |
| T15 | Write docker-compose.yml              | High     | Link Redis, Postgres, frontend/backend               | To Do  |
| T16 | Initialize Next.js frontend           | High     | Scaffold project with Tailwind + shadcn              | To Do  |
| T17 | Create UI for login/register          | High     | Auth screens with forms and API calls                | To Do  |
| T18 | Create homepage layout and feed       | High     | List all published posts with pagination             | To Do  |
| T19 | Create post detail page               | High     | Full content + comments section                      | To Do  |
| T20 | Create post editor                    | Medium   | Markdown editor for new/edit post                   | To Do  |
| T21 | Implement UI state and API hooks      | Medium   | Zustand/Context for managing auth + fetch            | To Do  |
| T22 | Setup frontend protected routes       | Medium   | Restrict author-only pages                          | To Do  |
| T23 | Setup CI with GitHub Actions          | Medium   | Basic test + lint pipelines                         | To Do  |
| T24 | Setup test config (Pytest/Jest)       | Low      | Basic test cases for BE + FE                        | To Do  |
| T25 | Add Prometheus metrics to FastAPI     | Low      | Instrument FastAPI endpoints                        | To Do  |
| T26 | Setup Jaeger for tracing              | Low      | Add trace IDs + propagation                         | To Do  |

---

## 4. 🧰 Tech Stack
### Languages
- Python ``
- JavaScript ``

### Frameworks
- FastAPI
- Next.js (React)

### Databases
- PostgreSQL ``

### Dev Tools
- Docker ``
- Redis ``
- Git ``
- Node.js ``

### Libraries
- Frontend:
  - Tailwind CSS
  - shadcn/ui
  - lucide-react
  - Zustand
- Backend:
  - SQLAlchemy
  - Alembic
  - Pydantic
  - passlib

---

## 5. 🌱 Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secret key for signing tokens
- `API_URL`: Backend URL for the frontend

### Configuration Files
- `.env.development`
- `.env.production`

---

## 6. 🧱 Architecture
- **Diagram:** `docs/architecture.png`

### Modules
- **API Service:** FastAPI
- **Web Client:** Next.js
- **Database:** PostgreSQL
- **Caching:** Redis
- **Authentication:** JWT

---

## 7. 🎨 UI/UX Design
### Principles
- Modern and minimal
- Accessible
- Mobile-first responsive

### User Flows
- `UF-001`: Visitor views list of posts → clicks post → reads full article → comments.
- `UF-002`: Author logs in → creates a draft → publishes post.

### Wireframes
- `Home Screen`: `design/wireframes/home.png`

### Mockups
- `High-Fidelity Homepage`: `design/mockups/homepage.png`

### Style Guide
- **Colors:** Primary `#1f2937`, Secondary `#f3f4f6`, Accent `#3b82f6`
- **Typography:**
  - Headings: `Inter`
  - Body: `Inter`

### Accessibility
- Standards: `WCAG 2.1 AA`

---

## 8. 👤 User Stories
- **US-001**
  - **Title:** User Registration
  - **Description:** As a user, I want to register so I can write posts
  - **Acceptance Criteria:**
    - Form includes email, password fields
    - Passwords are hashed and stored securely

- **US-002**
  - **Title:** View Post Feed
  - **Description:** As a visitor, I want to browse posts by authors
  - **Acceptance Criteria:**
    - Posts are paginated
    - Show title, author, excerpt

---

## 9. ✅ Acceptance Tests
- **AT-001**
  - **Related Story:** US-001
  - **Steps:**
    - Fill registration form
    - Submit and confirm redirect
  - **Expected Result:** User gets redirected to login screen

---

## 10. ⚡ Performance
- **SLA:**
  - Latency: `<300ms`
  - Throughput: `1000 req/sec`

- **Tools:**
  - k6
  - Locust

---

## 11. 🗄️ Database Schema
### `users`
- `id`: UUID, PRIMARY KEY
- `username`: VARCHAR(255), UNIQUE, NOT NULL
- `email`: VARCHAR(255), UNIQUE, NOT NULL
- `hashed_password`: TEXT, NOT NULL
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### `blog_posts`
- `id`: UUID, PRIMARY KEY
- `author_id`: UUID, FOREIGN KEY(users.id)
- `title`: VARCHAR(255)
- `content`: TEXT
- `status`: ENUM('draft','published')
- `published_at`: TIMESTAMP
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### `comments`
- `id`: UUID, PRIMARY KEY
- `post_id`: UUID, FOREIGN KEY(blog_posts.id)
- `user_id`: UUID, FOREIGN KEY(users.id), NULLABLE
- `content`: TEXT
- `created_at`: TIMESTAMP

### `tags`
- `id`: UUID, PRIMARY KEY
- `name`: VARCHAR(100), UNIQUE

### `post_tags`
- `post_id`: UUID, FK(blog_posts.id)
- `tag_id`: UUID, FK(tags.id)
- PRIMARY KEY(post_id, tag_id)

---

## 12. 🔌 Integrations
- **Caching:** Redis
- **Auth Tokens:** JWT

---

## 13. 🔍 Observability & Ops
### Logging
- Level: `INFO`
- Outputs:
  - Console
  - File: `logs/app.log`

### Metrics
- Tool: Prometheus + Grafana

### Tracing
- Tool: Jaeger

### Error Management
- Strategy: Centralized Exception Handlers in FastAPI

---

## 14. 🔄 CI/CD
- **Provider:** GitHub Actions
- **Workflows:**
  - `validate`: `.github/workflows/validate.yml`
  - `build`: `.github/workflows/ci.yml`
  - `deploy`: `.github/workflows/deploy.yml`

---

## 15. 📚 Documentation
- **Main:** `docs/index.md`
- **API Reference:** FastAPI auto docs `/docs`
- **Style Guide:** Tailwind config
- **Onboarding:** `docs/onboarding.md`

---

## 16. 🔐 Security
- **Authentication:** JWT (with refresh tokens optional)
- **Secrets Management:** `.env` files
- **Best Practices:**
  - Hash passwords with bcrypt
  - Secure headers and HTTPS only

---

## 17. 🧭 Governance
- **Versioning:** Semantic Versioning
- **Retention:**
  - Logs: 90 days
  - Backups: 30 days

---

## 📁 Suggested Directory Structure
```
fullstackblog/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── public/
│   ├── styles/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env
└── README.md
```

---
