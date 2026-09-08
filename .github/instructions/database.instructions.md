---
applyTo: "**/*migration*,**/*schema*,**/*model*,**/database/**"
---

# BetBot Database Instructions

The database stores financial, betting, authorization, and historical data.

Treat it as critical infrastructure.

## Schema Design

Schema design must preserve:

* server isolation
* financial auditability
* event lifecycle integrity
* bet odds snapshots
* transaction history
* user restrictions
* settlement safety

Prefer explicit relationships and constraints over relying solely on application code.

## Monetary Values

Do not store currency using binary floating-point database types.

Currency requires exact decimal representation with two decimal places.

Odds require exact decimal representation supporting up to three decimal places.

## Financial Records

Transactions are immutable.

Do not design normal application flows around updating historical financial records.

Corrections should create additional records.

## Balance

If a current balance is stored separately from the transaction ledger, the design must make clear:

* which component is used for fast balance reads
* how it stays consistent with financial operations
* how reconciliation can detect inconsistencies

Balance updates and their corresponding transactions must occur atomically.

## Constraints

Use database constraints where they materially protect important invariants.

Examples may include:

* unique daily reward per user/server/day
* unique Discord server ID
* unique user account per server
* valid relationships between bets/events/outcomes
* valid settlement ownership
* prevention of invalid duplicate financial operations

Do not rely exclusively on application checks for concurrency-sensitive uniqueness.

## Server Isolation

Queries involving server-scoped entities should make the server boundary explicit.

Avoid data-access APIs that make it easy to accidentally query globally when the operation is intended to be server-scoped.

## Migrations

All schema changes require migrations.

Before creating a migration:

1. inspect the current schema
2. inspect existing migration conventions
3. consider existing production data
4. consider indexes and constraints
5. consider rollback/recovery

Never casually drop columns, tables, indexes, or data.

## Data Retention

Historical betting and financial records must be retained.

User deletion/anonymization must not destroy required financial history.

## Indexes

Add indexes based on actual access patterns.

Likely important query patterns include:

* events by server/status/start time
* bets by event
* bets by user
* transactions by account/time
* users by server
* daily rewards by server/user/date

Do not add indexes without considering write cost and actual query usage.

## Concurrency

Database transactions and constraints are important tools for protecting:

* balances
* transfers
* settlements
* refunds
* daily rewards
* concurrent betting

Do not assume application-level locks are sufficient across multiple application processes.
