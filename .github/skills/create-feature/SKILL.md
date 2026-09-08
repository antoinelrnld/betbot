---
name: create-feature
description: Implement a GitHub issue as a production-quality BetBot feature. Use when asked to implement a feature, bug fix, enhancement, or issue from start to finish.
---

# Create Feature

Implement a BetBot GitHub issue using a disciplined, production-oriented workflow.

## Required workflow

Follow these phases in order:

1. Understand
2. Inspect
3. Plan
4. Implement
5. Test
6. Validate
7. Review
8. Summarize

Do not skip directly from the issue to implementation for non-trivial work.

---

## 1. Understand

Read the complete issue.

Identify:

* objective
* functional requirements
* acceptance criteria
* non-goals
* constraints
* dependencies
* edge cases

Then read the relevant sections of:

* `docs/product.md`
* `docs/domain.md`
* architecture documentation, if it exists

If the issue conflicts with established product/domain rules, stop and identify the conflict.

Do not silently change product behavior.

---

## 2. Inspect

Before modifying code:

* inspect repository structure
* identify the relevant backend/frontend components
* inspect related domain/application logic
* inspect relevant database models
* inspect existing migrations
* inspect related tests
* identify existing implementation patterns

Prefer extending existing patterns over creating parallel ones.

Do not assume a file exists merely because an issue suggests it should.

---

## 3. Plan

For non-trivial changes, produce a concise plan before implementation.

The plan should identify:

* affected areas
* domain changes
* application changes
* API/transport changes
* frontend changes
* database changes
* migrations
* tests
* risks

Keep the plan proportional to the complexity of the issue.

Do not create speculative infrastructure.

---

## 4. Implement

Implement the smallest complete solution satisfying the issue.

Preserve existing behavior outside the scope of the issue.

Business rules belong in the backend/application/domain layer.

Do not duplicate business rules between Discord and web clients.

For financial operations:

* use exact decimal arithmetic
* use atomic transactions
* protect against concurrent operations
* create appropriate ledger records
* make retry-sensitive operations idempotent

For authorization:

* verify permissions server-side
* verify server membership where required
* verify BetBot restrictions
* never trust frontend authorization

---

## 5. Database Changes

If schema changes are required:

* inspect current schema
* follow existing migration conventions
* create a migration
* preserve existing data
* add appropriate constraints/indexes
* test meaningful data migrations

Do not manually modify production schema outside the migration system.

---

## 6. Test

Add or update tests for changed behavior.

Prioritize business-critical cases.

For relevant changes, consider:

* happy path
* validation failure
* authorization failure
* boundary conditions
* concurrency
* idempotency
* transaction rollback
* server isolation
* regression cases

Do not write tests solely to increase coverage numbers.

---

## 7. Validate

Run the project's appropriate:

* unit tests
* integration tests
* type checks
* linters
* formatters
* build checks

Use the project's existing commands.

Do not invent replacement commands unless necessary.

Fix failures caused by the implementation.

Do not silently ignore failing validation.

---

## 8. Review

Before declaring completion, review the change as if reviewing a pull request.

Check:

### Product

* Does it satisfy the issue?
* Does it match `docs/product.md`?

### Domain

* Are invariants preserved?
* Are invalid state transitions prevented?

### Security

* Is authorization server-side?
* Can another server's data be accessed?

### Financial correctness

If applicable:

* Is the operation atomic?
* Is decimal arithmetic exact?
* Can the operation double-apply?
* Is the ledger correct?
* Can a balance become negative?

### Concurrency

Could two requests race?

Could a retry duplicate the operation?

### Testing

Are important edge cases covered?

### Maintainability

Is the solution understandable?

Did the implementation introduce unnecessary complexity?

---

## 9. Summarize

At the end, report:

### Implemented

List the meaningful changes.

### Tests

List the validation commands actually run and their results.

### Database

Mention migrations if applicable.

### Notes

Mention important implementation decisions.

### Remaining

Explicitly list anything not implemented or not verified.

Never claim a test or validation passed unless it was actually run.
