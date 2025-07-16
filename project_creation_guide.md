### **Part I: Foundational Phases - Setting the Stage for Your Blog**

The initial planning is the most critical part of launching a successful blog. These steps will help you define your purpose and create a clear roadmap.

---

#### **Section 1: Project Initiation and Discovery**

This phase is about defining a clear, unified vision. It translates your ideas into a concrete plan, which is crucial for a project with distinct user roles and content types.

* **Define Your Core Purpose:** The blog will serve a dual purpose: it will be a personal space to share articles about your daily life and a professional platform to publish tech and development articles.
* **Set SMART Objectives:**
    * "Develop the core platform with a three-tier role system (Admin, Writer, Reader) and deploy the initial version in 4 months."
    * "Publish 4 articles (2 tech, 2 personal) and onboard 10 beta readers for feedback within the first month post-launch."
* **Define Your Target Audience:** You will be writing for a mixed audience, including developers, gamers, and the general public. This means your design must be intuitive for non-tech users, and your writing voice must be adaptable.
* **Requirements Gathering and Scope:** The introduction of user roles is the most significant requirement.
    * **In Scope (Functionality):**
        * **Public Users (Not Logged In):** Can read published articles.
        * **Reader Role:** Can manage their own account, read published articles, and post/manage their own comments.
        * **Writer Role:** All Reader permissions, plus the ability to create, edit, and manage their own articles (drafts and published).
        * **Admin Role:** All Writer permissions, plus access to an admin dashboard to manage all users, articles, and comments, and to view site-wide statistics.
    * **Out of Scope (For Initial Launch):** Social media login, full-text search engine, and real-time notifications.

---

#### **Section 2: Strategic Planning & Information Architecture (IA)**

This is the technical blueprint, now updated to include the logic for multiple user roles and content categories.

* **Technology Stack & Architecture:** The stack remains Next.js, FastAPI, PostgreSQL, Redis, and Docker. The architecture must now explicitly support role-based access control (RBAC).
* **Information Architecture (IA):**
    * **API Endpoints (FastAPI):** Your API needs role-protected endpoints.
        * **Public:** `GET /posts`, `GET /posts/{post_id}`
        * **Reader+:** `POST /comments`, `PUT /users/me`, `GET /users/me`
        * **Writer+:** `POST /posts`, `PUT /posts/{post_id}` (with ownership check)
        * **Admin Only:** `GET /admin/stats`, `GET /users`, `DELETE /comments/{comment_id}`
    * **Page Routes (Next.js):** The frontend requires role-specific pages and layouts.
        * **Public:** `/`, `/blog/[slug]`, `/login`, `/register`
        * **Reader+:** `/profile`
        * **Writer+:** `/writer/dashboard`, `/writer/editor/{post_id}`
        * **Admin Only:** `/admin/dashboard`, `/admin/users`, `/admin/content`
    * **Database Schema (PostgreSQL):**
        * The `users` table must have a `role` column (e.g., using a PostgreSQL `ENUM` type for 'reader', 'writer', 'admin').
        * The `posts` table needs a `category` column ('Tech', 'Personal Life') and a `status` column ('draft', 'published').

---

#### **Section 3: UI/UX Design and Prototyping**

This phase focuses on creating a modern, eye-friendly design that reflects your personal aesthetic and caters to a broad audience.

* **Create Wireframes:** Design distinct wireframes for each major view: the public article page, the user profile, the writer's article editor, and the admin's statistical dashboard.
* **Develop a Comprehensive Style Guide:**
    * **Color Palette:** Based on your themes of plants, wood, mountains, and steampunk, here is a proposed eye-friendly, modern color scheme:
        * **Background:** `#24282B` (Dark Charcoal) - A deep, dark base that's easy on the eyes.
        * **Text:** `#E8E2D9` (Alabaster) - A soft, off-white for high readability without harsh contrast.
        * **Primary (Wood & Earth):** `#5C3D2E` (Deep Coffee) - For major UI components like footers or sidebars.
        * **Secondary (Plants):** `#364B44` (Brunswick Green) - For secondary elements and accents.
        * **Accent (Steampunk Brass):** `#C8A870` (Antique Brass) - For critical interactive elements like buttons and links to draw user attention.
    * **Component Styling:** Use a framework like Tailwind CSS to create reusable components that use these color variables, ensuring a consistent and professional look.
* **Design for Responsiveness:** Ensure the design works flawlessly on all devices. The admin dashboard, in particular, must be usable on mobile for on-the-go management.

---

#### **Section 4: Content Strategy and Creation**

Your content strategy must accommodate two distinct streams of articles.

* **Create a Content Matrix:** Your content spreadsheet should now include a `Category` column ('Tech' or 'Personal Life'). This will help you balance your content and plan your writing schedule.
* **Define Brand Voice and Tone:** Develop a flexible voice. For tech articles, it can be precise and informative. For daily life posts, it can be more personal and reflective. The overall tone should remain authentic and approachable to bridge the gap between your audiences.
* **Write Initial Content:** Before launch, write at least two tech articles and two personal articles. Also, write the copy for your core pages (About, Contact).

### **Part II: Core Execution and Delivery**

This is where you build the application, with a strong focus on implementing the role-based features.

---

#### **Section 5: Technical Development and Implementation**

Development is now more complex, involving authorization logic throughout the stack.

* **Foundational Setup:** Your Docker setup remains the same, but you will initialize your PostgreSQL database with the new tables for users (with roles), posts, and comments.
* **User Authentication and Authorization System:**
    * **Database Schema:** Create the `users` table with a `role` column. Create `posts` and `comments` tables with foreign keys linking back to the `user_id`.
    * **Backend (FastAPI):** This is a critical task. Implement a robust dependency injection system for security. A dependency function will check the user's JWT token for their role and grant or deny access to endpoints accordingly. You must also implement ownership checks (e.g., a writer can only edit posts where the `author_id` matches their own).
    * **Frontend (Next.js):** Implement role-based rendering. Fetch the user's role upon login and store it in a global state (e.g., using React Context). Use this state to:
        * Conditionally render UI elements (e.g., show an "Admin" link in the nav).
        * Protect pages from unauthorized access.
* **Feature Development:**
    * **Writer Dashboard:** A dedicated page where a writer can view a table of their articles, see their status ('draft'/'published'), and have options to edit or create new ones.
    * **Admin Dashboard:** A multi-tabbed interface for admins. It will feature:
        * A user management table to view, edit roles, or delete users.
        * A content management table to manage all articles and comments.
        * A statistics view with charts (using a library like **Recharts** or **Chart.js**) displaying data like new users per week or views per article.
    * **Comment System:**
        * **Frontend:** A component below each article to display comments and a form for authenticated users to submit new ones.
        * **Backend:** Endpoints to create, read, and delete comments, with business logic to ensure users can only delete their own comments (unless they are an Admin).

---

#### **Section 6: Comprehensive Quality Assurance (QA) and Testing**

Your testing strategy must now include comprehensive checks for the role-based access control.

* **Functional and Security Testing:**
    * Write specific tests to verify your authorization logic. Create test scenarios for each role.
    * **Example Scenarios:**
        * "Verify a 'Reader' receives a 403 Forbidden error when trying to access the `POST /posts` endpoint."
        * "Verify a 'Writer' can successfully edit their own post but gets a 403 error when trying to edit another writer's post."
        * "On the frontend, verify that a logged-in 'Reader' cannot see the 'Writer Dashboard' link in the navigation."
    * Use E2E tests with Cypress or Playwright to automate logging in as different roles and attempting to access restricted pages and features.

---

#### **Section 7: Deployment, Launch, and Handover**

The deployment process remains technically similar, but initial setup requires more care.

* **Go-Live (Deployment):** When you deploy, you will need to create the first `admin` user in your production database manually or via a secure, one-time script. This is a critical step to ensure you can manage the live application.
* **Project Handover and Documentation:** Your documentation (especially the README.md) must now include a section detailing the different user roles and their permissions. For your future self, document the process for promoting a user to 'Writer' or 'Admin' in the production environment.

---

#### **Section 8: Post-Launch Operations and Maintenance**

Your ongoing tasks now include user management.

* **Regular Maintenance:** In addition to software updates and backups, you will have administrative tasks like responding to user issues, promoting trusted readers to writers, and moderating content if necessary.
* **Continuous Improvement:** Use your admin dashboard analytics to understand your audience. Are your tech articles more popular? Are users engaging with comments? Use these data-driven insights to guide your future content and feature development.