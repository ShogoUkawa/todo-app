# TODO App

A full-stack TODO application — **Next.js** frontend + **FastAPI** backend — built with Clean Architecture and DDD.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 (App Router), TypeScript |
| Backend | FastAPI, Python 3.12+, SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Architecture | Clean Architecture + DDD (single bounded context) |

---

## Prerequisites

- **Node.js 20+** — a `.nvmrc` is in the repo root. If you use [nvm](https://github.com/nvm-sh/nvm), run `nvm use` once.
- **[uv](https://docs.astral.sh/uv/)** — Python package manager.
- **[Docker](https://docs.docker.com/get-docker/) + Compose** — runs PostgreSQL locally.
- **[just](https://github.com/casey/just)** — task runner (optional; manual commands are shown below).

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/todo-app.git
cd todo-app

just bootstrap          # install deps + start DB + migrate
just dev                # start backend & frontend
```

### Without `just`

```bash
docker compose up -d                              # 1. PostgreSQL → localhost:5433

cd backend
uv sync --all-extras                              # 2. install deps
uv run alembic upgrade head                       # 3. migrate
uv run uvicorn app.main:app --reload              # 4. backend  → localhost:8000

# ── in a new terminal ──────────────────────────
cd ../frontend
npm install                                       # 5. install deps
npm run dev                                       # 6. frontend → localhost:3000

# ── one-time, after the above ──────────────────────
cd ../backend
uv run pre-commit install                         # 7. git hooks
```

---

## Task Reference

| Command | What it does |
|---|---|
| `just bootstrap` | Install deps, start DB, create test DB, run migrations |
| `just dev` | Start backend + frontend together |
| `just backend` | Backend dev server only |
| `just frontend` | Frontend dev server only |
| `just test` | Run all backend tests |
| `just lint` | Lint backend (ruff) + frontend (biome) |
| `just migrate` | Apply pending migrations |
| `just migrate-new "msg"` | Generate a new Alembic migration |
| `just db-shell` | Drop into a `psql` session |
| `just pre-commit-install` | Install pre-commit hooks (run once after clone) |
| `just pre-commit-run` | Run all pre-commit hooks manually |

Run `just --list` for the full set.

---

## Deployment

### Frontend → GitHub Pages

Automated on every push to `main` via [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

**One-time setup:**
1. Go to **repo → Settings → Pages → Source** and select **GitHub Actions**.
2. Add a repository secret called `API_URL` whose value is your deployed backend URL (see the Render section below).

The live site will appear at `https://YOUR_USERNAME.github.io/todo-app/`.

### Backend → Render

A [Render blueprint](https://docs.render.com/blueprints) is provided in [`render.yaml`](render.yaml).

**Setup:**
1. Sign up at [render.com](https://render.com).
2. Provision a PostgreSQL database. Render's free tier no longer includes managed Postgres, so use an external provider such as [Neon](https://neon.tech/) (free tier available).
3. Create a new **Web Service** from this repo; Render will detect `render.yaml`.
4. Set the two required environment variables in the Render dashboard:
   - `DATABASE_URL` — your PostgreSQL connection string.
   - `FRONTEND_URL` — the **origin** of your GitHub Pages site (scheme + host only, no path). Example: `https://YOUR_USERNAME.github.io`
5. After the first deploy, open Render's shell and run migrations:
   ```bash
   cd backend && uv run alembic upgrade head
   ```

---

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every push and pull request to `main`:

- **Backend** — spins up a PostgreSQL service, runs migrations, executes `pytest`, lints with `ruff`.
- **Frontend** — lints with Biome, runs a production build.

---

## Environment Variables

| Variable | Where | Purpose |
|---|---|---|
| `DATABASE_URL` | `backend/.env` | PostgreSQL connection string |
| `FRONTEND_URL` | `backend/.env` | Allowed CORS origin |
| `NEXT_PUBLIC_API_URL` | `frontend/.env.local` | Backend base URL |

`.env.example` and `backend/.env.example` contain templates; copy and fill in values before running.
