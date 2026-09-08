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

Local development will use Docker Compose for shared infrastructure. The current Compose configuration starts PostgreSQL only; backend, frontend, Discord, and worker processes are not implemented yet.

```bash
docker compose up -d postgres
```

The PostgreSQL connection settings can be overridden with `POSTGRES_*` environment variables.
