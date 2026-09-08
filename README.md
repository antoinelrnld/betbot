# BetBot

BetBot is a Discord-first virtual betting application with a first-class web client. Users wager virtual currency on events within Discord servers; it is not a real-money gambling platform.

## Project status

This repository is currently bootstrapped for implementation. It contains the documented backend, frontend, and infrastructure boundaries, but no product functionality has been implemented yet.

## Architecture

BetBot is planned as a modular monolith with shared application and domain behavior:

- **Backend:** Python services will provide the authoritative application and domain logic through a FastAPI API, Discord adapters, PostgreSQL persistence, and retry-safe workers.
- **Frontend:** A Next.js App Router application will provide a responsive web client and communicate with the backend API.
- **Local infrastructure:** Docker Compose provides PostgreSQL for local development. Application containers and other infrastructure will be added when their corresponding features are implemented.

The backend is authoritative for authentication, authorization, server isolation, financial operations, betting rules, and event lifecycle behavior. Discord and web clients must use the same backend behavior.

## Documentation

Product behavior and domain invariants are defined in:

- [`docs/product.md`](docs/product.md)
- [`docs/domain.md`](docs/domain.md)

Technical architecture and implementation direction are documented in:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/adr/0001-initial-architecture.md`](docs/adr/0001-initial-architecture.md)

## Local development

Local development uses Docker Compose for shared infrastructure. PostgreSQL is
the authoritative persistence service; backend, frontend, Discord, and worker
processes are not implemented yet.

```bash
cp .env.example .env
cp backend/.env.example backend/.env
docker compose up -d --wait postgres
```

Set the PostgreSQL database name, username, password, and host port in the
root `.env` file. Compose intentionally requires these values instead of
providing credentials in the repository. The backend reads
`BETBOT_*` values from `backend/.env`; shell environment variables with the
same prefix take precedence. Use the root `.env` values to construct
`BETBOT_DATABASE_URL` in `backend/.env`; the database password must match.

Check the service health with:

```bash
docker compose ps
docker compose exec postgres sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

PostgreSQL data is stored in the named `postgres-data` volume and survives
container restarts. Stop the service without deleting data with
`docker compose down`; use `docker compose down -v` only when intentionally
discarding the local database. The `.env` files are ignored by Git and must
never contain production credentials in committed files.

### Backend

The backend uses `uv` for dependency management and exposes a minimal FastAPI
application while the domain features are implemented incrementally. Copy
`backend/.env.example` before starting it; `BETBOT_DATABASE_URL` is required
and startup fails with a validation error when it is absent or empty.

```bash
cd backend
uv sync --group dev
uv run python -m app.main
```

The API health endpoint is available at
[`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health). Backend checks
can be run with:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Configuration is loaded from `BETBOT_*` environment variables or
`backend/.env`. Shell values override the file:

| Variable | Required | Purpose |
| --- | --- | --- |
| `BETBOT_DATABASE_URL` | Yes | Async PostgreSQL connection URL. |
| `BETBOT_APP_ENV` | No | Runtime environment: `development`, `test`, or `production`; defaults to `development`. |
| `BETBOT_APP_HOST` | No | API bind host; defaults to `127.0.0.1`. |
| `BETBOT_APP_PORT` | No | API bind port from 1 through 65535; defaults to `8000`. |
| `BETBOT_DEBUG` | No | Enables backend debug mode; defaults to `false`. |

Discord and OAuth variables are not required until those integrations exist.
When introduced, they belong only in backend configuration and must never use
the `NEXT_PUBLIC_` prefix. No credentials are committed to the repository.

### Frontend

The frontend uses Next.js App Router, TypeScript, and Tailwind CSS.

```bash
cd frontend
npm ci
npm run dev
```

The initial web shell is available at
[`http://127.0.0.1:3000`](http://127.0.0.1:3000). Frontend validation can be
run with:

```bash
npm run lint
npx tsc --noEmit
npm run build
```

Browser API requests use `NEXT_PUBLIC_API_BASE_URL`, documented in
`frontend/.env.example`, and default to `http://localhost:8000` for local
development. Only `NEXT_PUBLIC_*` values may be exposed to the browser; never
put backend, Discord, OAuth, database, or other secret values in
`frontend/.env.local`. The current shell does not yet implement product
functionality.
