# Prerequisites: Node.js 20+ (see .nvmrc)
# Run `just` to see available commands

set shell := ["bash", "-c"]

_frontend := "frontend"

# ─── Development ─────────────────────────────────────────

# Start development server
dev:
    cd {{_frontend}} && npm run dev

# Production build
build:
    cd {{_frontend}} && npm run build

# ─── Code Quality ────────────────────────────────────────

# Lint code (check only)
lint:
    cd {{_frontend}} && npm run lint

# Format code
format:
    cd {{_frontend}} && npm run format

# Fix lint issues
lint-fix:
    cd {{_frontend}} && npx biome check --write .

# ─── Setup ───────────────────────────────────────────────

# Install dependencies
install:
    cd {{_frontend}} && npm ci

# Bootstrap: install dependencies
bootstrap: install
