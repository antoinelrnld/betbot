---
applyTo: "backend/**"
---

# BetBot Backend Instructions

The backend is the authoritative implementation of BetBot business rules.

## Architecture

Keep these concerns separated where the chosen architecture permits:

* transport/API/Discord adapters
* application/use-case orchestration
* domain/business rules
* persistence
* external integrations

Do not put substantial business logic directly inside HTTP handlers or Discord handlers.

Both Discord and web clients must ultimately use the same backend behavior.

## Domain Logic

Business rules must be enforced independently of the caller.

Never assume that a request originated from a trusted UI.

Important rules include:

* event lifecycle transitions
* betting availability
* bet modification
* odds snapshots
* payout calculation
* settlement
* cancellation/refunds
* transfers
* daily rewards
* balance invariants
* user restrictions
* server isolation
* administrator authorization

## Financial Operations

Every balance-changing operation must be atomic.

A financial operation should leave the system in a valid state even if:

* the request is retried
* two requests race
* the process crashes
* notification delivery fails

Use the database transaction facilities appropriate to the selected stack.

## Decimal Arithmetic

Never use binary floating point for currency or odds calculations.

Use the project's exact decimal representation.

Do not convert monetary values through floating-point types.

## Authorization

Authorization must be enforced server-side.

For administrator operations, verify current Discord Administrator permission.

For server-scoped operations, verify that the authenticated user is authorized to act within the requested server.

Never trust:

* client-provided roles
* client-provided server IDs without authorization checks
* client-provided account IDs
* hidden UI controls

## Server Isolation

Every server-scoped operation must enforce the server boundary.

Never allow:

```text
Server A → Server B data
```

through:

* IDs
* query parameters
* API payloads
* cached objects
* background jobs

Prefer authorization and ownership checks close to the data access boundary.

## Idempotency

Design retry-sensitive operations to be idempotent.

Especially:

* settlement
* refunds
* daily rewards
* scheduled event transitions
* notification processing where appropriate

## Errors

Use explicit application/domain errors.

Do not expose internal exceptions directly to users.

Log enough information to diagnose failures without logging secrets or unnecessary sensitive data.

## Background Processing

Scheduled tasks must be safe to retry.

Do not assume a scheduled task executes exactly once.

For event transitions, the database state must be the source of truth.

## Testing

Backend tests should focus heavily on domain behavior and invariants.

Prefer tests that verify observable behavior over implementation details.

Critical business logic should be covered before integration details.

## External Integrations

Discord, email, notification, and other external services should be isolated behind appropriate interfaces/adapters when useful.

Do not allow external service failures to corrupt core financial operations.

## Performance

Do not optimize prematurely.

First produce a correct implementation.

When performance becomes relevant:

* inspect actual bottlenecks
* measure
* optimize the relevant boundary
* preserve domain invariants

Do not introduce caching or asynchronous complexity without justification.
