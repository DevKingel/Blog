## Phase 1: Project Setup & Foundation 🏗️

This phase creates the skeleton of your project, including architectural planning, directory structures, and Docker configuration.

* **Project Architecture & Planning**
    * `[ ]` Create a `SITEMAP.md` file in the root directory. This file should outline the application's structure to guide development. It must include:
        * **Public Pages:** Homepage (`/`), Blog Post (`/blog/[slug]`), Category View (`/category/[slug]`), Tag View (`/tag/[slug]`), Login (`/login`), Register (`/register`).
        * **Authenticated Pages:** User Profile (`/profile`).
        * **Writer Pages:** Writer Dashboard (`/writer/dashboard`), Post Editor (`/writer/editor/[id]`).
        * **Admin Pages:** Admin Dashboard (`/admin/dashboard`), User Management (`/admin/users`), Content Management (`/admin/content`), Taxonomy Management (`/admin/categories`).
        * **Key Components:** `Navbar`, `Footer`, `PostCard`, `CommentList`, `CommentForm`.
* **Project Initialization**
    * `[ ]` Create a root project directory.
    * `[ ]` Initialize a `git` repository in the root directory.
    * `[ ]` Create a `.gitignore` file with appropriate entries for Python, Node.js, and OS-specific files.
    * `[ ]` Create a main `README.md` file with the project title.
* **Initial File Structure**
    * `[ ]` Create the `./backend` directory.
    * `[ ]` Inside `./backend`, create an `app` directory.
    * `[ ]` Inside `./backend/app`, create `__init__.py`, `main.py`, and sub-directories: `api`, `core`, `db`, `models`, `schemas`.
    * `[ ]` Create the `./frontend` directory.
    * `[ ]` Inside `./frontend`, create standard Next.js directories: `components`, `pages`, `styles`, `lib`.
* **Docker Configuration**
    * `[ ]` Create a base `compose.yaml` file in the root.
    * `[ ]` Define the `backend`, `frontend`, `db`, and `cache` services in `compose.yaml` without development-specific settings like ports or volumes.
    * `[ ]` Configure a named volume in `compose.yaml` for PostgreSQL data persistence.
    * `[ ]` Create a `compose.override.yaml` file. This file will automatically be used by Docker Compose in development.
    * `[ ]` In `compose.override.yaml`, add development configurations: map local source code (`./backend:/app`, `./frontend:/app`) into the containers and expose ports (`8000:8000`, `3000:3000`).
    * `[ ]` Create a `compose.production.yaml` file for production-specific settings.
    * `[ ]` In `compose.production.yaml`, configure services to use production environment files and not mount local source code.
    * `[ ]` Create a `.env.example` file in the `./backend` directory, listing variables like `DATABASE_URL` and `SECRET_KEY`.
    * `[ ]` Create a `.env.example` file in the `./frontend` directory, listing variables like `NEXT_PUBLIC_API_URL`.
* **Backend Application Setup**
    * `[ ]` Create a `Dockerfile` inside the `./backend` directory.
    * `[ ]` Create a `requirements.txt` file in `./backend` and add `fastapi`, `uvicorn`, `psycopg2-binary`, `SQLAlchemy`, `passlib[bcrypt]`, `python-jose[cryptography]`, and `python-multipart`.
    * `[ ]` Create a basic FastAPI application in `./backend/app/main.py` with a single "/" health check endpoint.
* **Frontend Application Setup**
    * `[ ]` Create a `Dockerfile` inside the `./frontend` directory for the Next.js app.
    * `[ ]` Run `npx create-next-app@latest ./frontend` to initialize the Next.js project.

---

## Phase 2: Backend Development (FastAPI) 🐍

This phase builds the entire backend API, from establishing a robust database connection to defining every endpoint and security measure.

### **Part 2.1: Core Configuration & Database Setup**

* **Project Configuration**
    * `[ ]` Create a `core` directory within the `app` folder.
    * `[ ]` Inside `core`, create a `config.py` file to manage settings.
    * `[ ]` In `config.py`, define a `Settings` class (using Pydantic) to load environment variables like `DATABASE_URL`, `SECRET_KEY`, and `ALGORITHM`.
* **Database Connection & Session Management**
    * `[ ]` Create a `db` directory within the `app` folder.
    * `[ ]` Inside `db`, create a `session.py` file.
    * `[ ]` In `session.py`, use the `DATABASE_URL` from your settings to create the SQLAlchemy `engine`.
    * `[ ]` In `session.py`, define the `SessionLocal` factory for creating database sessions.
    * `[ ]` In `session.py`, create the `Base` class using `declarative_base()` that all your models will inherit from.
* **Database Dependency & Initialization**
    * `[ ]` Inside the `db` directory, create a `dependencies.py` file.
    * `[ ]` In `db/dependencies.py`, define the `get_db` dependency function that yields a database session for each API request.
    * `[ ]` Inside the `db` directory, create an `init_db.py` script. This script will contain a function to create all tables in the database by importing the `Base` and all defined models.

### **Part 2.2: Data Models & Schemas**

* **User Model & Schemas**
    * `[ ]` Create a `models` directory and a `schemas` directory within the `app` folder.
    * `[ ]` In `models/user.py`, define the `User` SQLAlchemy model with columns for `id`, `email`, `hashed_password`, and `role`.
    * `[ ]` In `schemas/user.py`, define the Pydantic schemas: `UserCreate`, `UserUpdate`, and `UserInDB`.
* **Post Model & Schemas**
    * `[ ]` In `models/post.py`, define the `Post` SQLAlchemy model with columns for `title`, `slug`, `content`, `status`, `author_id`, etc.
    * `[ ]` In `schemas/post.py`, define the Pydantic schemas: `PostCreate`, `PostUpdate`, and `PostInDB`.
* **Taxonomy & Comment Models & Schemas**
    * `[ ]` In `models/comment.py`, define the `Comment` SQLAlchemy model.
    * `[ ]` In `models/taxonomy.py`, define the `Category` and `Tag` SQLAlchemy models, along with the necessary join tables.
    * `[ ]` Create corresponding Pydantic schemas for comments, categories, and tags in the `schemas` directory.
* **Statistics Model & Schemas**
    * `[ ]` In `models/stats.py`, define a `PageView` SQLAlchemy model with columns for `id`, `post_id` (foreign key to posts), and `timestamp`. This will allow for tracking views over time.
    * `[ ]` In `schemas/stats.py`, define Pydantic schemas for returning analytics data, such as `SiteSummary` and `TopPost`.

---

### **Part 2.4: API Endpoint Routers**

* **Posts Router**
    * `[ ]` In `api/endpoints`, create a `posts.py` file with its own APIRouter.
    * `[ ]` Define the public `GET` routes to list all published posts.
    * `[ ]` Define the public `GET` route for a single post (`/posts/{slug}`).
    * `[ ]` **Inside the single post route, add logic to create a new `PageView` record for that post to log the view.**
    * `[ ]` Define the `POST`, `PUT`, and `DELETE` routes for creating and managing posts, protecting them with the writer-role dependency.
* **Comments Router**
    * `[ ]` In `api/endpoints`, create a `comments.py` file with its own APIRouter.
    * `[ ]` Define the `POST` route for creating a comment, protected by a general logged-in user dependency.
    * `[ ]` Define the `DELETE` route for a comment, ensuring it checks for comment ownership or admin privileges.
* **Admin Router**
    * `[ ]` In `api/endpoints`, create an `admin.py` file with its own APIRouter.
    * `[ ]` Define all endpoints for managing users, categories, and tags within this router. Protect every endpoint with the `get_current_admin_user` dependency.
    * `[ ]` **Create a `GET` endpoint for site summary stats (`/admin/stats/summary`)**. This will query the database for total user, post, and comment counts.
    * `[ ]` **Create a `GET` endpoint for top posts (`/admin/stats/top-posts`)**. This will aggregate data from the `pageviews` table to find the most viewed articles.
    * `[ ]` **Create a `GET` endpoint for views over time (`/admin/stats/views-over-time`)**. This will query the `pageviews` table to return time-series data suitable for a chart.
* **Main Application Assembly**
    * `[ ]` In `app/main.py`, import all the routers (auth, posts, comments, admin).
    * `[ ]` In `app/main.py`, include each router into the main FastAPI app instance.

---

## Phase 3: Frontend Development & Feature Implementation ⚛️

This unified phase covers the entire frontend build, from initial setup to the creation and integration of all pages and their specific components, feature by feature.

### **Part 3.1: Frontend Foundation & Global Setup**

* **Styling & Global Layout**
    * `[ ]` Set up Tailwind CSS within the Next.js project.
    * `[ ]` Configure `tailwind.config.js` with the custom color palette (`#24282B`, `#E8E2D9`, `#5C3D2E`, etc.).
    * `[ ]` Build a responsive `Navbar` component.
    * `[ ]` Build a `Footer` component.
    * `[ ]` Create a main `Layout` component that wraps page content with the `Navbar` and `Footer`.
* **Global State & API Services**
    * `[ ]` Set up a global state management solution (e.g., React Context) for user authentication state.
    * `[ ]` Create a typed API client or a set of service functions in a `/lib` directory to handle all calls to the FastAPI backend.

### **Part 3.2: Public Pages & Components**

* **Home / Landing Page**
    * `[ ]` Create the page file `pages/index.tsx`.
    * `[ ]` Implement `getServerSideProps` to fetch the latest posts.
    * `[ ]` Build a `PostCard` component to display a single post preview (title, author, image, excerpt).
    * `[ ]` Build a `FeaturedPostsGrid` component that maps over the fetched data and uses the `PostCard` component.
    * `[ ]` Build a `SearchBar` component (UI only).
    * `[ ]` Build a `CategoriesList` component that links to category pages.
* **Article Listing Page**
    * `[ ]` Create the page file `pages/blog/index.tsx`.
    * `[ ]` Implement `getServerSideProps` for paginated article fetching.
    * `[ ]` Build a `FilterControls` component with dropdowns for categories and tags.
    * `[ ]` Build a `Pagination` component for page navigation.
    * `[ ]` Assemble the page using the `FilterControls`, `PostCard` grid, and `Pagination` components.
* **Article Detail Page**
    * `[ ]` Create the dynamic page file `pages/blog/[slug].tsx`.
    * `[ ]` Implement `getServerSideProps` to fetch the single post, its author, and comments.
    * `[ ]` Build an `ArticleHeader` component (title, author link, date).
    * `[ ]` Build an `ArticleBody` component to render the post's content.
    * `[ ]` Build a `Comment` component to display a single comment.
    * `[ ]` Build a `CommentThread` component that maps and displays a list of `Comment` components.
    * `[ ]` Build a `CommentForm` component, which is visibly disabled or hidden for non-logged-in users.
    * `[ ]` Use the `Head` component to set dynamic SEO metadata.
* **Author Profile Page**
    * `[ ]` Create the dynamic page file `pages/author/[id].tsx`.
    * `[ ]` Implement `getServerSideProps` to fetch the author's data and their posts.
    * `[ ]` Build an `AuthorBio` component.
    * `[ ]` Assemble the page using the `AuthorBio` and a grid of `PostCard` components.
* **Static Pages**
    * `[ ]` Create the `pages/about.tsx`, `pages/contact.tsx`, `pages/terms.tsx`, and `pages/privacy.tsx` pages with static content.

---

### **Part 3.3: Authentication Pages & Components**

* **Login & Register Pages**
    * `[ ]` Build a reusable `InputField` component.
    * `[ ]` Build a reusable `Button` component based on the style guide.
    * `[ ]` Create the `pages/login.tsx` page, assembling the form with `InputField` and `Button` components.
    * `[ ]` Implement the login `onSubmit` handler to call the API service.
    * `[ ]` Create the `pages/register.tsx` page and form.
* **Forgot/Reset Password Pages**
    * `[ ]` Create the `pages/forgot-password.tsx` page and its associated form.
    * `[ ]` Create the dynamic `pages/reset-password/[token].tsx` page and its associated form.

---

### **Part 3.4: Writer Pages & Components (Role-Protected)**

* **Writer Dashboard**
    * `[ ]` Create a `withAuth` Higher-Order Component (HOC) or use a similar pattern to protect pages based on user role.
    * `[ ]` Create the protected page `pages/writer/dashboard.tsx`.
    * `[ ]` Build a `DashboardStatCard` component.
    * `[ ]` Build a `WriterPostTable` component to list drafts and published posts with action buttons.
    * `[ ]` Assemble the dashboard using these components.
* **Create/Edit Post Page**
    * `[ ]` Create the protected page `pages/writer/editor/[id].tsx`.
    * `[ ]` Build or integrate a rich text `Editor` component.
    * `[ ]` Build a `CategoryTagSelector` component for associating taxonomies.
    * `[ ]` Build an `ImageUpload` component.
    * `[ ]` Assemble the editor page and implement the save/publish logic.

---

### **Part 3.5: Admin Pages & Components (Role-Protected)**

* **Admin Dashboard & Management Pages**
    * `[ ]` Build a generic, reusable `DataTable` component with features for sorting, filtering, and actions.
    * `[ ]` Build a `Chart` component by wrapping a library like Recharts.
    * `[ ]` Create the protected admin pages (`/admin/dashboard`, `/admin/articles`, `/admin/users`, etc.).
    * `[ ]` On each management page, configure the `DataTable` component to display the appropriate data (users, posts, etc.) and handle the specific actions (delete, change role).
* **Site Settings Page**
    * `[ ]` Create the protected page `pages/admin/settings.tsx`.
    * `[ ]` Build a `SettingsForm` component to manage site-wide configuration.

---

### **Part 3.6: Shared Pages & Components**

* **Profile Settings Page**
    * `[ ]` Create the protected page `pages/profile.tsx`.
    * `[ ]` Build an `UpdateProfileForm` component.
    * `[ ]` Build a `ChangePasswordForm` component.
* **Error & Notification Components**
    * `[ ]` Create a custom `pages/404.tsx` page.
    * `[ ]` Build a `Toast` or `Notification` component to provide user feedback after actions.
    * `[ ]` Integrate the `Notification` component into the main `Layout`.

---

### **Authentication Pages**

* **Login Page (`/login`)**
    * `[ ]` In `pages/login.tsx`, build the login form UI.
    * `[ ]` Implement the `onSubmit` handler to call the `/auth/token` API endpoint.
    * `[ ]` On success, store the JWT and redirect the user.
    * `[ ]` Display error messages from the API on failure.
* **Register Page (`/register`)**
    * `[ ]` In `pages/register.tsx`, build the registration form UI.
    * `[ ]` Implement the `onSubmit` handler to call the `/auth/register` API endpoint.
    * `[ ]` On success, redirect the user to the login page with a success message.
* **Forgot/Reset Password**
    * `[ ]` **Backend Task:** Create `/password/forgot` and `/password/reset` endpoints in FastAPI.
    * `[ ]` Create the `pages/forgot-password.tsx` page with a form to submit an email.
    * `[ ]` Create the dynamic page `pages/reset-password/[token].tsx` with a form to enter a new password.

---

### **Writer Pages (Role-Protected)**

* **Writer Dashboard (`/writer/dashboard`)**
    * `[ ]` Create the protected page `pages/writer/dashboard.tsx`.
    * `[ ]` Implement `getServerSideProps` with authentication checks to fetch data for the current writer.
    * `[ ]` Build a `QuickStats` component to show views and comments on the writer's posts.
    * `[ ]` Build two list components: `MyDraftsList` and `MyPublishedList`, showing the writer's posts.
* **Create/Edit Post Page (`/writer/editor/[id]`)**
    * `[ ]` Create the protected dynamic page `pages/writer/editor/[id].tsx`.
    * `[ ]` Build the main editor form, including fields for title and slug.
    * `[ ]` Integrate a rich text editor component (e.g., TipTap).
    * `[ ]` Build a `CategoryTagSelector` component to associate taxonomies with the post.
    * `[ ]` Build an `ImageUpload` component.
    * `[ ]` Implement the "Save Draft" and "Publish" actions to call the correct backend endpoints.
    * `[ ]` If an `id` is present, fetch the existing post data to populate the editor form.

---

### **Admin Pages (Role-Protected)**

* **Admin Dashboard (`/admin/dashboard`)**
    * `[ ]` Create the protected page `pages/admin/dashboard.tsx`.
    * `[ ]` Fetch and display `SiteHealth` stats (total posts, users, etc.).
    * `[ ]` Build a `SiteAnalytics` component using a chart library to show pageviews over time.
    * `[ ]` Build `TopPosts` and `RecentActivity` list components.
* **Article Management (`/admin/articles`)**
    * `[ ]` Create the protected page `pages/admin/articles.tsx`.
    * `[ ]` Build a data table component to display all posts from all authors.
    * `[ ]` Implement functionality for searching, filtering, and performing bulk actions (publish, unpublish, delete).
* **Comment Management (`/admin/comments`)**
    * `[ ]` Create the protected page `pages/admin/comments.tsx`.
    * `[ ]` Build a data table to display all comments with actions to approve or delete.
* **User Management (`/admin/users`)**
    * `[ ]` Create the protected page `pages/admin/users.tsx`.
    * `[ ]` Build a data table to display all users with actions to edit their profile or change their role.
* **Site Settings (`/admin/settings`)**
    * `[ ]` Create the protected page `pages/admin/settings.tsx`.
    * `[ ]` Build forms to update site-wide settings like the site name, logo, and SEO defaults.

---

### **Shared / Miscellaneous Pages & Components**

* **Profile Settings (`/profile`)**
    * `[ ]` Create the protected page `pages/profile.tsx` for all logged-in users.
    * `[ ]` Build a form for users to update their email, username, and password.
    * `[ ]` Build an avatar upload component.
* **Error Pages**
    * `[ ]` Create a custom `pages/404.tsx` page for "Not Found" errors.
    * `[ ]` Create a generic `pages/error.tsx` page or component to handle other errors (like 403 Forbidden).
* **Notification System**
    * `[ ]` Build a `Notification` or `Toast` component.
    * `[ ]` Integrate it into the global layout to display success or error messages from API calls.

***

## Phase 5: Testing & Quality Assurance 🧪

This phase ensures the application is stable and secure.

* `[ ]` Write unit tests for critical backend utility functions (e.g., token creation).
* `[ ]` Write integration tests for key API endpoints (login, post creation).
* `[ ]` Write unit tests for complex frontend components.
* `[ ]` Perform manual E2E testing for the main user flows:
    * `[ ]` User registration and login.
    * `[ ]` A writer creating and publishing a post.
    * `[ ]` A reader posting a comment.
    * `[ ]` An admin changing a user's role.
* `[ ]` Manually test responsive design on different screen sizes.
* `[ ]` Verify SSR is working by viewing the page source of a blog post.

***

## Phase 6: Deployment & Production 🚀

This phase moves the application to a live server.

* `[ ]` Choose a cloud provider (e.g., DigitalOcean, AWS).
* `[ ]` Set up a production server/instance.
* `[ ]` Install Docker and Docker Compose on the server.
* `[ ]` Configure a domain name to point to the server's IP address.
* `[ ]` Create production environment files (`.env.production`) for backend and frontend with real database credentials and secrets.
* `[ ]` Set up a reverse proxy (e.g., Nginx) to handle incoming traffic and route to the correct container.
* `[ ]` Configure Nginx to serve the Next.js frontend and proxy API requests to the FastAPI backend.
* `[ ]` Install an SSL certificate using Let's Encrypt for HTTPS.
* `[ ]` Pull the final code, build the production Docker images, and launch the application using `compose -f compose.yaml -f compose.production.yaml up -d --build`.
* `[ ]` Manually create the first `admin` user in the production database.
* `[ ]` Submit the sitemap to Google Search Console.