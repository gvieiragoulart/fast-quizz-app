# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development
make dev                    # Start dev server (uvicorn with reload on port 8000)
make install                # Install dependencies from requirements.txt

# Testing
make test                   # Run all tests
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/unit/domain/test_user.py::TestUserEntity::test_create_user  # Single test
make test-cov               # Tests with HTML coverage report

# Code Quality
make lint                   # ruff check + mypy
make format                 # black + ruff --fix

# Database
make migrate                # alembic upgrade head
alembic revision --autogenerate -m "description"  # Create migration

# Docker
make docker-up              # Build and start PostgreSQL + app
make docker-down            # Stop containers
```

## Architecture

Clean Architecture with four layers — dependencies flow inward only:

**Domain** (`src/domain/`) → Pure entities and repository interfaces (ABCs). No framework imports.

**Application** (`src/application/use_cases/`) → Business logic orchestration. Each entity has a UseCases class that coordinates repositories and validation. All methods are async.

**Infrastructure** (`src/infrastructure/`) → Implementations: SQLAlchemy models/repositories (`database/`, `repositories/`), auth utilities (`auth/`). Repositories convert between domain entities and SQLAlchemy models via `_to_entity()`/`_to_model()` methods.

**API** (`src/api/`) → FastAPI routes, Pydantic schemas (Create/Update/Response variants per entity), and OAuth2 dependencies. Routes wire up use cases via `Depends()`.

Key flow: Route → UseCase → Repository Interface → Repository Implementation → Database

## Tech Stack

- **FastAPI** + **Uvicorn** (ASGI)
- **SQLAlchemy 2.0** ORM with **Alembic** migrations
- **PostgreSQL** (production/Docker) / **SQLite** (local dev via .env)
- **JWT** auth (python-jose) + **Argon2** password hashing (passlib)
- **Pydantic v2** for request/response validation

## Testing

Tests use an in-memory SQLite database configured in `tests/conftest.py`. Integration tests create a test client with auth token fixture (`tests/integration/conftest.py`). Pytest markers: `unit`, `integration`, `slow`. Async mode is `auto` (no need for `@pytest.mark.asyncio`).

## Code Style

- Line length: 100 (both ruff and black)
- Target: Python 3.11
- mypy strict mode enabled (`disallow_untyped_defs=true`)

## Environment

Copy `.env.example` to `.env`. Key variables: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`. Local dev defaults to SQLite (`sqlite:///./dev.db`).
