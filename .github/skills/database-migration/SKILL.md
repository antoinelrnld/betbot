---
name: database-migration
description: Safely design, implement, and validate BetBot database schema changes and migrations.
---

# Database Migration

Use this skill whenever a change modifies database schema, constraints, indexes, relationships, or persisted data.

## 1. Inspect

Before creating a migration:

* inspect the current schema
* inspect existing migration history
* inspect model definitions
* inspect relevant queries
* inspect existing data assumptions
* identify production compatibility concerns

Never assume the schema is empty.

---

## 2. Understand the change

Determine whether the change requires:

* new table
* new column
* removed column
* renamed column
* changed type
* foreign key
* unique constraint
* check constraint
* index
* data migration
* backfill
* archival change

Prefer additive and backwards-compatible changes when possible.

---

## 3. Protect data

Do not casually:

* drop production data
* delete historical financial records
* rewrite immutable transactions
* remove foreign-key relationships
* change monetary precision destructively

If a destructive migration is genuinely required, explicitly explain:

* why
* what data is affected
* how existing data is handled
* how rollback/recovery works

---

## 4. Financial schema

Financial entities require special care.

Ensure:

* exact decimal representation
* immutable transaction records
* auditable relationships
* safe balance updates
* appropriate uniqueness constraints
* appropriate indexes

If a balance is stored separately from the ledger, preserve a clear consistency model.

---

## 5. Concurrency constraints

Use database-level constraints when they protect invariants that application code alone cannot safely enforce.

Examples:

```text
unique(server_id, user_id)
unique(server_id, user_id, reward_date)
```

Use the actual schema conventions once established.

---

## 6. Migration implementation

Follow the project's migration framework and naming conventions.

Keep migrations focused.

Do not combine unrelated schema changes.

If a data migration is required, make it deterministic and safe to rerun where practical.

---

## 7. Validation

After creating the migration:

* validate schema generation
* run migration tests if available
* test affected domain behavior
* inspect generated SQL where appropriate
* verify indexes/constraints
* run relevant application tests

Do not declare the migration safe without validation.

---

## 8. Rollback

Consider rollback before implementation.

If the migration cannot be safely reversed, document why and identify the recovery strategy.

---

## 9. Final review

Check:

* existing data preserved
* server isolation preserved
* financial invariants preserved
* appropriate constraints added
* indexes justified
* migration deterministic
* application code compatible with both old and new states where required
* tests updated
