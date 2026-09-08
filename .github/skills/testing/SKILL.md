---
name: testing
description: Design, implement, run, and review tests for BetBot features, bugs, domain rules, and critical business behavior.
---

# Testing

Use this skill when adding tests, investigating failures, validating a feature, or reviewing test coverage.

## Testing philosophy

Tests should provide confidence in behavior.

Prefer:

```text
Given
When
Then
```

style reasoning.

Avoid testing implementation details unless those details are themselves a contract.

---

## Test priority

Prioritize:

1. financial correctness
2. domain invariants
3. authorization
4. event lifecycle
5. betting
6. settlement
7. cancellation/refunds
8. transfers
9. daily rewards
10. server isolation
11. user restrictions
12. API/UI behavior

---

## Financial tests

When financial behavior changes, test:

* exact decimal arithmetic
* minimum amounts
* insufficient balance
* zero balance
* negative balance prevention
* ledger entries
* balance changes
* payout calculations
* refunds
* transfers
* administrative adjustments

---

## Settlement tests

Test:

* one winning outcome
* multiple winning outcomes
* invalid zero winners
* losing bets
* winning payouts
* odds snapshots
* no-bet events
* cancellation
* duplicate settlement requests
* already-settled events
* transaction rollback
* concurrent settlement attempts

---

## Event lifecycle

Test valid and invalid transitions.

Valid:

```text
SCHEDULED → STARTED
STARTED → AWAITING_RESULT
AWAITING_RESULT → SETTLED

SCHEDULED → CANCELLED
STARTED → CANCELLED
AWAITING_RESULT → CANCELLED
```

Invalid transitions should be rejected.

---

## Betting tests

Cover:

* scheduled event
* started event
* awaiting-result event
* settled event
* cancelled event
* server betting disabled
* user betting disabled
* BetBot-banned user
* minimum stake
* insufficient balance
* multiple bets
* multiple outcomes
* opposing outcomes
* odds snapshot
* bet modification
* modification after start

---

## Authorization tests

Test independently from frontend visibility.

Verify:

* administrator access
* standard user restrictions
* non-member access
* BetBot ban
* betting-disabled state
* cross-server access
* stale Discord permission state

---

## Concurrency

For race-sensitive operations, use concurrency tests where the project's test infrastructure supports them.

Important examples:

* two daily reward claims
* simultaneous transfers
* simultaneous bets
* simultaneous settlement
* concurrent refunds

The expected result must preserve domain invariants.

---

## Regression testing

For bugs:

1. reproduce the bug
2. add a regression test
3. implement the fix
4. verify the regression test
5. run the relevant suite

---

## Running tests

Use repository-provided scripts and commands.

Do not assume a specific test framework before inspecting the repository.

Start with focused tests, then broaden validation.

Always report exactly what was run.

---

## Test quality

Avoid:

* excessive mocking
* testing framework internals
* brittle snapshots
* duplicate coverage
* meaningless assertions
* tests that pass while the important behavior is broken

A smaller number of strong tests is preferable to large amounts of low-value coverage.
