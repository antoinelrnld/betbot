# ADR 0001: Initial BetBot Architecture

* Status: Accepted
* Date: 2026-09-08

## Context

BetBot requires a production-oriented architecture supporting:

* Discord interactions
* a first-class web application
* multiple isolated Discord servers
* server-specific virtual economies
* event scheduling
* betting
* settlement
* financial transactions
* administrative operations
* background automation
* real-time updates

Financial correctness, authorization, maintainability, and operational reliability are more important than minimizing the number of technologies.

## Decision

BetBot will use:

* Python for backend development
* FastAPI for HTTP APIs
* discord.py for Discord integration
* PostgreSQL as the authoritative database
* SQLAlchemy for database access
* Alembic for migrations
* Pydantic for validation
* Next.js + TypeScript for the web client
* Tailwind CSS for frontend styling
* dedicated background workers
* Redis only when justified by a concrete infrastructure requirement
* Docker for reproducible local and production environments

The backend will use a layered architecture:

```text
API
 ↓
Application
 ↓
Domain
 ↓
Infrastructure
```

Discord and other external systems will be implemented as adapters.

## Rationale

### Python

Python is already the selected backend language and has a mature ecosystem for APIs, Discord integrations, background workers, testing, and data processing.

### FastAPI

FastAPI provides strong typing, validation, async support, automatic OpenAPI documentation, and a clean foundation for an API-first architecture.

### PostgreSQL

BetBot has transactional financial requirements.

PostgreSQL provides strong transactional guarantees, constraints, indexing, row-level locking, and mature support for concurrent workloads.

### Next.js

The web application is a first-class client rather than a simple administration page.

Next.js provides a mature React-based application framework suitable for the responsive dashboard and user-facing web experience.

### Redis

Redis is intentionally not a mandatory architectural dependency.

It may be introduced for specific requirements such as:

* distributed coordination
* caching
* rate limiting
* job infrastructure
* real-time infrastructure

PostgreSQL remains authoritative.

## Consequences

### Positive

* Strong transactional guarantees
* Clear separation between clients and domain logic
* Reusable backend functionality
* Good testing boundaries
* Production-ready foundation
* Easy API documentation
* Strong support for multiple clients
* Good path toward horizontal scaling

### Negative

* More moving parts than a monolithic single-process application
* Requires discipline around architectural boundaries
* Requires database migration management
* Requires explicit background-job design
* Discord and web integration need additional adapter code

These costs are accepted because BetBot has financial and multi-client requirements that justify them.

## Rejected Alternatives

### Frontend-only business logic

Rejected because financial and authorization rules cannot safely live in an untrusted client.

### SQLite as the primary production database

Rejected because BetBot requires stronger concurrency and transactional infrastructure.

### Redis as the primary financial store

Rejected because Redis must not be the source of truth for financial state.

### Separate business logic for Discord and web

Rejected because duplicated rules would create correctness and maintenance risks.

### Microservices

Rejected for v1.

BetBot does not currently require independent service ownership or deployment boundaries.

A modular monolith with workers provides sufficient separation while keeping operational complexity manageable.

## Future Reconsideration

This decision should be revisited only when actual scale or operational requirements justify it.

Potential future changes include:

* dedicated real-time infrastructure
* separate notification service
* dedicated job infrastructure
* read replicas
* service decomposition

Such changes should be driven by measurable requirements rather than speculation.
