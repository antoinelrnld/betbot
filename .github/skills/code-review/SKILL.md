---
name: code-review
description: Perform a production-quality review of BetBot changes, focusing on correctness, security, domain invariants, concurrency, and maintainability.
---

# Code Review

Review changes as a production pull request.

Do not focus only on style.

Prioritize correctness and risk.

---

## 1. Understand the change

Read:

* issue
* changed files
* relevant product documentation
* relevant domain documentation
* relevant architecture documentation
* tests

Understand the intended behavior before evaluating the implementation.

---

## 2. Correctness

Check:

* requirements are satisfied
* edge cases are handled
* invalid states are rejected
* error paths are safe
* existing behavior is preserved

---

## 3. Domain invariants

Verify:

* balances cannot become negative
* financial operations are atomic
* transactions are immutable
* settlements are idempotent
* refunds are idempotent
* transfers are atomic
* daily rewards cannot be duplicated
* odds snapshots are preserved
* event lifecycle transitions are valid
* event structure cannot change after bets exist
* settled/cancelled events are terminal

---

## 4. Authorization

Check every sensitive operation.

Verify:

* authentication is required
* server membership is validated
* server context is validated
* administrator permission is verified server-side
* BetBot bans are enforced
* betting-disabled state is enforced
* cross-server access is impossible

Do not accept frontend authorization as evidence of security.

---

## 5. Financial safety

For every financial operation, ask:

```text
Can this operation:
- double-charge?
- double-pay?
- create money?
- destroy money?
- create a negative balance?
- leave a partial transaction?
- become inconsistent after retry?
- become inconsistent after concurrent requests?
```

If yes, identify the issue.

---

## 6. Concurrency

Look for race conditions around:

* balance checks
* transfers
* betting
* bet modification
* settlement
* refunds
* daily rewards

Application-level checks without appropriate transactional/concurrency protection should be treated as suspicious.

---

## 7. Database

Review:

* migration safety
* constraints
* indexes
* foreign keys
* transaction boundaries
* server isolation
* historical data preservation

---

## 8. Security

Look for:

* authorization bypasses
* IDOR-style access
* missing server scoping
* leaked secrets
* unsafe logging
* unsafe external input
* insecure session handling
* trust in client-provided roles or IDs

---

## 9. API and frontend

Check that:

* backend validation exists
* errors are handled
* stale state is handled
* real-time updates do not override authoritative server state
* users receive understandable feedback
* sensitive actions are not merely hidden from unauthorized users

---

## 10. Tests

Determine whether tests cover the meaningful behavior.

Do not accept tests that only exercise the happy path for high-risk financial operations.

---

## 11. Maintainability

Look for:

* unnecessary abstractions
* duplicated business logic
* excessive complexity
* unrelated changes
* unclear naming
* hidden side effects
* premature optimization

Prefer simple, explicit code.

---

## Review output

Organize findings by severity:

### Critical

Security vulnerabilities, data corruption, financial corruption, or severe correctness failures.

### High

Important bugs that could materially affect users or system integrity.

### Medium

Meaningful correctness, maintainability, or reliability problems.

### Low

Minor issues that are worth addressing but do not materially threaten the change.

### Positive observations

Mention particularly strong implementation choices when useful.

If there are no meaningful issues, explicitly state that.

Do not manufacture findings merely to appear thorough.
