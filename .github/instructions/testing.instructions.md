---
applyTo: "**/*test*,**/*spec*,tests/**"
---

# BetBot Testing Instructions

Tests should provide confidence that BetBot's product behavior and critical invariants remain correct.

## Test Behavior

Prefer testing observable behavior and domain rules rather than implementation details.

Tests should survive reasonable refactoring.

## Priority

Prioritize tests for:

1. financial correctness
2. authorization
3. event lifecycle
4. betting rules
5. settlement
6. cancellation/refunds
7. transfers
8. daily rewards
9. server isolation
10. user restrictions

## Financial Tests

Test:

* exact decimal calculations
* minimum bet
* insufficient balance
* zero balance
* balance never becoming negative
* winning payouts
* losing bets
* multiple winners
* refunds
* transfers
* administrative adjustments

## Settlement Tests

Settlement tests should cover:

* valid winner selection
* multiple winners
* invalid zero-winner settlement
* losing bets
* winning payouts
* atomic failure
* retry/idempotency
* already-settled events
* already-processed bets
* events with no bets

## Event Lifecycle Tests

Cover:

```text
SCHEDULED → STARTED
STARTED → AWAITING_RESULT
AWAITING_RESULT → SETTLED

SCHEDULED → CANCELLED
STARTED → CANCELLED
AWAITING_RESULT → CANCELLED
```

Also verify invalid transitions.

## Betting Tests

Cover:

* betting while scheduled
* betting after start
* betting after cancellation
* betting after settlement
* minimum stake
* insufficient balance
* odds snapshot
* multiple bets
* multiple outcomes
* opposing outcomes
* bet modification before start
* bet modification after start

## Authorization Tests

Test authorization independently from UI behavior.

Cover:

* normal user
* administrator
* non-member
* betting-disabled user
* BetBot-banned user
* cross-server access
* stale/invalid authorization state

## Concurrency Tests

Where practical, test race-sensitive operations.

Particularly:

* concurrent daily claims
* concurrent transfers
* concurrent settlement
* concurrent betting against a limited balance

The test suite should verify that invariants survive concurrent requests.

## Test Names

Test names should describe behavior and expected outcome.

Prefer:

```text
rejects_bet_when_event_has_started
```

over:

```text
test_event_status_method
```

## Avoid Brittle Tests

Do not assert:

* incidental internal implementation
* irrelevant object ordering
* exact database query structure
* framework internals

unless the behavior is specifically important.

## Regression Tests

When fixing a bug:

1. reproduce it with a test
2. implement the fix
3. verify the regression test fails before the fix when practical
4. verify the complete relevant suite afterward
