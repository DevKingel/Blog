### **Part I: Foundational Phases - Setting the Stage for Your Blog**

The initial planning is the most critical part of launching a successful blog. These steps will help you define your purpose and create a clear roadmap.

---

#### **Section 1: Project Initiation and Discovery**

* **Define Your Core Purpose:** The blog will be a multi-purpose platform for personal and tech articles, designed for a broad audience.
* **Set SMART Objectives:** Your goals remain focused on developing the role-based platform, now with the added complexity of content taxonomies.
* **Define Your Target Audience:** The audience is a mix of tech-savvy users and the general public, reinforcing the need for an intuitive UI.
* **Requirements Gathering and Scope:**
    * **In Scope (Functionality):**
        * **Unauthenticated Users:** Can read published articles but cannot post comments.
        * **Reader Role:** Can manage their own account, read published articles, and post/manage their own comments.
        * **Writer Role:** All Reader permissions, plus the ability to create, edit, and manage their own articles (drafts and published).
        * **Admin Role:** All Writer permissions, plus access to an admin dashboard to manage all users, articles, and comments, and to view site-wide statistics.
        * An Admin-managed system for creating and assigning **categories** and **tags** to articles.
        * The application must be **Server-Side Rendered (SSR)** for optimal **SEO** and initial load performance.
        * The application must feel like a **Single-Page Application (SPA)** during user navigation.

---

#### **Section 2: Strategic Planning & Information Architecture (IA)**

This blueprint now includes the data structures and routes for your content taxonomies and aligns with a modern, SEO-friendly architecture.

* **Technology Stack & Architecture:**
    * **Next.js** is specifically chosen for its powerful hybrid framework capabilities. It will provide true **Server-Side Rendering (SSR)** on a per-request basis, which is essential for SEO. Once loaded, its client-side routing will deliver a fluid **SPA** experience.
* **Information Architecture (IA):**
    * **Database Schema (PostgreSQL):**
        * Create tables for `categories` and `tags`.
        * Create join tables (`post_categories` and `post_tags`) to establish the many-to-many relationships between posts and your taxonomies.
    * **API Endpoints (FastAPI):**
        * Develop Admin-only CRUD endpoints for `/categories` and `/tags`.
        * Update the `GET /posts` endpoint to allow filtering by category or tag slugs.
    * **Page Routes (Next.js):**
        * Add dynamic routes to browse by taxonomy: `/category/[slug]` and `/tag/[slug]`.
        * The Admin dashboard will need routes for managing categories and tags: `/admin/categories` and `/admin/tags`.

---

#### **Section 3: UI/UX Design and Prototyping**

* **Create Wireframes:** Design the views for managing categories and tags in the admin panel. Also, design how categories and tags will be displayed on article pages and as filterable lists.
* **Develop a Comprehensive Style Guide:** The proposed color palette remains ideal for your aesthetic:
    * **Background:** `#24282B` (Dark Charcoal)
    * **Text:** `#E8E2D9` (Alabaster)
    * **Primary:** `#5C3D2E` (Deep Coffee)
    * **Secondary:** `#364B44` (Brunswick Green)
    * **Accent:** `#C8A870` (Antique Brass)

---

#### **Section 4: Content Strategy and Creation**

* **Create a Content Matrix:** Your content planning spreadsheet should now include dedicated columns for `Category` and `Tags` for each planned article. This helps organize your content from the start.

### **Part II: Core Execution and Delivery**

This development phase details the implementation of your new features, with a strong emphasis on the technical strategy for rendering, SEO, and user permissions.

---

#### **Section 5: Technical Development and Implementation**

* **Feature: Category and Tag Management:**
    * **Backend (FastAPI):** Build the CRUD endpoints for categories and tags. Secure them so that only users with the 'Admin' role can access them.
    * **Frontend (Next.js):**
        * **Admin UI:** In the admin dashboard, create the interface for managing categories and tags.
        * **Writer UI:** In the article editor, add a component that allows writers to select from the list of existing categories and tags to associate with their posts.
* **Feature: Comment System:**
    * **Frontend:** A component below each article will display all existing comments to every visitor. However, the form to submit a new comment will only be visible or enabled for authenticated users (Reader, Writer, Admin).
    * **Backend:** Endpoints to create, read, and delete comments, with business logic to ensure users can only delete their own comments (unless they are an Admin).
* **Frontend Development (SSR, SPA, and SEO Focus):**
    * **Server-Side Rendering (SSR):**
        * For dynamic pages that need to be indexed by search engines (like `/blog/[slug]`, `/category/[slug]`), you will use the **`getServerSideProps`** function in Next.js.
        * This function runs on the server for every request, fetches the necessary data from your FastAPI backend, and uses it to pre-render the complete HTML page. This is the core of your SEO strategy, as it ensures search engine crawlers receive fully-populated content.
    * **Single-Page Application (SPA) Experience:**
        * To achieve the fluid feel of an SPA, you will use the Next.js **`<Link>`** component for all internal navigation.
        * When a user clicks a `<Link>`, Next.js handles the routing on the client-side without a full page reload, fetching only the necessary data and updating the UI. This combination gives you the best of both worlds: great SEO from SSR and a fast user experience from client-side navigation.
    * **Search Engine Optimization (SEO):**
        * **Metadata:** For each page, especially blog posts, dynamically manage SEO-critical tags. Use the built-in Next.js `metadata` object to set a unique `<title>` and `<meta name="description">` for each page. This is crucial for search engine rankings.
        * **Semantic HTML:** Write clean, semantic HTML for your components. Use `<h1>` for the main title, `<h2>` for subheadings, and so on.
        * **Sitemap:** After launch, submit an XML sitemap to Google Search Console to help it discover all your pages.

---

#### **Section 6: Comprehensive Quality Assurance (QA) and Testing**

Your testing must now validate the new features, the role-based access control and the SSR/SEO implementation.

* **Functional and Security Testing:**
    * Write specific tests to verify your authorization logic. Create test scenarios for each role.
    * **Example Scenarios:**
        * "Write test cases to ensure that only Admins can create/edit/delete categories and tags."
        * "Verify a 'Reader' receives a 403 Forbidden error when trying to access the `POST /posts` endpoint."
        * "Verify a 'Writer' can successfully edit their own post but gets a 403 error when trying to edit another writer's post."
        * "On the frontend, verify that a logged-in 'Reader' cannot see the 'Writer Dashboard' link in the navigation."
    * Use E2E tests with Cypress or Playwright to automate logging in as different roles and attempting to access restricted pages and features.
* **SEO and SSR Validation:**
    * For a key page like a blog post, use your browser's "View Page Source" feature. **Verify that the rendered HTML contains the full text of the article.** If you only see JavaScript, SSR is not working correctly.
    * Use Google's Rich Results Test to see how a search engine crawler "sees" your page and to validate your metadata.

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