# BetBot Development Roadmap

## Goal

Build BetBot incrementally as a production-grade Discord betting platform with a first-class web client.

Development should proceed from infrastructure and domain foundations toward user-facing features.

Each phase should leave the project in a working state.

---

# Phase 0 — Repository Foundation

## Goals

Establish the development environment and repository structure.

### Work

* initialize repository
* configure Python project
* configure frontend project
* configure linting
* configure formatting
* configure type checking
* configure testing
* configure Docker
* configure Docker Compose
* configure environment configuration
* configure CI
* establish project README
* establish development documentation

### Exit criteria

* backend starts
* frontend starts
* PostgreSQL starts
* tests execute
* linting executes
* CI executes
* local development is documented

---

# Phase 1 — Database Foundation

## Goals

Create the core persistence model.

### Core entities

* Server
* User
* ServerUser / UserAccount
* Event
* EventOutcome
* Bet
* Transaction
* restriction records
* server settings

### Work

* SQLAlchemy models
* relationships
* PostgreSQL schema
* Alembic
* constraints
* indexes
* base repositories
* database test infrastructure

### Exit criteria

* migrations work
* schema is reproducible
* server isolation is represented
* financial fields use exact decimal types
* database tests work

---

# Phase 2 — Authentication & Server Context

## Goals

Establish Discord identity and server authorization.

### Work

* Discord OAuth2
* web sessions
* Discord identity model
* server membership verification
* BetBot installation verification
* server selector
* automatic server initialization
* administrator permission verification

### Exit criteria

A user can:

* authenticate with Discord
* see authorized servers
* select a server
* access only authorized server data

An administrator can be recognized through current Discord permissions.

---

# Phase 3 — Economy

## Goals

Build the financial foundation before betting.

### Work

* server starting balance
* user account creation
* immutable transaction ledger
* balance calculation
* daily rewards
* admin balance operations
* transaction history
* transfer system
* financial authorization
* concurrency protection

### Exit criteria

All balance-changing operations are:

* atomic
* auditable
* retry-safe
* server-scoped
* concurrency-safe

---

# Phase 4 — User Restrictions

## Goals

Implement server-specific restrictions.

### Work

* betting disabled
* BetBot ban
* unban
* restriction enforcement
* restriction visibility
* audit history

### Exit criteria

Restrictions work consistently across:

* API
* web
* Discord
* background jobs

---

# Phase 5 — Events

## Goals

Build the event system.

### Work

* event creation
* event listing
* event details
* outcomes
* odds
* scheduling
* lifecycle state machine
* event editing rules
* cancellation
* archiving
* event permissions

### Exit criteria

The complete lifecycle works:

```text
SCHEDULED
→ STARTED
→ AWAITING_RESULT
→ SETTLED
```

with cancellation before settlement.

---

# Phase 6 — Betting

## Goals

Allow users to place and modify bets.

### Work

* event selection
* outcome selection
* stake validation
* odds snapshot
* bet creation
* multiple bets
* bet modification
* balance deduction
* betting restrictions
* betting cutoff
* bet history

### Exit criteria

Users can safely:

* place bets
* modify bets before start
* place multiple bets
* bet on multiple outcomes

Users cannot bypass backend rules.

---

# Phase 7 — Settlement

## Goals

Complete the financial event lifecycle.

### Work

* admin settlement screen
* winning outcome selection
* settlement preview
* payout calculation
* losing bets
* winning bets
* payout transactions
* event settlement
* settlement history
* settlement notifications
* idempotency
* zero-bet automatic settlement

### Exit criteria

Settlement is:

* atomic
* correct
* auditable
* retry-safe
* immutable

---

# Phase 8 — Discord Experience

## Goals

Make BetBot genuinely useful inside Discord.

### Work

* `/betbot`
* events
* balance
* daily reward
* history
* transfers
* help
* interactive buttons
* select menus
* modals
* admin controls
* notifications

### Exit criteria

Core user workflows can be completed naturally from Discord.

---

# Phase 9 — Web Experience

## Goals

Deliver the first-class web client.

### Work

* landing/auth
* server selector
* dashboard
* events
* event details
* betting
* balance
* history
* transfers
* settings
* admin event management
* admin economy
* admin users
* server settings

### Exit criteria

Core functionality available through web.

---

# Phase 10 — Real-Time & Automation

## Goals

Make the system feel live and reduce manual operational work.

### Work

* event start automation
* event end automation
* zero-bet settlement
* notifications
* real-time event updates
* real-time odds updates
* real-time balances
* real-time settlement updates
* retry-safe workers
* job monitoring

### Exit criteria

Time-driven event behavior is reliable without manual intervention.

---

# Phase 11 — Production Hardening

## Goals

Prepare for real usage.

### Work

* rate limiting
* structured logging
* request IDs
* error tracking
* monitoring
* health checks
* security review
* dependency review
* database backup strategy
* disaster recovery
* load testing
* concurrency testing
* migration testing
* production deployment

### Exit criteria

The system can be deployed and operated safely.

---

# Development Rule

Do not jump ahead because a later feature looks more exciting.

Financial correctness comes before UI polish.

The recommended implementation order is:

```text
Foundation
    ↓
Database
    ↓
Authentication
    ↓
Economy
    ↓
Restrictions
    ↓
Events
    ↓
Betting
    ↓
Settlement
    ↓
Discord UX
    ↓
Web UX
    ↓
Automation
    ↓
Production hardening
```

Every phase should leave behind tested, maintainable code.

---

# Issue Strategy

Each implementation unit should be represented by a focused GitHub issue.

Issues should normally describe one coherent capability.

Avoid giant issues such as:

> Build the entire economy.

Prefer:

* Create server economy schema
* Create user server account
* Implement balance ledger
* Implement daily reward
* Implement user transfers
* Implement admin balance adjustment
* Add transaction history API

This allows Copilot to work incrementally and makes changes easier to review.

---

# Definition of Done

A feature is considered complete only when:

* requirements are implemented
* domain rules are enforced
* authorization is enforced server-side
* database changes are migrated
* concurrency is considered
* idempotency is considered
* tests are present
* relevant tests pass
* errors are handled
* documentation is updated
* Discord/web behavior is consistent where applicable
* no unrelated changes were introduced
* the final diff has been reviewed
