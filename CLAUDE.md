# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router), TypeScript, Node.js 20+ (`.nvmrc` in root) |
| Frontend Tooling | Biome v2 (lint + format), Vitest + React Testing Library |
| Backend | FastAPI, Python 3.12+, SQLAlchemy 2.0 (async) |
| Backend Tooling | uv (package mgmt), Ruff (lint + format), mypy, pytest + httpx |
| Database | PostgreSQL 16 via Docker Compose, Alembic migrations |
| Architecture | Clean Architecture + DDD (single bounded context: todos) |

---

## Architecture

### Layer Dependency Rule

Dependencies flow **inward only**. This is the single most important constraint in the codebase.

```
Interface (routes/)            ← HTTP entry, Pydantic schemas
    │ calls
    ▼
Application (use cases/)       ← Orchestrates domain, owns DTOs
    │ uses
    ▼
Domain (domain/)               ← Entities, repo interfaces, zero external deps
    ▲ implements
    │
Infrastructure (infra/)        ← SQLAlchemy, DB session, DI wiring
```

**Rules that must never be violated:**
- `domain/` never imports from `application/`, `infrastructure/`, or `interface/`
- `application/` never imports from `infrastructure/` or `interface/`
- Routes call use cases only — never repositories directly
- `infrastructure/` implements repository ABCs declared in `domain/`

### Layer Responsibilities

| Layer | Directory | What lives here |
|---|---|---|
| Domain | `backend/src/app/domain/{context}/` | Entities (`@dataclass`), value objects, repository interfaces (`abc.ABC`), domain services |
| Application | `backend/src/app/application/{context}/` | Use case classes (one per operation), input/output DTOs (plain dataclasses) |
| Infrastructure | `backend/src/app/infrastructure/` | SQLAlchemy models, repository implementations, DB engine/session, DI wiring (`di.py`) |
| Interface | `backend/src/app/interface/routes/` | FastAPI routers, Pydantic request/response schemas |

### Dependency Injection

FastAPI `Depends()` is the DI mechanism. All wiring lives in `infrastructure/di.py`. Routes inject **use cases**, never repositories.

```python
# infrastructure/di.py
from domain.todo.repository import TodoRepository          # ABC (interface)
from infrastructure.database.todo_repository import SQLAlchemyTodoRepository

def get_todo_repository() -> TodoRepository:
    return SQLAlchemyTodoRepository(session=get_session())

def get_create_todo_use_case(
    repo: TodoRepository = Depends(get_todo_repository),
) -> CreateTodo:
    return CreateTodo(repo)

# interface/routes/todo.py
@router.post("/todos")
async def create_todo(use_case: CreateTodo = Depends(get_create_todo_use_case)):
    ...
```

### Frontend Feature Structure

Frontend is organized by **feature**, not by technical layer. Each feature is self-contained.

```
features/{name}/
├── components/   # React components
├── hooks/        # Data-fetching hooks (own loading/error state)
├── api/          # fetch() calls to backend — only place API calls live
└── types.ts      # TypeScript types for this feature
```

`shared/` holds cross-feature layout and utilities. Pages in `app/` are thin shells that import from features.

### Frontend → Backend Connection

Frontend calls the FastAPI backend **directly** (no Next.js API route proxy). The backend base URL is configured via `NEXT_PUBLIC_API_URL`. CORS is configured on the FastAPI side.

---

## Project Structure

```
├── frontend/
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   ├── features/         # Feature modules (see Architecture above)
│   │   └── shared/           # Shared components and utils
│   ├── package.json
│   ├── biome.json
│   ├── tsconfig.json
│   └── next.config.ts
├── backend/
│   ├── src/
│   │   └── app/
│   │       ├── main.py       # FastAPI app factory + CORS + exception handlers
│   │       ├── domain/       # Domain layer (bounded context dirs inside)
│   │       ├── application/  # Use cases (bounded context dirs inside)
│   │       ├── infrastructure/  # DB models, repo implementations, di.py
│   │       └── interface/    # FastAPI routers + Pydantic schemas
│   ├── tests/
│   │   ├── unit/             # Domain + use case tests (repos are mocked)
│   │   └── integration/      # Endpoint tests via httpx (real test DB)
│   ├── alembic/              # Migration scripts
│   └── pyproject.toml
├── docker-compose.yml        # PostgreSQL container definition
├── .env.example              # Template for required env vars
└── CLAUDE.md
```

---

## Environment Variables

Copy `.env.example` to `.env` before running anything. Both frontend and backend read from it.

| Variable | Used by | Example |
|---|---|---|
| `DATABASE_URL` | Backend | `postgresql+asyncpg://dev:devpassword@localhost:5432/todo_db` |
| `NEXT_PUBLIC_API_URL` | Frontend | `http://localhost:8000` |

---

## Development Commands

### Database (prerequisite — start before backend)

```bash
docker compose up -d           # Start PostgreSQL container
docker compose down            # Stop and remove container
```

### Backend

```bash
cd backend
uv sync                                          # Install dependencies
uv run alembic upgrade head                      # Apply pending migrations
uv run uvicorn app.main:app --reload             # Dev server → localhost:8000

uv run pytest                                    # All tests
uv run pytest tests/unit/                        # Unit tests only
uv run pytest tests/integration/ -v              # Integration tests only

uv run ruff check .                              # Lint
uv run ruff format .                             # Format
uv run mypy src/                                 # Type check
uv run alembic revision --autogenerate -m "msg"  # Generate new migration
```

### Frontend

```bash
cd frontend
npm install                    # Install dependencies
npm run dev                    # Dev server → localhost:3000
npm run build                  # Production build

npm run lint                   # Biome lint
npm run format                 # Biome format
npm test                       # Run Vitest
npm test -- --coverage         # Tests with coverage report
```

---

## Coding Conventions

### Backend

- **Use cases are named as verb phrases:** `CreateTodo`, `ListTodos`, `CompleteTodo`. Each has a single `execute()` method. This is the only entry point for business logic.
- **Domain entities are `@dataclass`.** No Pydantic, no SQLAlchemy columns. They are framework-free value holders.
- **Repository interfaces use `abc.ABC` + `@abstractmethod`.** Implementations in `infrastructure/` are the only place that knows about SQLAlchemy.
- **Pydantic models exist only in `interface/`** (HTTP request/response schemas). Application-layer DTOs are plain dataclasses.
- **Domain exceptions** are defined in `domain/`. Routes have a global exception handler (`main.py`) that converts domain exceptions → HTTP status codes. Business logic never raises generic `HTTPException`.
- **Unit tests** mock repositories. **Integration tests** use `httpx.AsyncClient` against a test DB distinct from the dev DB.

### Frontend

- **Server Components by default.** Add `"use client"` only to components that use event handlers or hooks.
- **API calls live exclusively in `features/{name}/api/`.** No `fetch()` in components or hooks directly.
- **Hooks own loading/error/data state.** Components receive data and callbacks — they know nothing about fetching mechanics.
- **Define `types.ts` first** when adding a new feature. Types drive the shape of API calls and components.
