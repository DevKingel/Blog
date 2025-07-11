# 📘 Project Blueprint: Blog App

## 1\. 📝 Project Overview

-   **Name:** Blog App
-   **Description:** A modern, high-performance blog platform built with a decoupled architecture using FastAPI and Next.js. It is designed to be a secure, scalable, and user-friendly Single Page Application (SPA) with Server-Side Rendering (SSR) for optimal SEO and performance.
-   **Version:** `0.1`
-   **Start Date:** `2024-07-15`
-   **Repository URL:** `<Git repo URL for the project>`
-   **License:** `MIT`
-   **Authors:**
    -   Name: `<Your Name/Team Name>`
    -   Role: `<e.g., Full-Stack Developer>`
    -   Email: `<your-email@example.com>`

---

## 2\. 🎯 Project Purpose

-   **What is being built?** A feature-rich blog application that allows users to create, publish, and share articles. It will also provide a great reading experience with features like comments and social sharing.
-   **Why is it being built?** To provide a modern, fast, and secure platform for content creators and readers, addressing the shortcomings of older, monolithic blogging platforms.
-   **Who is it for?** Content creators (bloggers, writers, journalists), businesses that need a content marketing platform, and general readers.
-   **What problems does it solve?** Slow load times, poor mobile experience, security vulnerabilities, and limited SEO capabilities found in many existing blog solutions.
-   **Success Metrics:** High user engagement, growth in the number of published articles, excellent performance metrics, and positive user feedback.
-   **Key Performance Indicators (KPIs):**
    -   **User Engagement:** `Monthly Active Users (MAU) > 10,000`
    -   **Content Growth:** `>100 new articles published per month`
    -   **Performance:** `Page Load Time (LCP) < 2.5s`, `API response time < 150ms for 99% of requests`
    -   **SEO:** `Top 10 ranking for target keywords within 6 months`
    -   **User Satisfaction:** `User satisfaction score > 8/10`

---

## 3\. 🧩 Tasks & Priorities for MVP

| ID  | Title                                                         | Priority | User Story ID  | Dependencies | Status |
| --- | ------------------------------------------------------------- | -------- | -------------- | ------------ | ------ |
| T01 | Setup Docker environment for all services                     | High     | -              |              | To Do  |
| T02 | Design and implement User & Role DB Schema (Many-to-Many)     | High     | US-001, US-006 |              | To Do  |
| T03 | Implement User Authentication API (FastAPI)                   | High     | US-001         | T02          | To Do  |
| T04 | Create Login/Register Page UI (Next.js)                       | High     | US-001         | T03          | To Do  |
| T05 | Design and implement Article DB Schema                        | High     | US-002         |              | To Do  |
| T06 | Implement Article CRUD API (FastAPI)                          | High     | US-002         | T05          | To Do  |
| T07 | Create "New Post" and "Edit Post" UI (Next.js)                | High     | US-002         | T06          | To Do  |
| T08 | Implement Public Article View (Next.js with SSR)              | High     | US-003         | T06          | To Do  |
| T09 | Implement Redis caching for articles                          | Medium   | -              | T06          | To Do  |
| T10 | Design and implement Comments DB Schema                       | Medium   | US-004         |              | To Do  |
| T11 | Implement Comments API (FastAPI)                              | Medium   | US-004         | T10          | To Do  |
| T12 | Implement Comments section UI (Next.js)                       | Medium   | US-004         | T11          | To Do  |
| T13 | Design and implement Category & Tags DB Schema                | High     | US-005         | T05          | To Do  |
| T14 | Implement Category & Tags CRUD API (FastAPI)                  | High     | US-005         | T13          | To Do  |
| T15 | Update "New/Edit Post" UI for Category/Tag selection          | High     | US-002         | T07, T14     | To Do  |
| T16 | Implement pages to view articles by Category/Tag              | Medium   | US-005         | T14          | To Do  |
| T17 | Design Admin Panel UI                                         | High     | US-006         |              | To Do  |
| T18 | Implement Admin API endpoints (metrics, user/role management) | High     | US-006         | T02          | To Do  |
| T19 | Implement Role-Based Access Control (RBAC) in API             | High     | US-006         | T03          | To Do  |
| T20 | Design User Settings Page UI                                  | Medium   | US-007         |              | To Do  |
| T21 | Implement User Settings API endpoints                         | Medium   | US-007         | T03          | To Do  |

---

## 4\. 🧰 Tech Stack

### Languages

-   Python `3.13.5`
-   Node.js `24.4`

### Frameworks

-   FastAPI `0.116.0`
-   Next.js `15.3`

### Databases

-   PostgreSQL `17.5`
-   Redis `8.0.3`

### Dev Tools

-   Docker `28.3.2`
-   Git `2.43.3`

---

## 5\. 🌱 Environment Variables

-   `POSTGRES_USER`: **Purpose:** Username for the PostgreSQL database.
-   `POSTGRES_PASSWORD`: **Purpose:** Password for the PostgreSQL database.
-   `POSTGRES_DB`: **Purpose:** Name of the PostgreSQL database.
-   `DATABASE_URL`: **Purpose:** Connection string for the PostgreSQL database.
-   `REDIS_URL`: **Purpose:** Connection string for the Redis cache.
-   `JWT_SECRET_KEY`: **Purpose:** Secret key for signing and verifying JSON Web Tokens.
-   `JWT_ALGORITHM`: **Purpose:** Algorithm for JWT signing (e.g., HS256).
-   `NEXT_PUBLIC_API_URL`: **Purpose:** Base URL for the FastAPI backend, accessible from the Next.js client.

### Configuration Files

-   **`.env`**: For FastAPI/Docker/Next.js local development.
-   **`.env.development`**: For FastAPI/Docker/Next.js development-specific settings.
-   **`.env.production`**: For FastAPI/Docker/Next.js production-specific settings.
-   **`compose.yaml`**: Defines the services, networks, and volumes for the production application.
-   **`compose.override.yaml`**: Defines the services for the development environment, configured for hot-reloading and interactive dependency management.
-   **`next.config.js`**: Next.js configuration file.
-   **`ci.yaml`**: GitHub Actions workflow for continuous integration (linting, testing, building).
-   **`deploy.yaml`**: GitHub Actions workflow for continuous deployment.
-   **`dependabot.yaml`**: Dependabot configuration file.
-   **`alembic.ini`**: Alembic configuration file.

---

## 6\. 🧱 Architecture

-   **Diagram:** `docs/architecture.png` (A diagram showing Next.js client, FastAPI backend, PostgreSQL DB, and Redis cache as separate, containerized services).

### Modules

-   **API Service (FastAPI):** Handles all business logic, RESTful API endpoints, and database interactions. Implements role-based access control.
-   **Web Client (Next.js):** A Single Page Application (SPA) responsible for all UI rendering. Includes a public-facing site, a user settings area, and a protected admin panel. It will use Server-Side Rendering (SSR) for initial page loads for performance and SEO, and client-side rendering for subsequent navigation.
-   **Database (PostgreSQL):** The primary data store for users, roles, articles, comments, etc.
-   **Cache (Redis):** Used for caching frequently accessed data, such as published articles and site-wide metrics, to reduce database load and improve response times.

### API Specification

-   **Specification File:** `docs/openapi.json`. The API will be self-documenting via FastAPI's automatic OpenAPI generation.

### Data Flow Example: Creating a New Post

1.  A logged-in user with the 'WRITER' role submits the new post content from the `Web Client` (Next.js).
2.  The `Web Client` sends a `POST` request with the article data (including `category_id` and an array of `tags`) and the user's JWT to the `API Service`'s `/api/v1/articles/` endpoint.
3.  The `API Service` (FastAPI) validates the JWT, authorizes the user by checking for the 'WRITER' role, and validates the incoming article data.
4.  The `API Service` saves the new article to the `PostgreSQL Database` and creates associations in the `article_tags` table.
5.  The `API Service` invalidates any relevant caches in `Redis`.
6.  The `API Service` returns a `201 Created` response with the newly created article data.
7.  The `Web Client` redirects the user to the newly created article page.

### State Management (Frontend)

-   **Strategy:** The `Web Client` will use **React Context** for global state management (e.g., user authentication status and an array of roles). For more complex state, a library like **Zustand** or **Redux Toolkit** could be employed. Server-side data fetching and caching will be handled by Next.js's built-in capabilities and libraries like SWR or React Query.

---

## 7\. 🎨 UI/UX Design

### Principles

-   **Mobile-First:** The design will be optimized for mobile devices first, then scaled up for tablet and desktop.
-   **Responsiveness:** The layout will be fully responsive and adapt to all screen sizes.
-   **Simplicity & Clarity:** A clean, minimalist design to keep the focus on the content.
-   **Accessibility:** Adherence to WCAG 2.1 AA standards to ensure the app is usable by everyone.

### User Flows

-   **`UF-001`: User Registration & Login**
-   **`UF-002`: Create and Publish a New Article**
-   **`UF-003`: Read an Article and View Comments**
-   **`UF-004`: Add a Comment to an Article**
-   **`UF-005`: Filter Content by Category/Tag**
-   **`UF-006`: Admin Manages Content & Views Metrics**
-   **`UF-007`: User Modifies Profile Settings**

### Component Library

-   A custom component library will be built using **Tailwind CSS** to ensure a consistent and modern design. Components will be developed in isolation, possibly using Storybook.

### Wireframes & Mockups

-   `Home Page Wireframe`: \`\`
-   `Article Page Wireframe`: \`\`
-   `Admin Panel Mockup`: \`\`
-   `User Settings Mockup`: \`\`
-   `High-Fidelity Mockups`: \`\`

### Style Guide

-   **Colors:** A modern and accessible color palette.
-   **Typography:** Legible and well-structured typography using web fonts (e.g., from Google Fonts).
-   **Accessibility Standards:** `WCAG 2.1 AA`

---

## 8\. 👤 User Stories

-   **US-001: User Registration**

    -   **Title:** User can register for an account.
    -   **Description:** As a new user, I want to create an account so that I can comment on articles.
    -   **Acceptance Criteria:**
        -   User can register with a username, email, and password.
        -   User is assigned the default 'USER' role.
        -   User is automatically logged in upon successful registration.

-   **US-002: Article Creation**

    -   **Title:** Writer can create and publish an article.
    -   **Description:** As a logged-in user with the 'WRITER' role, I want to create, save as a draft, and publish an article.
    -   **Acceptance Criteria:**
        -   A user with the 'WRITER' role can create a new article with a title, content (supporting Markdown), and a featured image.
        -   A user must select one category for the article.
        -   A user can add multiple, specific tags to the article.
        -   A user can save an article as a draft or publish it.
        -   Published articles are publicly accessible via a unique URL (slug).
        -   Users without the 'WRITER' role cannot access the article creation/editing pages.

-   **US-003: Article Reading**

    -   **Title:** Any user can read a published article.
    -   **Description:** As a visitor, I want to be able to read published articles without needing an account.
    -   **Acceptance Criteria:**
        -   The article page loads quickly (SSR).
        -   The content is well-formatted and easy to read.

-   **US-004: Commenting**

    -   **Title:** Logged-in user can comment on an article.
    -   **Description:** As a logged-in user, I want to add comments to articles to engage in discussions.
    -   **Acceptance Criteria:**
        -   Any logged-in user (regardless of role) can submit a comment on an article.
        -   Comments are displayed below the article content.

-   **US-005: Content Discovery**

    -   **Title:** Filter articles by category or tag.
    -   **Description:** As a user, I want to see all articles belonging to a specific category or tag so I can discover content relevant to my interests.
    -   **Acceptance Criteria:**
        -   Clicking on a category name shows all articles in that category.
        -   Clicking on a tag shows all articles with that tag.

-   **US-006: Admin Management**

    -   **Title:** Admin can manage content, users, and view site metrics.
    -   **Description:** As an Admin, I want to access a protected dashboard to manage all articles, assign roles to users, and view analytics so I can moderate the platform.
    -   **Acceptance Criteria:**
        -   Only users with the 'ADMIN' role can access the `/admin` route.
        -   The admin panel displays key metrics.
        -   The admin can perform CRUD operations on any article.
        -   The admin can assign/revoke roles for any user.

-   **US-007: User Profile Management**
    -   **Title:** User can manage their settings.
    -   **Description:** As a logged-in user, I want to access a settings page where I can update my profile information (e.g., username, email) and change my password.
    -   **Acceptance Criteria:**
        -   A user can navigate to a `/settings` page.
        -   A user can update their own profile information.
        -   A user can change their password.

---

## 9\. ✅ Acceptance Tests

-   **AT-001: Successful Registration & Login**

    -   **Related Story:** `US-001`
    -   **Steps:** Navigate to `/register`, fill in the form, submit.
    -   **Expected Result:** User is redirected to their dashboard/homepage and their session is active.

-   **AT-002: Article Creation Access Control**

    -   **Related Story:** `US-002`
    -   **Steps:** Login as a user with the 'WRITER' role. Navigate to `/posts/new`.
    -   **Expected Result:** The article creation page is displayed.
    -   **Steps (Negative):** Login as a user with only the 'USER' role. Navigate to `/posts/new`.
    -   **Expected Result:** Access is denied.

-   **AT-003: Admin Panel Access**
    -   **Related Story:** `US-006`
    -   **Steps:** Login as a user with the 'ADMIN' role. Navigate to `/admin`.
    -   **Expected Result:** The admin panel is displayed.
    -   **Steps (Negative):** Login as a user with 'USER' or 'WRITER' roles. Navigate to `/admin`.
    -   **Expected Result:** Access is denied, user is redirected or shown a 403 Forbidden error.

---

## 10\. ⚡ Performance & SEO

-   **Performance Budget:**
    -   **LCP:** < 2.5s
    -   **FID:** < 100ms
    -   **CLS:** < 0.1
-   **SEO Strategy:**
    -   **Server-Side Rendering (SSR):** All public pages (homepage, article pages, category/tag pages) will be server-rendered for fast initial load and full indexability by search engines.
    -   **Metadata:** Dynamic generation of `<title>`, `<meta description>`, and other relevant meta tags for each page.
    -   **Structured Data:** Use of JSON-LD for rich snippets (e.g., for articles).
    -   **Sitemap:** Automatic generation of `sitemap.xml`.

---

## 11\. 🗄️ Database Schema

### `roles` table

| Column | Data Type     | Constraints          | Description                                  |
| ------ | ------------- | -------------------- | -------------------------------------------- |
| `id`   | `UUID`        | `PRIMARY KEY`        | Unique identifier for the role               |
| `name` | `VARCHAR(50)` | `NOT NULL`, `UNIQUE` | Name of the role (e.g., ADMIN, WRITER, USER) |

### `users` table

| Column            | Data Type      | Constraints                 | Description                    |
| ----------------- | -------------- | --------------------------- | ------------------------------ |
| `id`              | `UUID`         | `PRIMARY KEY`               | Unique identifier for the user |
| `username`        | `VARCHAR(50)`  | `NOT NULL`, `UNIQUE`        | User's unique username         |
| `email`           | `VARCHAR(255)` | `NOT NULL`, `UNIQUE`        | User's email address           |
| `hashed_password` | `VARCHAR(255)` | `NOT NULL`                  | Hashed user password           |
| `created_at`      | `TIMESTAMPTZ`  | `NOT NULL`, `DEFAULT NOW()` | Timestamp of record creation   |

### `user_roles` (Join Table)

| Column    | Data Type | Constraints                            | Description    |
| --------- | --------- | -------------------------------------- | -------------- |
| `user_id` | `UUID`    | `PRIMARY KEY`, `FOREIGN KEY(users.id)` | ID of the user |
| `role_id` | `UUID`    | `PRIMARY KEY`, `FOREIGN KEY(roles.id)` | ID of the role |

### `categories` table

| Column | Data Type      | Constraints          | Description                             |
| ------ | -------------- | -------------------- | --------------------------------------- |
| `id`   | `UUID`         | `PRIMARY KEY`        | Unique identifier for the category      |
| `name` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` | Name of the category (e.g., Technology) |
| `slug` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` | URL-friendly slug for the category      |

### `tags` table

| Column | Data Type      | Constraints          | Description                    |
| ------ | -------------- | -------------------- | ------------------------------ |
| `id`   | `UUID`         | `PRIMARY KEY`        | Unique identifier for the tag  |
| `name` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` | Name of the tag (e.g., nodejs) |
| `slug` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` | URL-friendly slug for the tag  |

### `articles` table

| Column         | Data Type      | Constraints                              | Description                       |
| -------------- | -------------- | ---------------------------------------- | --------------------------------- |
| `id`           | `UUID`         | `PRIMARY KEY`                            | Unique identifier for the article |
| `author_id`    | `UUID`         | `NOT NULL`, `FOREIGN KEY(users.id)`      | ID of the authoring user          |
| `category_id`  | `UUID`         | `NOT NULL`, `FOREIGN KEY(categories.id)` | ID of the article's category      |
| `slug`         | `VARCHAR(255)` | `NOT NULL`, `UNIQUE`                     | URL-friendly slug for the article |
| `title`        | `VARCHAR(255)` | `NOT NULL`                               | Title of the article              |
| `content`      | `TEXT`         | `NOT NULL`                               | Content of the article (Markdown) |
| `is_published` | `BOOLEAN`      | `NOT NULL`, `DEFAULT FALSE`              | Whether the article is published  |
| `created_at`   | `TIMESTAMPTZ`  | `NOT NULL`, `DEFAULT NOW()`              | Timestamp of record creation      |
| `updated_at`   | `TIMESTAMPTZ`  | `NOT NULL`, `DEFAULT NOW()`              | Timestamp of last record update   |

### `article_tags` (Join Table)

| Column       | Data Type | Constraints                               | Description       |
| ------------ | --------- | ----------------------------------------- | ----------------- |
| `article_id` | `UUID`    | `PRIMARY KEY`, `FOREIGN KEY(articles.id)` | ID of the article |
| `tag_id`     | `UUID`    | `PRIMARY KEY`, `FOREIGN KEY(tags.id)`     | ID of the tag     |

---

## 12\. 🔌 Integrations

-   **Email Service:** (Optional for MVP)
-   **Image Storage:** (Optional for MVP)

---

## 13\. 🔍 Observability & Ops

### Logging

-   **Strategy:** Structured logging (JSON format) for both FastAPI and Next.js applications. Logs will be output to `stdout` to be managed by Docker.

### Metrics

-   **Strategy:** The FastAPI application will expose a `/metrics` endpoint for Prometheus to scrape. Key metrics will include request latency, error rates, and database performance.

### Tracing

-   **Strategy:** (Post-MVP) Implement distributed tracing using OpenTelemetry to trace requests across the Next.js and FastAPI services.

---

## 14\. 🔄 CI/CD

-   **Provider:** GitHub Actions
-   **Workflows:**
    -   **`ci.yml`:** On every push to `main` or a PR, this workflow will:
        1. Lint the code (Python & JS).
        2. Run unit and integration tests for both frontend and backend.
        3. Build Docker images.
    -   **`deploy.yml`:** On merge to `main`, this workflow will:
        1. Push Docker images to a container registry (e.g., Docker Hub, AWS ECR).
        2. Deploy the new versions to the production environment.

---

## 15\. 📚 Documentation

-   **API Documentation:** Automatically generated and served by FastAPI at `/docs`.
-   **README.md:** Detailed instructions for setting up and running the project locally using Docker.
-   **Component Documentation:** (Optional) Storybook for the Next.js components.

---

## 16\. 🔐 Security

-   **Authentication:** JWT-based authentication. Access tokens will be short-lived, with a refresh token mechanism.
-   **Authorization:** Role-based access control (RBAC) will be implemented in the FastAPI backend. API endpoints will be protected by dependencies that verify the user has the required role (e.g., 'WRITER', 'ADMIN') in their list of assigned roles.
-   **Password Security:** Passwords will be hashed using `bcrypt`.
-   **Input Validation:** Pydantic will be used in FastAPI for rigorous input validation to prevent injection attacks.
-   **CORS:** A strict Cross-Origin Resource Sharing (CORS) policy will be configured in FastAPI.
-   **HTTPS:** The application will be served over HTTPS in production.
-   **Dependency Scanning:** Use of tools like Dependabot or Snyk to scan for vulnerabilities in dependencies.

---

## 17\. 🧭 Governance

-   **Versioning Policy:** Semantic Versioning.
-   **Code Style:** `black` and `isort` for Python, `prettier` for JavaScript/TypeScript.
-   **Branching Strategy:** GitFlow (or a simplified version with `master` and feature branches).
-   **Commit Strategy:** Feature branches for new features, bugfixes, etc., should be squashed into a single, meaningful commit when merging into the `master` branch to maintain a clean and understandable git history.
-   **Testing Requirement:** All new features must be accompanied by corresponding unit tests to ensure code quality, verify functionality, and prevent regressions.

---

## 18\. ⚙️ Environment Configuration

This project will require separate configurations for different environments to ensure security and proper behavior.

-   **Development:** Geared for local development with features like hot-reloading, debug mode enabled, and connection to local Docker services.
-   **Testing:** Uses a dedicated test database and may disable certain services to isolate tests.
-   **Production:** Optimized for performance and security. Debug mode is disabled, and it connects to production-level services and databases.

### Configuration Strategy

-   **Docker:** Separate `compose.yaml` files will be used for each environment (e.g., `compose.production.yaml` for production, `compose.override.yaml` for development). The development compose file will mount local code volumes for hot-reloading.
-   **Backend (FastAPI):** Configuration will be managed via environment variables, loaded using Pydantic's `BaseSettings`. `.env` will be used for shared settings, `.env.development` for development-specific settings, and `.env.production` for production settings.
-   **Frontend (Next.js):** Next.js has built-in support for environment variables. `.env` will be used for shared settings, `.env.development` for development-specific settings, and `.env.production` for production settings.

This approach ensures that sensitive information like production database credentials or API keys are not hardcoded or exposed in the development environment.

### Development Docker Services

The `compose.override.yaml` file is designed for an interactive and flexible development workflow. It allows developers to manage dependencies directly within the running containers, mimicking a local setup while maintaining containerization benefits.

-   **Backend (FastAPI & uv)** 🐍

    -   **Purpose:** Runs the FastAPI application with hot-reloading.
    -   **Dependency Management:** The service mounts the `backend/` source code as a volume. To add or remove a Python package, a developer can open a shell in the running container (`docker-compose exec backend bash`). Inside the container, they can use **`uv`** to manage dependencies (e.g., `uv add <package>`). This provides a fast and interactive way to manage Python dependencies without rebuilding the image.

-   **Frontend (Next.js & pnpm)** ⚛️

    -   **Purpose:** Runs the Next.js development server with Hot Module Replacement (HMR).
    -   **Dependency Management:** The service mounts the `frontend/` source code as a volume. Similar to the backend, a developer can get a shell in the container (`docker-compose exec frontend bash`) and use `pnpm` to add/remove dependencies (e.g., `pnpm add <package>`). Changes are immediately reflected in the `package.json` and lock files on the host machine.

-   **E2E Testing (Playwright)** 🎭
    -   **Purpose:** Provides an on-demand environment for running end-to-end tests.
    -   **Configuration:** This service uses the official Microsoft Playwright image, which comes with all necessary browser binaries and dependencies pre-installed. It mounts the frontend code so it can access the test files.
    *   **Workflow:** This service does not run continuously. It is started on-demand by the developer to execute the test suite against the running frontend and backend services using a command like `docker-compose run --rm playwright npx playwright test`.

---

## 19\. 📁 Suggested Directory Structure

```
blog-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── (admin)/
│   │   ├── (user)/
│   │   └── (public)/
│   ├── components/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── docs/
│   └── architecture.png
├── docker-compose.yml
├── docker-compose.dev.yml
└── README.md
```
