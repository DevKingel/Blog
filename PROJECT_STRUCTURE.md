# Project Architecture Documentation

## Technology Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS (PNPM)
- **Backend**: FastAPI, Python 3.11, SQLAlchemy 2.0 (UV)
- **Testing**: Jest (Unit), Playwright (E2E), pytest
- **CI/CD**: GitHub Actions
- **Infrastructure**: Docker, Docker Compose

## Directory Structure

```bash
├── src/
│   ├── frontend/
│   │   ├── components/      # Shared UI components
│   │   ├── layouts/         # Application layouts
│   │   ├── pages/           # Next.js page routes (app router)
│   │   ├── lib/             # Client-side libraries
│   │   ├── styles/          # Global CSS/Tailwind config
│   │   └── public/          # Static assets
│   │
│   └── backend/
│       ├── app/             # FastAPI application core
│       ├── routers/         # API endpoint definitions
│       ├── models/          # SQLAlchemy models
│       ├── schemas/         # Pydantic schemas
│       └── services/        # Business logic layer

├── tests/
│   ├── unit/                # Unit tests (Jest/pytest)
│   ├── integration/         # Integration tests
│   └── e2e/                 # Playwright tests

├── docs/
│   ├── technical/           # ADRs and system diagrams
│   ├── user-guides/         # API documentation
│   └── deployment/          # Cloud deployment guides

├── .github/
│   └── workflows/
│       ├── ci-frontend.yml  # Next.js build & test
│       └── ci-backend.yml   # Python test & build

├── docker-compose.yml       # Dev environment setup
├── Dockerfile.frontend      # Next.js production build
├── Dockerfile.backend       # Python/UVicorn setup
└── Makefile                 # Dev commands
```

## Key Configuration Files

### Frontend
- `package.json`: PNPM workspace configuration
- `next.config.js`: Next.js build
- `tailwind.config.js`: Tailwind setup
- `jest.config.js`: Testing framework config
- `tsconfig.json`: TypeScript configuration

### Backend
- `pyproject.toml`: PEP 621 project metadata
- `alembic.ini`: Database migrations
- `.env.sample`: Environment template
- `pytest.ini`: Coverage configuration

## Development Workflow
1. **Testing Strategy**:
   - Unit tests with coverage reporting
   - Playwright for browser automation
   - pytest-cov for backend coverage
2. **CI/CD Pipeline**:
   - Parallel test execution
   - Coverage reporting in CI
3. **Docker Setup**:
   - Hot-reload in development
   - Layer caching for PNPM/UV
   - Multi-stage builds
4. **Package Management**:
   - Frontend: PNPM for dependency management
   - Backend: UV for fast Python package installation

## Implementation Notes
- Starter files will be provided for:
  - Frontend base configuration (PNPM workspace)
  - Backend UV toolchain setup
  - Makefile with common dev commands

## Version Control

### Commit Message Convention
Example commit for architectural documentation:
```bash
git commit -m "docs(architecture): Add initial project structure documentation

- Outline directory hierarchy and component responsibilities
- Define technology stack choices
- Document development workflow processes
- Add Docker/CI configuration overview"
```

Follow Conventional Commits format:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks