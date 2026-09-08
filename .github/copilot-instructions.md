# BetBot — GitHub Copilot Instructions

## Project

BetBot is a production-grade Discord-first virtual betting application with a first-class web client.

Users wager virtual currency on events within Discord servers.

The product is not a real-money gambling platform.

The authoritative product specification is:

* `docs/product.md`
* `docs/domain.md`

Read those documents before implementing functionality that affects product behavior or domain rules.

---

# Core Engineering Principles

## 1. Correctness over cleverness

Prefer simple, explicit, maintainable solutions.

Do not introduce abstractions, dependencies, patterns, or infrastructure unless they solve a real problem.

Avoid premature optimization.

Do not over-engineer for hypothetical future requirements.

---

## 2. Protect domain invariants

Business rules are not UI concerns.

Critical rules include:

* balances must never become negative
* financial operations must be atomic
* financial history is immutable
* settlements must be idempotent
* refunds must be idempotent
* transfers must be atomic
* daily rewards must be concurrency-safe
* bets must retain their odds snapshot
* betting closes when an event starts
* event structure becomes immutable once bets exist
* settled and cancelled events are terminal
* server data must remain isolated
* administrator permissions must be verified server-side
* frontend authorization must never be trusted
* currency calculations must use exact decimal arithmetic

Never weaken or bypass a domain invariant merely to make an implementation easier.

---

# Architecture

## 3. Separate clients from business logic

Discord and web are clients of the same application/domain behavior.

Do not duplicate business rules between:

* Discord commands
* Discord components
* HTTP/API handlers
* web pages
* background jobs

Client code should translate user interaction into application operations.

Business logic belongs in the appropriate backend/application/domain layer.

---

## 4. Backend is authoritative

The backend must independently validate:

* authentication
* server membership
* authorization
* event state
* user restrictions
* balances
* bet validity
* transfer validity
* settlement validity
* configuration
* input constraints

Never rely on the frontend or Discord UI to enforce security or business rules.

---

# Financial Operations

## 5. Treat money-like operations as critical

Although BetBot uses virtual currency, balances and transactions must be treated with the same engineering discipline as financial data.

Balance-changing operations must be:

* atomic
* concurrency-safe
* auditable
* retry-safe where applicable

Never perform a balance update separately from the operation that caused it.

For example, placing a bet must not be implemented as:

```text
update balance
then
create bet
```

unless both operations participate in the same atomic transaction.

---

## 6. Never use binary floating point for currency

Use exact decimal arithmetic for:

* balances
* stakes
* payouts
* transfers
* rewards
* adjustments

Currency uses two decimal places.

Odds use up to three decimal places.

Do not use binary floating-point arithmetic for financial calculations.

---

## 7. Preserve financial history

Transactions are immutable.

Do not silently edit or delete financial transactions.

Corrections must be represented by new transactions.

Administrative balance changes must be auditable.

---

# Authentication and Authorization

## 8. Discord is the identity provider

Discord is the source of truth for:

* identity
* server membership
* Administrator permission
* display name
* avatar

BetBot is the source of truth for:

* BetBot account state
* balances
* bets
* transactions
* restrictions
* bans
* server configuration

Do not invent a separate identity system unless explicitly required by the product specification.

---

## 9. Never trust client authorization

The frontend may hide unavailable actions for UX purposes, but the backend must always enforce authorization.

Never accept claims such as:

```text
"isAdmin": true
```

from the client as proof of authorization.

Administrator access must be verified against the current Discord permission.

---

# Database

## 10. Schema changes require migrations

Never modify the database schema manually as part of feature implementation.

Schema changes must use the project's migration system.

Migrations must be:

* deterministic
* reviewable
* reversible where practical
* safe for existing data
* tested when they contain meaningful data transformations

Do not destroy production data to simplify a migration.

---

# API and External Input

## 11. Validate external input

Treat all external input as untrusted.

This includes input from:

* Discord
* browsers
* APIs
* background jobs
* webhooks
* configuration
* external services

Validate input at the appropriate application boundary.

Do not assume that frontend validation is sufficient.

---

## 12. Explicit errors

Use explicit, meaningful errors for rejected operations.

Errors should communicate the reason an operation failed without exposing:

* secrets
* internal credentials
* stack traces to end users
* sensitive implementation details

---

# Testing

## 13. Test business-critical behavior

Every meaningful change to business logic should have appropriate tests.

Prioritize tests for:

* event lifecycle
* betting rules
* bet modification
* odds snapshots
* payouts
* settlement
* cancellation/refunds
* transfers
* daily rewards
* balance invariants
* user restrictions
* authorization
* concurrency-sensitive operations

Tests should verify behavior, not implementation details unnecessarily.

---

# Concurrency and Idempotency

## 14. Assume requests can race

Design critical operations assuming two requests can happen simultaneously.

Particularly important:

* betting
* bet modification
* transfers
* daily rewards
* settlement
* refunds
* administrative balance changes

Use appropriate database constraints, transactions, locking, idempotency mechanisms, or other concurrency controls.

Do not attempt to solve concurrency solely with frontend state.

---

# Background Jobs

## 15. Background jobs must be safe to retry

Scheduled/background operations may execute:

* late
* twice
* after a process restart
* after a temporary failure

Jobs must therefore be designed to be idempotent where practical.

This is particularly important for:

* event start transitions
* event end transitions
* automatic settlement of events with no bets
* notifications
* refunds
* other financial processing

---

# Notifications

## 16. Notifications are secondary effects

Notification delivery must never determine whether the underlying business operation succeeds.

For example:

```text
Settlement succeeds
        ↓
Notification attempted
        ↓
Notification fails
        ↓
Settlement remains successful
```

Notification failures should be observable and recoverable without reversing the underlying operation.

---

# Security

## 17. Never expose secrets

Never commit or print:

* Discord bot tokens
* OAuth client secrets
* database credentials
* API keys
* session secrets
* private keys
* production credentials

Use environment/configuration mechanisms appropriate to the deployment architecture.

---

## 18. Minimize sensitive data

Only collect and store information required by BetBot.

Do not introduce unnecessary personal data.

User deletion/anonymization must preserve required financial history.

---

# Dependencies

## 19. Keep dependencies minimal

Before introducing a dependency:

1. Check whether the existing stack already provides the functionality.
2. Check whether a small internal implementation is more appropriate.
3. Consider maintenance and security implications.
4. Consider whether the dependency is justified by the product.

Do not add dependencies merely for convenience.

---

# Implementation Workflow

When implementing an issue, follow this process:

```text
1. Understand
2. Inspect
3. Plan
4. Implement
5. Test
6. Lint / typecheck / format
7. Review
8. Summarize
```

## Understand

Read the issue completely.

Read relevant product/domain documentation.

Identify acceptance criteria and constraints.

If requirements conflict, stop and explain the conflict rather than silently choosing behavior.

## Inspect

Before changing code:

* inspect the existing architecture
* locate related functionality
* identify existing patterns
* inspect relevant tests
* inspect database models/migrations where applicable

Do not assume the repository structure.

## Plan

For non-trivial work, provide a concise implementation plan before making changes.

Identify:

* affected components
* domain changes
* API changes
* database changes
* tests
* risks

## Implement

Make focused changes.

Do not rewrite unrelated code.

Follow existing project conventions unless there is a clear reason to improve them.

## Test

Add or update tests for changed behavior.

Run the narrowest relevant tests first.

Then run broader validation as appropriate.

## Review

Before declaring the issue complete, check:

* business rules
* authorization
* concurrency
* transactions
* error handling
* tests
* migrations
* security
* unintended behavior changes

---

# Change Discipline

## 20. Do not silently change requirements

If implementation reveals an ambiguity:

* identify it
* explain it
* propose the safest option
* ask for a decision when the choice affects product behavior

Do not invent major product behavior.

Small implementation details may be chosen pragmatically when they do not alter user-visible behavior or domain rules.

---

## 21. Keep changes focused

An issue should normally result in a focused change.

Avoid:

* unrelated refactoring
* dependency upgrades unrelated to the issue
* formatting entire repositories unnecessarily
* changing architecture without justification
* fixing unrelated bugs in the same change

If an issue exposes a separate problem, mention it separately.

---

# Commit and Branch Conventions

## 22. Follow Conventional Commits

Commit messages must follow the Conventional Commits format:

```text
<type>[optional scope]: <description>
```

Use a valid type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, or `ci`. Keep the description concise and imperative. Use a body and footers when additional context or breaking changes need to be documented, and mark breaking changes with `!` after the type or scope and/or a `BREAKING CHANGE:` footer.

Branch names must use the same type prefixes and a short kebab-case description:

```text
<type>/<short-description>
```

For example: `feat/add-event-settlement` and `fix/prevent-negative-balance`. Do not use vague branch names such as `work`, `changes`, or `update`.

Pull request titles must follow the same Conventional Commits format as commit messages:

```text
<type>[optional scope]: <description>
```

Use the same valid types, concise imperative descriptions, and breaking-change notation for pull request titles.

---

# Documentation

## 23. Keep documentation synchronized

When a change intentionally modifies established product behavior, update the relevant documentation.

Do not duplicate the entire product specification throughout the repository.

Use:

* `docs/product.md` for product behavior
* `docs/domain.md` for domain rules
* architecture documentation for technical architecture
* code comments for local implementation details

Comments should explain **why**, not merely restate **what** the code does.

---

# Copilot Behavior

When uncertain:

* inspect the repository first
* consult the relevant documentation
* prefer existing project patterns
* avoid guessing
* ask when a product decision is required

Do not claim tests passed unless they were actually run.

Do not claim an implementation is complete if important acceptance criteria remain unverified.

Always distinguish between:

* implemented
* tested
* not tested
* known limitation
* unresolved decision
