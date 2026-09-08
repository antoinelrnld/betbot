# BetBot Architecture

## 1. Purpose

This document defines the technical architecture for BetBot.

BetBot is a Discord-first virtual betting platform with a first-class web client.

The architecture must support:

* multiple Discord servers
* isolated server economies
* Discord-based authentication
* Discord bot interactions
* web interactions
* administrative functionality
* event lifecycle automation
* financial transactions
* immutable financial history
* reliable background processing
* real-time client updates
* strong authorization
* concurrency-safe operations
* production deployment

The architecture prioritizes correctness over premature optimization.

---

# 2. Architectural Principles

## 2.1 Backend is authoritative

The backend owns all business rules.

Neither the Discord bot nor the web frontend may independently implement authoritative business logic.

Examples:

* whether a user may bet
* whether betting is open
* whether an event may be modified
* whether a user has enough balance
* payout calculation
* settlement
* cancellation
* transfers
* daily rewards
* administrator authorization

All of these must be enforced by backend/domain logic.

---

## 2.2 One domain, multiple interfaces

BetBot has multiple clients:

* Discord bot
* Web application
* background workers
* administrative tools

They must use the same application/domain services.

The Discord bot and web frontend must not contain separate implementations of financial or betting rules.

Conceptually:

```text
                    ┌──────────────────┐
                    │   Web Frontend   │
                    └────────┬─────────┘
                             │
                             ▼
┌────────────────┐     ┌───────────────┐
│ Discord Client │────▶│   API / App   │
└────────────────┘     │    Layer      │
                       └───────┬───────┘
                               │
                               ▼
                       ┌───────────────┐
                       │    Domain     │
                       │    Services   │
                       └───────┬───────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │ PostgreSQL  │       │   Workers   │
             └─────────────┘       └─────────────┘
```

---

# 3. Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* pytest

Python is the primary backend language.

The backend should use modern Python typing and asynchronous APIs where appropriate.

---

## Discord

Use `discord.py` for Discord integration.

Discord-specific code must remain in an adapter/integration layer.

Discord event handling must call application/domain services rather than implement business rules directly.

---

## Database

Use PostgreSQL.

PostgreSQL is the authoritative persistence layer.

Financial amounts must use exact decimal types.

Do not use floating-point types for:

* balances
* stakes
* payouts
* rewards
* transfers
* odds calculations

Recommended database representation:

```text
NUMERIC(...)
```

with precision and scale chosen explicitly for each financial field.

---

## ORM

Use SQLAlchemy 2.x.

Database access must remain behind repositories/data-access abstractions where doing so improves separation of concerns.

Do not allow HTTP handlers or Discord handlers to contain complex database queries and business rules together.

---

## Migrations

Use Alembic.

Every schema change must have a migration.

Never modify production schema manually as part of normal application development.

Migrations must be:

* deterministic
* reviewable
* safe
* reversible where practical
* tested against realistic data

---

## Frontend

Use:

* Next.js
* TypeScript
* App Router
* Tailwind CSS

The frontend is a first-class application, not merely an administrative dashboard.

The frontend communicates with the backend API.

The frontend must never be trusted to enforce authorization or financial rules.

---

## Cache / Coordination

Redis may be introduced for:

* distributed locks
* short-lived cache
* rate limiting
* job coordination
* real-time infrastructure

Redis must not become the source of truth for financial state.

PostgreSQL remains authoritative.

Do not introduce Redis into a feature unless there is a demonstrated need.

---

# 4. Repository Structure

The preferred repository structure is:

```text
/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── application/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   ├── integrations/
│   │   │   └── discord/
│   │   ├── workers/
│   │   └── main.py
│   ├── tests/
│   ├── alembic/
│   ├── pyproject.toml
│   └── ...
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   ├── tests/
│   ├── package.json
│   └── ...
│
├── docs/
│   ├── product.md
│   ├── domain.md
│   ├── architecture.md
│   └── roadmap.md
│
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   ├── skills/
│   └── agents/
│
├── docker/
├── docker-compose.yml
└── README.md
```

The exact structure may evolve if implementation demonstrates a better organization.

---

# 5. Backend Layers

The backend should follow a layered architecture.

## 5.1 API layer

Responsible for:

* HTTP routing
* authentication extraction
* request validation
* response serialization
* HTTP-specific error mapping

The API layer must remain thin.

It should not contain financial business rules.

---

## 5.2 Application layer

Responsible for orchestrating use cases.

Examples:

```text
CreateEvent
ModifyBet
PlaceBet
CancelEvent
SettleEvent
TransferFunds
ClaimDailyReward
UpdateServerSettings
BanUser
UnbanUser
```

Application services coordinate:

* authorization
* domain operations
* repositories
* transactions
* external integrations
* side effects

---

## 5.3 Domain layer

Contains core BetBot business rules.

Examples:

* Event lifecycle
* Betting rules
* Settlement rules
* Payout calculation
* Economy rules
* Transfer rules
* User restrictions
* Daily reward eligibility

The domain should be as independent of frameworks as practical.

---

## 5.4 Infrastructure layer

Responsible for:

* SQLAlchemy
* PostgreSQL
* Redis
* background job implementation
* persistence
* external infrastructure

Infrastructure must not redefine domain rules.

---

## 5.5 Integration layer

Contains external systems.

Examples:

```text
integrations/
└── discord/
    ├── bot
    ├── oauth
    └── permissions
```

External systems are adapters around the core application.

---

# 6. Multi-Tenant Server Model

Every server-owned BetBot resource must be associated with a Discord server.

Conceptually:

```text
Discord Server
    │
    ├── Server Settings
    ├── User Accounts
    ├── Events
    ├── Bets
    ├── Transactions
    ├── Notifications
    └── Restrictions
```

A user's global Discord identity is separate from their server-specific BetBot account.

Therefore:

```text
Discord User
     │
     ├── Server A account
     ├── Server B account
     └── Server C account
```

Balances never cross server boundaries.

Transfers must never cross server boundaries.

Bans are server-specific.

Betting restrictions are server-specific.

---

# 7. Financial Architecture

Financial operations require special treatment.

Every balance-changing operation must be atomic.

Examples:

* placing a bet
* modifying a bet
* cancelling an event
* settling an event
* daily reward
* transfer
* admin adjustment

A financial operation should conceptually follow:

```text
BEGIN TRANSACTION

validate state
lock required rows
validate balance / authorization
create immutable ledger entries
update current balance
update related domain state

COMMIT
```

If any operation fails, the entire financial operation must roll back.

---

# 8. Balance and Ledger

User accounts maintain a current balance for efficient reads.

The transaction ledger remains immutable.

Conceptually:

```text
UserAccount
├── current_balance
└── ...

Transaction
├── server
├── user
├── type
├── amount
├── balance_before
├── balance_after
├── reference
├── created_at
└── metadata
```

The current balance is a materialized representation of the ledger state.

Financial history must never be edited destructively.

Corrections create additional transactions.

---

# 9. Event Lifecycle

The event state machine is:

```text
SCHEDULED
    │
    ▼
STARTED
    │
    ▼
AWAITING_RESULT
    │
    ▼
SETTLED
```

Cancellation is possible before settlement:

```text
SCHEDULED ─────┐
STARTED ───────┼──▶ CANCELLED
AWAITING_RESULT┘
```

Rules:

* betting opens immediately when created
* betting closes at start time
* start time cannot be in the past
* end time moves the event to `AWAITING_RESULT` when bets exist
* events without bets automatically settle at end
* events with bets require administrative settlement
* settlement is atomic
* settlement is idempotent
* settlement is immutable

---

# 10. Event Automation

A background worker is responsible for time-driven state transitions.

Examples:

```text
start scheduled events
transition ended events
auto-settle events with no bets
send notifications
process retryable asynchronous work
```

Workers must be retry-safe.

A worker retry must never:

* pay a user twice
* refund a user twice
* create duplicate rewards
* duplicate notifications where deduplication is required
* settle an event twice

---

# 11. Betting Architecture

Bets contain an immutable snapshot of the relevant pricing information.

A bet stores:

```text
event
outcome
stake
odds
potential payout
created_at
status
```

The odds stored on a bet are the odds that were active when the bet was placed.

Changing event odds must not change existing bets.

---

# 12. Settlement Architecture

Settlement is a single atomic operation.

Conceptually:

```text
BEGIN

lock event
verify settlement state
validate winning outcomes

lock affected accounts
calculate payouts
create payout/loss ledger entries
update balances
mark bets settled
mark event settled

COMMIT
```

Settlement must be idempotent.

A retry must not create duplicate payouts.

Winning payout:

```text
total_payout = stake × odds
```

Profit:

```text
profit = total_payout - stake
```

Payouts are rounded to two decimal places using an explicitly defined decimal rounding policy.

---

# 13. Authorization

Authorization is performed by the backend.

Discord Administrator permission is the source of truth for administrative privileges.

For administrative operations:

```text
request
  ↓
authenticated Discord identity
  ↓
verify current server membership
  ↓
verify current Discord Administrator permission
  ↓
authorize operation
  ↓
execute use case
```

Never trust:

* frontend admin flags
* client-provided roles
* cached authorization without an appropriate freshness policy
* Discord usernames
* Discord display names

Discord user IDs and server IDs are authoritative identifiers.

---

# 14. Authentication

Discord OAuth2 is the only web authentication mechanism.

The web application must not introduce independent BetBot passwords.

The web application establishes an authenticated session after successful Discord authentication.

The backend must verify that:

1. the Discord identity is valid
2. the user is currently a member of the selected server
3. BetBot is currently installed in that server
4. the requested resource belongs to that server

---

# 15. Discord Bot Architecture

Discord interactions should follow:

```text
Discord interaction
       ↓
Discord adapter
       ↓
Application use case
       ↓
Domain
       ↓
Persistence
       ↓
Response
```

Discord-specific concerns include:

* slash commands
* buttons
* select menus
* modals
* Discord embeds
* Discord permissions
* interaction responses
* notification delivery

Business rules must remain outside these handlers.

---

# 16. Web Architecture

The web frontend communicates with backend APIs.

Conceptually:

```text
Browser
   ↓
Next.js
   ↓
BetBot API
   ↓
Application services
   ↓
Domain
   ↓
PostgreSQL
```

The frontend is responsible for:

* presentation
* interaction
* local UI state
* loading states
* optimistic UI only where safe
* accessibility
* responsive design
* displaying server errors
* real-time updates

The frontend is not responsible for authoritative business decisions.

---

# 17. Real-Time Updates

BetBot requires real-time updates for:

* event state changes
* odds changes
* balance changes
* bet changes
* cancellations
* settlements

The implementation should use a backend-controlled real-time abstraction.

The initial implementation may use WebSockets or Server-Sent Events depending on the concrete requirements.

The choice should prioritize:

1. correctness
2. simplicity
3. reconnect behavior
4. authorization
5. scalability

Real-time transport must never be required for financial correctness.

If a real-time message is lost, the client must be able to recover through normal API reads.

---

# 18. Background Jobs

Background jobs should be designed as durable, retry-safe operations.

Examples:

* event lifecycle transitions
* notifications
* cleanup
* reconciliation
* scheduled tasks

Every job must have clear idempotency behavior.

A job must never assume that it runs exactly once.

---

# 19. Notifications

Notifications are secondary effects.

Core financial/domain operations must succeed even if notification delivery fails.

Therefore:

```text
financial operation
       ↓
COMMIT
       ↓
notification job
       ↓
delivery
```

not:

```text
notification
       ↓
financial operation
```

Notification failures must be observable and retryable.

---

# 20. Server Isolation

Every server-owned query must enforce server scope.

For example:

```text
WHERE server_id = current_server_id
```

must be part of the authorization/data-access strategy.

Never rely solely on frontend filtering.

A user must never be able to access another server's:

* balance
* bets
* events
* transactions
* settings
* restrictions
* administrative data

---

# 21. Concurrency

Concurrency must be considered explicitly for:

* placing bets
* modifying bets
* transfers
* daily rewards
* admin balance adjustments
* event cancellation
* event settlement

Database transactions and appropriate row-level locking or unique constraints should be preferred over application-level race-condition assumptions.

---

# 22. Observability

Production deployments should provide:

* structured logs
* request IDs
* error tracking
* job failure visibility
* database error visibility
* audit information for administrative operations

Sensitive information must never be logged.

Financial operations should have enough audit context to reconstruct what happened without exposing secrets.

---

# 23. Security

Security requirements include:

* server-side authorization
* strict input validation
* secure OAuth handling
* CSRF protection where applicable
* secure session management
* rate limiting where appropriate
* protection against cross-server access
* protection against duplicate financial operations
* no secrets in source control
* safe error messages
* dependency updates
* least-privilege infrastructure

---

# 24. Testing Strategy

Critical domain behavior requires automated tests.

Highest-priority test areas:

1. balance correctness
2. ledger correctness
3. betting
4. bet modification
5. event lifecycle
6. settlement
7. cancellation/refunds
8. transfers
9. daily rewards
10. authorization
11. server isolation
12. banned-user restrictions
13. concurrency
14. idempotency

Integration tests should verify PostgreSQL behavior for critical transactional operations.

Frontend tests should focus on user-visible behavior rather than implementation details.

---

# 25. API Design

APIs should be organized around domain resources and use cases.

Examples:

```text
/auth
/servers
/events
/bets
/balance
/transactions
/transfers
/daily-reward
/admin/events
/admin/economy
/admin/users
/admin/settings
```

Exact endpoint naming may evolve during implementation.

API contracts must be explicit.

Breaking API changes require deliberate review.

---

# 26. Error Handling

Errors must be:

* explicit
* predictable
* safe
* actionable

The API should distinguish between:

* validation errors
* authentication failures
* authorization failures
* resource not found
* invalid domain state
* insufficient balance
* concurrency conflicts
* external integration failures
* internal failures

Internal implementation details must not leak to users.

---

# 27. Deployment

The application should be deployable as separate processes/services:

```text
web
api
discord-bot
worker
postgres
redis (optional)
```

For local development, Docker Compose should provide the infrastructure required to run the system consistently.

Production infrastructure may combine or separate services depending on deployment requirements.

---

# 28. Architecture Decision Rules

When implementing a new feature, prefer:

1. existing architecture over introducing new architecture
2. domain services over duplicated business logic
3. PostgreSQL transactions over distributed coordination
4. database constraints over assumptions
5. idempotent operations over exactly-once assumptions
6. simple infrastructure over premature complexity
7. explicit code over clever abstractions
8. tests over documentation-only guarantees

New infrastructure requires justification.

---

# 29. Definition of Architectural Completion

A feature is not architecturally complete until:

* domain rules are implemented centrally
* authorization is enforced server-side
* persistence is safe
* financial operations are atomic where applicable
* concurrency is considered
* retries are safe
* tests cover critical behavior
* Discord and web use the same application logic
* documentation remains accurate
* observability is sufficient for production debugging

Architecture should evolve when implementation reveals real requirements, but changes must be deliberate and documented.
