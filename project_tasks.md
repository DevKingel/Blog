# Project Tasks

## Phase 1: Project Setup & Foundation 🏗️

This phase creates the skeleton of your project, including architectural planning, directory structures, and Docker configuration.

-   **Project Architecture & Planning**
    -   `[ ]` Create a `SITEMAP.xml` file in the root directory. This file should outline the application's structure to guide development. It must include:
        -   **Public Pages:** Homepage (`/`), Blog Post (`/blog/[slug]`), Category View (`/category/[slug]`), Tag View (`/tag/[slug]`), Login (`/login`), Register (`/register`).
        -   **Authenticated Pages:** User Profile (`/profile`).
        -   **Writer Pages:** Writer Dashboard (`/writer/dashboard`), Post Editor (`/writer/editor/[id]`).
        -   **Admin Pages:** Admin Dashboard (`/admin/dashboard`), User Management (`/admin/users`), Content Management (`/admin/content`), Taxonomy Management (`/admin/categories`).
        -   **Key Components:** `Navbar`, `Footer`, `PostCard`, `CommentList`, `CommentForm`.
-   **Project Initialization**
    -   `[ ]` Create a root project directory.
    -   `[ ]` Initialize a `git` repository in the root directory.
    -   `[ ]` Create a `.gitignore` file with appropriate entries for Python, Node.js, and OS-specific files.
    -   `[ ]` Create a main `README.md` file with the project title.
-   **Initial File Structure**
    -   `[ ]` Create the `./backend` directory.
        -   `[ ]` Create `Dockerfile`, `requirements.txt`, `.env.example`, `pyproject.toml`, `README.md`, `uv.lock`, `alembic.ini` inside `./backend`.
        -   `[ ]` Create `app/` directory inside `./backend`.
            -   `[ ]` Create `__init__.py`, `main.py` inside `./backend/app`.
            -   `[ ]` Create `api/`, `core/`, `db/`, `models/`, `schemas/` directories inside `./backend/app`.
                -   `[ ]` Create `__init__.py` in each of these subdirectories.
                -   `[ ]` Create `dependencies.py` in `backend/app/api/`.
                -   `[ ]` Create `endpoints/` directory in `backend/app/api/`.
                    -   `[ ]` Create `__init__.py`, `auth.py`, `posts.py`, `comments.py`, `admin.py` in `backend/app/api/endpoints/`.
                -   `[ ]` Create `config.py`, `security.py` in `backend/app/core/`.
                -   `[ ]` Create `session.py`, `dependencies.py`, `init_db.py` in `backend/app/db/`.
                -   `[ ]` Create `user.py`, `post.py`, `comment.py`, `taxonomy.py`, `stats.py` in `backend/app/models/`.
                -   `[ ]` Create `user.py`, `post.py`, `comment.py`, `taxonomy.py`, `stats.py` in `backend/app/schemas/`.
    -   `[ ]` Create the `./frontend` directory.
        -   `[ ]` Create `Dockerfile`, `package.json`, `next.config.ts`, `tailwind.config.js`, `.env.example`, `postcss.config.mjs`, `README.md`, `tsconfig.json`, `eslint.config.mjs`, `pnpm-lock.yaml` inside `./frontend`.
        -   `[ ]` Create `components/`, `lib/`, `pages/`, `styles/`, `public/`, `app/` directories inside `./frontend`.
            -   `[ ]` Create `layout/` directory in `frontend/components/`.
                -   `[ ]` Create `Layout.tsx`, `Navbar.tsx`, `Footer.tsx` in `frontend/components/layout/`.
            -   `[ ]` Create `posts/` directory in `frontend/components/`.
                -   `[ ]` Create `PostCard.tsx`, `ArticleBody.tsx` in `frontend/components/posts/`.
            -   `[ ]` Create `ui/` directory in `frontend/components/`.
                -   `[ ]` Create `Button.tsx`, `InputField.tsx` in `frontend/components/ui/`.
            -   `[ ]` Create `admin/` directory in `frontend/components/`.
                -   `[ ]` Create `DataTable.tsx`, `Chart.tsx` in `frontend/components/admin/`.
            -   `[ ]` Create `api.ts` in `frontend/lib/`.
            -   `[ ]` Create `_app.tsx`, `_document.tsx`, `index.tsx`, `about.tsx`, `login.tsx` in `frontend/pages/`.
            -   `[ ]` Create `blog/` directory in `frontend/pages/`.
                -   `[ ]` Create `[slug].tsx` in `frontend/pages/blog/`.
            -   `[ ]` Create `admin/` directory in `frontend/pages/`.
                -   `[ ]` Create `dashboard.tsx`, `users.tsx` in `frontend/pages/admin/`.
            -   `[ ]` Create `writer/` directory in `frontend/pages/`.
                -   `[ ]` Create `dashboard.tsx` in `frontend/pages/writer/`.
            -   `[ ]` Create `globals.css` in `frontend/styles/`.
            -   `[ ]` Create `favicon.ico`, `globe.svg`, `next.svg`, `vercel.svg`, `window.svg`, `file.svg` in `frontend/public/`.
            -   `[ ]` Create `layout.tsx`, `page.tsx`, `globals.css`, `favicon.ico` in `frontend/app/`.
    -   `[ ]` Create `.gitignore`, `docker-compose.yml`, `docker-compose.override.yml`, `docker-compose.production.yml`, `README.md` in the root directory.
-   **Docker Configuration**
    -   `[ ]` Create a base `compose.yaml` file in the root.
    -   `[ ]` Define the `backend`, `frontend`, `db`, and `cache` services in `compose.yaml` without development-specific settings like ports or volumes.
    -   `[ ]` Configure a named volume in `compose.yaml` for PostgreSQL data persistence.
    -   `[ ]` Create a `compose.override.yaml` file. This file will automatically be used by Docker Compose in development.
    -   `[ ]` In `compose.override.yaml`, add development configurations: map local source code (`./backend:/app`, `./frontend:/app`) into the containers and expose ports (`8000:8000`, `3000:3000`).
    -   `[ ]` In `compose.override.yaml`, configure `backend` service to use `uv` for dependency management and hot-reloading.
    -   `[ ]` In `compose.override.yaml`, configure `frontend` service to use `pnpm` for dependency management and Hot Module Replacement (HMR).
    -   `[ ]` In `compose.override.yaml`, add an `e2e_testing` service using the official Microsoft Playwright image, mounting frontend code for on-demand E2E tests.
    -   `[ ]` Create a `compose.production.yaml` file for production-specific settings.
    -   `[ ]` In `compose.production.yaml`, configure services to use production environment files and not mount local source code.
    -   `[ ]` Create a `.env.example` file in the `./backend` directory, listing variables like `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `REDIS_URL`.
    -   `[ ]` Create a `.env.example` file in the `./frontend` directory, listing variables like `NEXT_PUBLIC_API_URL`.
    -   `[ ]` Create `.env`, `.env.development`, `.env.production` files in the root for FastAPI/Docker/Next.js local development, development-specific settings, and production-specific settings respectively.
-   **Backend Application Setup**
    -   `[ ]` Create a `Dockerfile` inside the `./backend` directory.
    -   `[ ]` Create a `pyproject.toml` file in `./backend` and configure it for `uv` and `poetry` (if applicable).
    -   `[ ]` Create a `requirements.txt` file in `./backend` and add `fastapi`, `uvicorn`, `psycopg2-binary`, `SQLAlchemy`, `passlib[bcrypt]`, `python-jose[cryptography]`, `python-multipart`, `python-dotenv`, `alembic`, `pydantic`, `pydantic-settings`.
    -   `[ ]` Create a basic FastAPI application in `./backend/app/main.py` with a single "/" health check endpoint.
-   **Frontend Application Setup**
    -   `[ ]` Create a `Dockerfile` inside the `./frontend` directory for the Next.js app.
    -   `[ ]` Run `npx create-next-app@latest ./frontend --ts --eslint --tailwind --app --src-dir --use-pnpm --import-alias "@/*"` to initialize the Next.js project with TypeScript, ESLint, Tailwind CSS, App Router, `src` directory, pnpm, and `@/*` import alias.
    -   `[ ]` Create `package.json`, `next.config.ts`, `tailwind.config.js`, `.env.example`, `postcss.config.mjs`, `README.md`, `tsconfig.json`, `eslint.config.mjs`, `pnpm-lock.yaml` in the `./frontend` directory.

---

## Phase 2: Backend Development (FastAPI) 🐍

This phase builds the entire backend API, from establishing a robust database connection to defining every endpoint and security measure.

### **Part 2.1: Core Configuration & Database Setup**

-   **Project Configuration**
    -   `[ ]` Create a `core` directory within the `app` folder.
    -   `[ ]` Inside `core`, create a `config.py` file to manage settings.
    -   `[ ]` In `config.py`, define a `Settings` class (using Pydantic) to load environment variables like `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `REDIS_URL`, `NEXT_PUBLIC_API_URL`.
-   **Database Connection & Session Management**
    -   `[ ]` Create a `db` directory within the `app` folder.
    -   `[ ]` Inside `db`, create a `session.py` file.
    -   `[ ]` In `session.py`, use the `DATABASE_URL` from your settings to create the SQLAlchemy `engine`.
    -   `[ ]` In `session.py`, define the `SessionLocal` factory for creating database sessions.
    -   `[ ]` In `session.py`, create the `Base` class using `declarative_base()` that all your models will inherit from.
-   **Database Dependency & Initialization**
    -   `[ ]` Inside the `db` directory, create a `dependencies.py` file.
    -   `[ ]` In `db/dependencies.py`, define the `get_db` dependency function that yields a database session for each API request.
    -   `[ ]` Inside the `db` directory, create an `init_db.py` script. This script will contain a function to create all tables in the database by importing the `Base` and all defined models.
    -   `[ ]` Implement Alembic for database migrations.

### **Part 2.2: Data Models & Schemas**

-   **Folder**
    -   `[ ]` Create a `models` directory and a `schemas` directory within the `app` folder.
-   **User Model & Schemas**
    -   `[ ]` In `models/user.py`, define the `User` SQLAlchemy model with columns for `id`, `username`, `email`, `hashed_password`, and `created_at`, and establish the many-to-many relationship with the `Role` model via the `user_roles` table.
    -   `[ ]` In `schemas/user.py`, define the Pydantic schemas: `UserCreate`, `UserUpdate`, `UserInDB`, `Token`, `TokenData`.
-   **Post Model & Schemas**
    -   `[ ]` In `models/post.py`, define the `Article` SQLAlchemy model with columns for `id`, `author_id`, `category_id`, `slug`, `title`, `content`, `is_published`, `created_at`, and `updated_at`.
    -   `[ ]` In `schemas/post.py`, define the Pydantic schemas: `ArticleCreate`, `ArticleUpdate`, `ArticleInDB`.
-   **Taxonomy & Comment Models & Schemas**
    -   `[ ]` In `models/comment.py`, define the `Comment` SQLAlchemy model.
    -   `[ ]` In `models/taxonomy.py`, define the `Category` and `Tag` SQLAlchemy models, along with the necessary join tables.
    -   `[ ]` Create corresponding Pydantic schemas for comments, categories, and tags in the `schemas` directory.
-   **Statistics Model & Schemas**
    -   `[ ]` In `models/stats.py`, define a `PageView` SQLAlchemy model with columns for `id`, `article_id` (foreign key to articles), and `timestamp`. This will allow for tracking views over time.
    -   `[ ]` In `schemas/stats.py`, define Pydantic schemas for returning analytics data, such as `SiteSummary` and `TopPost`.
-   **Role Model & Schemas**
    -   `[ ]` In `models/role.py`, define the `Role` SQLAlchemy model with columns for `id` and `name`.
    -   `[ ]` In `schemas/role.py`, define the Pydantic schemas for roles.

---

### **Part 2.4: API Endpoint Routers**

-   **Authentication Router**
    -   `[ ]` In `api/endpoints`, create an `auth.py` file with its own APIRouter.
    -   `[ ]` Define the `POST` route for user registration (`/auth/register`).
    -   `[ ]` Define the `POST` route for user login (`/auth/token`), returning a JWT.
    -   `[ ]` Define the `POST` routes for password reset requests (`/password/forgot`) and password reset confirmation (`/password/reset`).
-   **Users Router**
    -   `[ ]` In `api/endpoints`, create a `users.py` file with its own APIRouter.
    -   `[ ]` Define `GET` route for current user's profile (`/users/me`), protected by authentication.
    -   `[ ]` Define `PUT` route for updating current user's profile (`/users/me`), protected by authentication.
    -   `[ ]` Define `GET` route for a public user profile (`/users/{username}`).
-   **Articles Router**
    -   `[ ]` In `api/endpoints`, create a `articles.py` file with its own APIRouter.
    -   `[ ]` Define the public `GET` routes to list all published articles.
    -   `[ ]` Define the public `GET` route for a single article (`/articles/{slug}`).
    -   `[ ]` **Inside the single article route, add logic to create a new `PageView` record for that article to log the view.**
    -   `[ ]` Define the `POST`, `PUT`, and `DELETE` routes for creating and managing articles, protecting them with the writer-role dependency.
-   **Comments Router**
    -   `[ ]` In `api/endpoints`, create a `comments.py` file with its own APIRouter.
    -   `[ ]` Define the `POST` route for creating a comment, protected by a general logged-in user dependency.
    -   `[ ]` Define the `DELETE` route for a comment, ensuring it checks for comment ownership or admin privileges.
    -   `[ ]` Define the `PUT` route for modifying a comment, ensuring it checks for comment ownership privileges.
-   **Taxonomy Router**
    -   `[ ]` In `api/endpoints`, create a `taxonomy.py` file with its own APIRouter.
    -   `[ ]` Define `GET` routes for listing categories and tags.
    -   `[ ]` Define `POST`, `PUT`, `DELETE` routes for managing categories and tags, protected by admin-role dependency.
-   **Admin Router**
    -   `[ ]` In `api/endpoints`, create an `admin.py` file with its own APIRouter.
    -   `[ ]` Define all endpoints for managing users, categories, and tags within this router. Protect every endpoint with the `get_current_admin_user` dependency.
    -   `[ ]` **Create a `GET` endpoint for site summary stats (`/admin/stats/summary`)**. This will query the database for total user, article, and comment counts.
    -   `[ ]` **Create a `GET` endpoint for top articles (`/admin/stats/top-articles`)**. This will aggregate data from the `pageviews` table to find the most viewed articles.
    -   `[ ]` **Create a `GET` endpoint for views over time (`/admin/stats/views-over-time`)**. This will query the `pageviews` table to return time-series data suitable for a chart.
-   **Main Application Assembly**
    -   `[ ]` In `app/main.py`, import all the routers (auth, users, articles, comments, taxonomy, admin).
    -   `[ ]` In `app/main.py`, include each router into the main FastAPI app instance.
    -   `[ ]` In `app/main.py`, configure CORS settings.

---

## Phase 3: Frontend Development & Feature Implementation ⚛️

This unified phase covers the entire frontend build, from initial setup to the creation and integration of all pages and their specific components, feature by feature.

### **Part 3.1: Frontend Foundation & Global Setup**

-   **Styling & Global Layout**
    -   `[ ]` Set up Tailwind CSS within the Next.js project.
    -   `[ ]` Configure `tailwind.config.js` with the custom color palette : Based on your themes of plants, wood, mountains, and steampunk, here is a proposed eye-friendly, modern color scheme :
        -   `[ ]` Background: #24282B (Dark Charcoal) - A deep, dark base that's easy on the eyes.
        -   `[ ]` Text: #E8E2D9 (Alabaster) - A soft, off-white for high readability without harsh contrast.
        -   `[ ]` Primary (Wood & Earth): #5C3D2E (Deep Coffee) - For major UI components like footers or sidebars.
        -   `[ ]` Secondary (Plants): #364B44 (Brunswick Green) - For secondary elements and accents.
        -   `[ ]` Accent (Steampunk Brass): #C8A870 (Antique Brass) - For critical interactive elements like buttons and links to draw user attention.
    -   `[ ]` Build a responsive `Navbar` component.
    -   `[ ]` Build a `Footer` component.
    -   `[ ]` Create a main `Layout` component that wraps page content with the `Navbar` and `Footer`.
-   **Global State & API Services**
    -   `[ ]` Set up a global state management solution (e.g., React Context) for user authentication state.
    -   `[ ]` Create a typed API client or a set of service functions in a `/lib` directory to handle all calls to the FastAPI backend.

### **Part 3.2: Public Pages & Components**

-   **Home / Landing Page**
    -   `[ ]` Create the page file `pages/index.tsx`.
    -   `[ ]` Implement `getServerSideProps` to fetch the latest articles.
    -   `[ ]` Build a `ArticleCard` component to display a single article preview (title, author, image, excerpt).
    -   `[ ]` Build a `FeaturedArticlesGrid` component that maps over the fetched data and uses the `ArticleCard` component.
    -   `[ ]` Build a `SearchBar` component (UI only).
    -   `[ ]` Build a `CategoriesList` component that links to category pages.
-   **Article Listing Page**
    -   `[ ]` Create the page file `pages/blog/index.tsx`.
    -   `[ ]` Implement `getServerSideProps` for paginated article fetching.
    -   `[ ]` Build a `FilterControls` component with dropdowns for categories and tags.
    -   `[ ]` Build a `Pagination` component for page navigation.
    -   `[ ]` Assemble the page using the `FilterControls`, `ArticleCard` grid, and `Pagination` components.
-   **Article Detail Page**
    -   `[ ]` Create the dynamic page file `pages/blog/[slug].tsx`.
    -   `[ ]` Implement `getServerSideProps` to fetch the single article, its author, and comments.
    -   `[ ]` Build an `ArticleHeader` component (title, author link, date).
    -   `[ ]` Build an `ArticleBody` component to render the article's content.
    -   `[ ]` Build a `Comment` component to display a single comment.
    -   `[ ]` Build a `CommentThread` component that maps and displays a list of `Comment` components.
    -   `[ ]` Build a `CommentForm` component, which is visibly disabled or hidden for non-logged-in users.
    -   `[ ]` Use the `Head` component to set dynamic SEO metadata.
-   **Author Profile Page**
    -   `[ ]` Create the dynamic page file `pages/author/[id].tsx`.
    -   `[ ]` Implement `getServerSideProps` to fetch the author's data and their articles.
    -   `[ ]` Build an `AuthorBio` component.
    -   `[ ]` Assemble the page using the `AuthorBio` and a grid of `ArticleCard` components.
-   **Static Pages**
    -   `[ ]` Create the `pages/about.tsx`, `pages/contact.tsx`, `pages/terms.tsx`, and `pages/privacy.tsx` pages with static content.

---

### **Part 3.3: Authentication Pages & Components**

-   **Login & Register Pages**
    -   `[ ]` Build a reusable `InputField` component.
    -   `[ ]` Build a reusable `Button` component based on the style guide.
    -   `[ ]` Create the `pages/login.tsx` page, assembling the form with `InputField` and `Button` components.
    -   `[ ]` Implement the login `onSubmit` handler to call the API service.
    -   `[ ]` Create the `pages/register.tsx` page and form.
-   **Forgot/Reset Password Pages**
    -   `[ ]` Create the `pages/forgot-password.tsx` page and its associated form.
    -   `[ ]` Create the dynamic `pages/reset-password/[token].tsx` page and its associated form.

---

### **Part 3.4: Writer Pages & Components (Role-Protected)**

-   **Writer Dashboard**
    -   `[ ]` Create a `withAuth` Higher-Order Component (HOC) or use a similar pattern to protect pages based on user role.
    -   `[ ]` Create the protected page `pages/writer/dashboard.tsx`.
    -   `[ ]` Build a `DashboardStatCard` component.
    -   `[ ]` Build a `WriterArticleTable` component to list drafts and published articles with action buttons.
    -   `[ ]` Assemble the dashboard using these components.
-   **Create/Edit Article Page**
    -   `[ ]` Create the protected page `pages/writer/editor/[id].tsx`.
    -   `[ ]` Build or integrate a rich text `Editor` component.
    -   `[ ]` Build a `CategoryTagSelector` component for associating taxonomies.
    -   `[ ]` Build an `ImageUpload` component.
    -   `[ ]` Assemble the editor page and implement the save/publish logic.

---

### **Part 3.5: Admin Pages & Components (Role-Protected)**

-   **Admin Dashboard & Management Pages**
    -   `[ ]` Build a generic, reusable `DataTable` component with features for sorting, filtering, and actions.
    -   `[ ]` Build a `Chart` component by wrapping a library like Recharts.
    -   `[ ]` Create the protected admin pages (`/admin/dashboard`, `/admin/articles`, `/admin/users`, etc.).
    -   `[ ]` On each management page, configure the `DataTable` component to display the appropriate data (users, articles, etc.) and handle the specific actions (delete, change role).
-   **Site Settings Page**
    -   `[ ]` Create the protected page `pages/admin/settings.tsx`.
    -   `[ ]` Build a `SettingsForm` component to manage site-wide configuration.

---

### **Part 3.6: Shared Pages & Components**

-   **Profile Settings Page**
    -   `[ ]` Create the protected page `pages/profile.tsx`.
    -   `[ ]` Build an `UpdateProfileForm` component.
    -   `[ ]` Build a `ChangePasswordForm` component.
-   **Error & Notification Components**
    -   `[ ]` Create a custom `pages/404.tsx` page.
    -   `[ ]` Build a `Toast` or `Notification` component to provide user feedback after actions.
    -   `[ ]` Integrate the `Notification` component into the main `Layout`.

---

### **Authentication Pages**

-   **Login Page (`/login`)**
    -   `[ ]` In `pages/login.tsx`, build the login form UI.
    -   `[ ]` Implement the `onSubmit` handler to call the `/auth/token` API endpoint.
    -   `[ ]` On success, store the JWT and redirect the user.
    -   `[ ]` Display error messages from the API on failure.
-   **Register Page (`/register`)**
    -   `[ ]` In `pages/register.tsx`, build the registration form UI.
    -   `[ ]` Implement the `onSubmit` handler to call the `/auth/register` API endpoint.
    -   `[ ]` On success, redirect the user to the login page with a success message.
-   **Forgot/Reset Password**
    -   `[ ]` **Backend Task:** Create `/password/forgot` and `/password/reset` endpoints in FastAPI.
    -   `[ ]` Create the `pages/forgot-password.tsx` page with a form to submit an email.
    -   `[ ]` Create the dynamic page `pages/reset-password/[token].tsx` with a form to enter a new password.

---

### **Writer Pages (Role-Protected)**

-   **Writer Dashboard (`/writer/dashboard`)**
    -   `[ ]` Create the protected page `pages/writer/dashboard.tsx`.
    -   `[ ]` Implement `getServerSideProps` with authentication checks to fetch data for the current writer.
    -   `[ ]` Build a `QuickStats` component to show views and comments on the writer's articles.
    -   `[ ]` Build two list components: `MyDraftsList` and `MyPublishedList`, showing the writer's articles.
-   **Create/Edit Article Page (`/writer/editor/[id]`)**
    -   `[ ]` Create the protected dynamic page `pages/writer/editor/[id].tsx`.
    -   `[ ]` Build the main editor form, including fields for title and slug.
    -   `[ ]` Integrate a rich text editor component (e.g., TipTap).
    -   `[ ]` Build a `CategoryTagSelector` component to associate taxonomies with the article.
    -   `[ ]` Build an `ImageUpload` component.
    -   `[ ]` Implement the "Save Draft" and "Publish" actions to call the correct backend endpoints.
    -   `[ ]` If an `id` is present, fetch the existing article data to populate the editor form.

---

### **Admin Pages (Role-Protected)**

-   **Admin Dashboard (`/admin/dashboard`)**
    -   `[ ]` Create the protected page `pages/admin/dashboard.tsx`.
    -   `[ ]` Fetch and display `SiteHealth` stats (total articles, users, etc.).
    -   `[ ]` Build a `SiteAnalytics` component using a chart library to show pageviews over time.
    -   `[ ]` Build `TopArticles` and `RecentActivity` list components.
-   **Article Management (`/admin/articles`)**
    -   `[ ]` Create the protected page `pages/admin/articles.tsx`.
    -   `[ ]` Build a data table component to display all articles from all authors.
    -   `[ ]` Implement functionality for searching, filtering, and performing bulk actions (publish, unpublish, delete).
-   **Comment Management (`/admin/comments`)**
    -   `[ ]` Create the protected page `pages/admin/comments.tsx`.
    -   `[ ]` Build a data table to display all comments with actions to approve or delete.
-   **User Management (`/admin/users`)**
    -   `[ ]` Create the protected page `pages/admin/users.tsx`.
    -   `[ ]` Build a data table to display all users with actions to edit their profile or change their role.
-   **Site Settings (`/admin/settings`)**
    -   `[ ]` Create the protected page `pages/admin/settings.tsx`.
    -   `[ ]` Build forms to update site-wide settings like the site name, logo, and SEO defaults.

---

### **Shared / Miscellaneous Pages & Components**

-   **Profile Settings (`/profile`)**
    -   `[ ]` Create the protected page `pages/profile.tsx` for all logged-in users.
    -   `[ ]` Build a form for users to update their email, username, and password.
    -   `[ ]` Build an avatar upload component.
-   **Error Pages**
    -   `[ ]` Create a custom `pages/404.tsx` page for "Not Found" errors.
    -   `[ ]` Create a generic `pages/error.tsx` page or component to handle other errors (like 403 Forbidden).
-   **Notification System**
    -   `[ ]` Build a `Notification` or `Toast` component.
    -   `[ ]` Integrate it into the global layout to display success or error messages from API calls.

---

## Phase 5: Testing & Quality Assurance 🧪

This phase ensures the application is stable and secure.

-   `[ ]` Write unit tests for critical backend utility functions (e.g., token creation).
-   `[ ]` Write integration tests for key API endpoints (login, post creation).
-   `[ ]` Write unit tests for complex frontend components.
-   `[ ]` Perform manual E2E testing for the main user flows:
    -   `[ ]` User registration and login.
    -   `[ ]` A writer creating and publishing a post.
    -   `[ ]` A reader posting a comment.
    -   `[ ]` An admin changing a user's role.
-   `[ ]` Manually test responsive design on different screen sizes.
-   `[ ]` Verify SSR is working by viewing the page source of a blog post.

---

## Phase 6: Deployment & Production 🚀

This phase moves the application to a live server.

-   `[ ]` Choose a cloud provider (e.g., DigitalOcean, AWS).
-   `[ ]` Set up a production server/instance.
-   `[ ]` Install Docker and Docker Compose on the server.
-   `[ ]` Configure a domain name to point to the server's IP address.
-   `[ ]` Create production environment files (`.env.production`) for backend and frontend with real database credentials and secrets.
-   `[ ]` Set up a reverse proxy (e.g., Nginx) to handle incoming traffic and route to the correct container.
-   `[ ]` Configure Nginx to serve the Next.js frontend and proxy API requests to the FastAPI backend.
-   `[ ]` Install an SSL certificate using Let's Encrypt for HTTPS.
-   `[ ]` Pull the final code, build the production Docker images, and launch the application using `compose -f compose.yaml -f compose.production.yaml up -d --build`.
-   `[ ]` Manually create the first `admin` user in the production database.
-   `[ ]` Submit the sitemap to Google Search Console.

### Phase 7: Documentation Updates & Gap Resolution 📝

#### New Tasks Identified from project_description.md:

-   `[ ]` Implement image upload endpoint in backend/articles.py (project_description.md:171-174)
-   `[ ]` Add refresh token rotation mechanism to security.py (project_description.md:373)
-   `[ ]` Create PageView record in article GET endpoint (project_description.md:142-143)
-   `[ ]` Implement JSON-LD structured data in ArticleBody component (project_description.md:256)

#### New Tasks Identified from project_pages.md:

-   `[ ]` Build AuditLog component for admin dashboard (project_pages.md:53)
-   `[ ]` Create notifications center page with message list (project_pages.md:60)
-   `[ ]` Add comment moderation UI to writer dashboard (project_pages.md:33)

#### Structural Updates from project_structure.md:

-   `[ ]` Implement init_db.py population script (project_structure.md:28)
-   `[ ]` Add alembic migration generation task to Phase 2.1 (project_structure.md:102)
-   `[ ]` Complete api.ts client with all endpoint methods (project_structure.md:64)
