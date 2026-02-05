# Prerequisites: Node.js 20+ (see .nvmrc), uv, Docker
# Run `just` to see available commands

set shell := ["bash", "-c"]

_backend  := "backend"
_frontend := "frontend"

# ─── Database ────────────────────────────────────────────

# Start PostgreSQL
db-up:
    docker compose up -d

# Stop PostgreSQL
db-down:
    docker compose down

# Open a psql shell
db-shell:
    docker compose exec db psql -U dev -d todo_db

# Create the test database (run once after db-up)
db-test-create:
    docker compose exec db createdb -U dev todo_db_test || true

# ─── Backend ─────────────────────────────────────────────

# Start backend dev server
backend:
    cd {{_backend}} && uv run uvicorn app.main:app --reload

# Run backend tests
backend-test:
    cd {{_backend}} && uv run pytest -v

# Lint backend (check only)
backend-lint:
    cd {{_backend}} && uv run ruff check . && uv run ruff format --check .

# Fix backend lint issues
backend-lint-fix:
    cd {{_backend}} && uv run ruff check --fix . && uv run ruff format .

# Type-check backend
backend-typecheck:
    cd {{_backend}} && uv run mypy src/

# Apply pending migrations
migrate:
    cd {{_backend}} && uv run alembic upgrade head

# Generate a new migration — usage: just migrate-new "add foo column"
migrate-new name:
    cd {{_backend}} && uv run alembic revision --autogenerate -m "{{name}}"

# ─── Frontend ────────────────────────────────────────────

# Start frontend dev server
frontend:
    cd {{_frontend}} && npm run dev

# Production build
frontend-build:
    cd {{_frontend}} && npm run build

# Lint frontend (check only)
frontend-lint:
    cd {{_frontend}} && npm run lint

# Format frontend
frontend-format:
    cd {{_frontend}} && npm run format

# Fix frontend lint issues
frontend-lint-fix:
    cd {{_frontend}} && npx biome check --write .

# ─── Hooks ───────────────────────────────────────────────

# Install pre-commit hooks (run once after cloning)
pre-commit-install:
    cd {{_backend}} && uv run pre-commit install

# Run pre-commit on all files (useful for CI or manual check)
pre-commit-run:
    cd {{_backend}} && uv run pre-commit run --all-files

# ─── Combined ────────────────────────────────────────────

# Start backend + frontend concurrently (Ctrl+C stops both)
dev: db-up
    (cd {{_backend}} && uv run uvicorn app.main:app --reload) & BACKEND=$!; trap 'kill $BACKEND 2>/dev/null' EXIT; cd {{_frontend}} && npm run dev

# Run all tests
test: backend-test

# Lint everything
lint: backend-lint frontend-lint

# Install all dependencies
install:
    cd {{_backend}} && uv sync --all-extras
    cd {{_frontend}} && npm ci

# Bootstrap: install deps, start DB, create test DB, run migrations, install hooks
bootstrap: install db-up db-test-create migrate pre-commit-install
