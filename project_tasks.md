Of course. Here is a granular, step-by-step task list designed for an AI assistant to build your application from scratch to production.

***

## Phase 1: Project Setup & Foundation 🏗️

This phase creates the skeleton of your project, including the directory structure and Docker configuration.

* **Project Initialization**
    * `[ ]` Create a root project directory.
    * `[ ]` Initialize a `git` repository in the root directory.
    * `[ ]` Create a `.gitignore` file with appropriate entries for Python, Node.js, and OS-specific files.
    * `[ ]` Create a main `README.md` file with the project title.
* **Docker Configuration**
    * `[ ]` Create a `docker-compose.yml` file in the root.
    * `[ ]` Define the `backend` service in `docker-compose.yml`, pointing to a `./backend` directory.
    * `[ ]` Define the `frontend` service in `docker-compose.yml`, pointing to a `./frontend` directory.
    * `[ ]` Define the `db` service in `docker-compose.yml` using the official `postgres:15` image.
    * `[ ]` Define the `cache` service in `docker-compose.yml` using the official `redis:7` image.
    * `[ ]` Configure environment variables for the PostgreSQL service (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
    * `[ ]` Create a named volume in `docker-compose.yml` for PostgreSQL data persistence.
* **Backend Application Setup**
    * `[ ]` Create the `./backend` directory.
    * `[ ]` Create a `Dockerfile` inside the `./backend` directory.
    * `[ ]` Create a `requirements.txt` file in `./backend` and add `fastapi`, `uvicorn`, `psycopg2-binary`, `SQLAlchemy`, `passlib[bcrypt]`, `python-jose[cryptography]`, and `python-multipart`.
    * `[ ]` Create a basic FastAPI application in `./backend/app/main.py` with a single "/" health check endpoint.
* **Frontend Application Setup**
    * `[ ]` Create the `./frontend` directory.
    * `[ ]` Create a `Dockerfile` inside the `./frontend` directory for the Next.js app.
    * `[ ]` Run `npx create-next-app@latest ./frontend` to initialize the Next.js project.

***

## Phase 2: Backend Development (FastAPI) 🐍

This phase builds all the API endpoints and database logic.

* **Database & ORM Setup**
    * `[ ]` Establish the database connection logic using SQLAlchemy.
    * `[ ]` Create a base model class and session management for the database.
    * `[ ]` Create the `users` table model with columns for `id`, `email`, `hashed_password`, and `role` (using an `Enum` type for 'reader', 'writer', 'admin').
    * `[ ]` Create the `posts` table model with columns for `id`, `title`, `slug`, `content`, `status`, `author_id` (foreign key to users).
    * `[ ]` Create the `comments` table model with columns for `id`, `content`, `author_id`, and `post_id`.
    * `[ ]` Create the `categories` and `tags` table models.
    * `[ ]` Create the `post_categories` and `post_tags` join tables for many-to-many relationships.
* **User Authentication & Authorization**
    * `[ ]` Create Pydantic schemas for User creation, User display, and Token data.
    * `[ ]` Implement password hashing functions using `passlib`.
    * `[ ]` Create the `/auth/register` endpoint to register a new user (default role 'reader').
    * `[ ]` Create the `/auth/token` endpoint for user login, which returns a JWT access token.
    * `[ ]` Implement JWT token creation and decoding functions.
    * `[ ]` Create a dependency function `get_current_user` to validate the JWT and return the user model.
    * `[ ]` Create dependency functions for role checks (`is_reader`, `is_writer`, `is_admin`) based on the current user.
* **API Endpoints**
    * `[ ]` Create CRUD endpoints for `/posts` protected by the `is_writer` dependency.
    * `[ ]` Implement ownership check logic within the update/delete post endpoints.
    * `[ ]` Create public endpoints `GET /posts` and `GET /posts/{slug}` to fetch published articles.
    * `[ ]` Create CRUD endpoints for `/comments` protected by the `is_reader` dependency.
    * `[ ]` Create Admin-only CRUD endpoints for `/categories` and `/tags`.
    * `[ ]` Create Admin-only endpoints for user management (e.g., `GET /users`, `PUT /users/{user_id}/role`).
    * `[ ]` Create an Admin-only endpoint for statistics (`GET /admin/stats`).

***

## Phase 3: Frontend Development (Next.js) ⚛️

This phase builds the user interface and connects it to the backend API.

* **Styling & Layout**
    * `[ ]` Set up Tailwind CSS within the Next.js project.
    * `[ ]` Configure `tailwind.config.js` with the custom color palette (`#24282B`, `#E8E2D9`, `#5C3D2E`, etc.).
    * `[ ]` Create a main `Layout` component that includes a navbar and footer.
    * `[ ]` Build a responsive Navbar component.
    * `[ ]` Build a Footer component.
* **Pages & Routing**
    * `[ ]` Create the homepage file (`/pages/index.tsx`) to display a list of recent posts.
    * `[ ]` Create the dynamic blog post page (`/pages/blog/[slug].tsx`).
    * `[ ]` Create the login page (`/pages/login.tsx`) with a form.
    * `[ ]` Create the registration page (`/pages/register.tsx`) with a form.
    * `[ ]` Create dynamic pages for categories and tags (`/pages/category/[slug].tsx`).
* **State Management & API Calls**
    * `[ ]` Set up a global state management solution (e.g., React Context or Zustand) for user authentication state.
    * `[ ]` Create a typed API client or service functions to fetch data from the FastAPI backend.
    * `[ ]` Implement the login form logic to call the `/auth/token` endpoint and store the token.
* **Component Building**
    * `[ ]` Build a `PostCard` component for displaying post previews.
    * `[ ]` Build a `Comment` component to display a single comment.
    * `[ ]` Build a `CommentForm` component, visible only to logged-in users.
    * `[ ]` Build reusable Form components (Input, Button) based on the style guide.

***

## Phase 4: Integration & Feature Completion 🔗

This phase connects the frontend and backend for specific user roles and features.

* **Server-Side Rendering (SSR) & SEO**
    * `[ ]` Use `getServerSideProps` on the `[slug].tsx` page to fetch post data and render it on the server.
    * `[ ]` Use the `Head` component in Next.js to dynamically set the `<title>` and `<meta name="description">` for each blog post.
* **Writer Role Features**
    * `[ ]` Create a protected page for the writer dashboard (`/pages/writer/dashboard.tsx`).
    * `[ ]` Build the UI for the writer to see a table of their own articles.
    * `[ ]` Create a post editor page with a rich text editor (e.g., TipTap or TinyMCE).
    * `[ ]` Implement the logic to create and update posts from the editor, including associating categories and tags.
* **Admin Role Features**
    * `[ ]` Create protected pages for the admin dashboard.
    * `[ ]` Build the UI for managing users (view list, change roles).
    * `[ ]` Build the UI for managing all comments (view list, delete).
    * `[ ]` Build the UI for managing categories and tags (create, edit, delete).
    * `[ ]` Build the UI to display site statistics using a chart library like Recharts.

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
* `[ ]` Pull the final code, build the production Docker images, and launch the application using `docker-compose`.
* `[ ]` Manually create the first `admin` user in the production database.
* `[ ]` Submit the sitemap to Google Search Console.