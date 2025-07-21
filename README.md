# Blog Platform Documentation

## Project Overview

Modern blog platform with decoupled architecture:

-   **Backend**: FastAPI/Python
-   **Frontend**: Next.js/TypeScript
-   **Database**: PostgreSQL
-   **Cache**: Redis

![Architecture Diagram](/docs/images/architecture.png)

## Key Features

-   Role-based access control (User, Writer, Admin)
-   Server-side rendered content
-   JWT authentication
-   Article analytics tracking
-   Admin dashboard with metrics

## Tech Stack

| Component        | Technology       |
| ---------------- | ---------------- |
| API Framework    | FastAPI 0.116.0  |
| Frontend         | Next.js 15.3     |
| ORM              | SQLAlchemy 2.0   |
| Styling          | Tailwind CSS 3.3 |
| Containerization | Docker 28.3.2    |

## Getting Started

### Prerequisites

-   Docker 28.3.2+
-   Node.js 24.4+
-   Python 3.13.5+

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/blog-platform.git
cd blog-platform

# Start development environment
docker compose -f compose.yaml -f compose.override.yaml up --build
```

## Project Structure

```
blog-platform/
├── backend/         # FastAPI application
│   ├── app/         # Core application logic
│   │   ├── api/     # API endpoints
│   │   ├── models/  # Database models
│   │   └── schemas/ # Pydantic schemas
├── frontend/        # Next.js application
│   ├── app/         # Page routes
│   ├── components/  # React components
│   └── lib/         # API client utilities
└── docs/            # Documentation assets
```

## API Documentation

Access auto-generated OpenAPI docs at `/docs` when running the backend. Key endpoints:

| Endpoint Group | Description               | Example Route        |
| -------------- | ------------------------- | -------------------- |
| Authentication | User registration/login   | POST /auth/token     |
| Articles       | CRUD operations for posts | GET /api/v1/articles |
| Admin          | User/content management   | GET /admin/users     |

## Environment Variables

Required configuration (see `.env.example`):

```ini
# Backend
DATABASE_URL=postgresql://user:pass@db:5432/blog
JWT_SECRET_KEY=your-secret-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

Production deployment steps:

1. Configure production environment files
2. Build optimized Docker images:

```bash
docker compose -f compose.yaml -f compose.production.yaml build
```

3. Run migration scripts
4. Start services in detached mode:

```bash
docker compose -f compose.yaml -f compose.production.yaml up -d
```

## Contributing

1. Create feature branch from `main`
2. Implement changes with tests
3. Submit pull request for review

## License

MIT License - see [LICENSE](LICENSE) for details
