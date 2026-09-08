# BetBot Domain Model

This document defines the conceptual domain model and business invariants for BetBot.

It is implementation-independent.

The concrete database schema, framework models, API contracts, and infrastructure are defined separately.

---

# 1. Domain Boundaries

The BetBot domain can be divided into these areas:

```text
Identity & Access
        │
        ├── Server
        ├── User
        └── Permissions
                │
                ▼
Economy ────── Betting ────── Events
   │              │              │
   └──── Transactions ───────────┘
                │
                ▼
          Notifications
```

The primary domain areas are:

1. Server
2. User Account
3. Event
4. Outcome
5. Bet
6. Economy / Balance
7. Transaction
8. Transfer
9. Daily Reward
10. Restrictions
11. Settlement
12. Notifications

---

# 2. Server

A `Server` represents a Discord server using BetBot.

Conceptually:

```text
Server
├── Discord server ID
├── lifecycle state
├── configuration
├── users
├── events
└── transactions
```

Possible lifecycle states:

```text
ACTIVE
ARCHIVED
```

Rules:

* Server IDs are globally unique.
* Server data is isolated from other servers.
* Archived servers retain historical data.
* Re-adding BetBot to an archived server restores access to the existing server data.
* A server cannot be used for normal operations while archived unless the product explicitly restores it.

---

# 3. User Identity

A global user identity represents the Discord account.

The global identity contains information such as:

* Discord user ID
* current Discord display name
* current Discord avatar

Identity information is not the same thing as a BetBot account.

---

# 4. User Account

A `UserAccount` represents a user's BetBot state within one server.

Conceptually:

```text
UserAccount
├── server
├── Discord identity
├── balance
├── betting restriction
├── BetBot ban state
└── account metadata
```

A user may have multiple BetBot accounts:

```text
Discord User
├── Server A → Account A
├── Server B → Account B
└── Server C → Account C
```

Balances and financial history must never cross server boundaries.

---

# 5. User Restrictions

User restrictions are server-specific.

## Betting disabled

Prevents:

* placing bets
* modifying bets

Does not prevent:

* viewing
* rewards
* transfers
* payouts
* refunds

## BetBot banned

Prevents:

* placing bets
* modifying bets
* claiming daily reward
* web access to that server

Does not prevent:

* viewing historical data
* viewing balance
* sending transfers
* receiving transfers
* receiving payouts
* receiving refunds

A ban does not erase or confiscate assets.

---

# 6. Event

An `Event` represents a betting opportunity.

Conceptually:

```text
Event
├── server
├── name
├── description
├── start_at
├── end_at
├── status
├── outcomes
├── creator
├── created_at
├── updated_at
└── settlement/cancellation metadata
```

---

# 7. Event Status

Valid statuses:

```text
SCHEDULED
STARTED
AWAITING_RESULT
SETTLED
CANCELLED
```

Valid transitions:

```text
SCHEDULED
 ├── STARTED
 └── CANCELLED

STARTED
 ├── AWAITING_RESULT
 └── CANCELLED

AWAITING_RESULT
 ├── SETTLED
 └── CANCELLED
```

A settled or cancelled event is terminal.

No transition is allowed from:

```text
SETTLED → anything
CANCELLED → anything
```

unless a future explicitly defined administrative recovery workflow is introduced.

---

# 8. Event Invariants

### Schedule

```text
start_at > now_at_creation
end_at > start_at
```

### Betting

Only `SCHEDULED` events accept new bets.

### Modification

Only bets belonging to `SCHEDULED` events may be modified.

### Existing bets lock event structure

Once an event has at least one bet:

* name is immutable
* description is immutable
* start time is immutable
* end time is immutable
* outcome set is immutable
* outcome ordering is immutable

Odds remain mutable until settlement.

### Settlement

Settlement requires at least one winning outcome.

### Cancellation

Cancellation is allowed before settlement.

---

# 9. Outcome

An `Outcome` represents one possible result of an event.

Conceptually:

```text
Outcome
├── event
├── identifier
├── name
├── display order
└── current odds
```

An event must have at least one outcome.

Outcomes may have more than two choices.

Once bets exist, the outcome set cannot change.

---

# 10. Odds

Odds represent the payout multiplier for an outcome.

Odds:

* are exact decimal values
* support up to three decimal places
* must be valid positive betting odds
* are mutable while the event is unsettled

A bet snapshots the odds at placement time.

Changing current outcome odds never changes historical bet odds.

---

# 11. Bet

A `Bet` represents one user's stake on one event outcome.

Conceptually:

```text
Bet
├── user account
├── event
├── outcome
├── stake
├── odds snapshot
├── potential payout
├── status
├── created_at
└── updated_at
```

The bet must permanently retain the odds used when the stake was created.

---

# 12. Bet Status

Suggested states:

```text
ACTIVE
WON
LOST
REFUNDED
```

A bet may transition:

```text
ACTIVE → WON
ACTIVE → LOST
ACTIVE → REFUNDED
```

Terminal states:

```text
WON
LOST
REFUNDED
```

A bet cannot be processed twice.

---

# 13. Bet Invariants

### Minimum stake

```text
stake >= 0.01
```

### Balance

The user must have enough available balance when increasing or placing a bet.

### Currency precision

Stake uses two decimal places.

### Odds precision

Odds use up to three decimal places.

### Snapshot

Historical odds are immutable.

### Settlement

A settled bet must have exactly one terminal result:

```text
WON
LOST
```

### Cancellation

A cancelled event causes active bets to become:

```text
REFUNDED
```

---

# 14. Bet Modification

A bet can be modified only while its event is `SCHEDULED`.

For an old stake and new stake:

```text
balance_change = old_stake - new_stake
```

Examples:

```text
old = 100.00
new = 150.00

balance change = -50.00
```

The user pays 50 more.

```text
old = 100.00
new = 75.00

balance change = +25.00
```

The user receives 25 back.

The operation must be atomic.

---

# 15. Settlement

A `Settlement` represents the final result processing of an event.

Conceptually:

```text
Settlement
├── event
├── winning outcomes
├── settled by
├── settled at
└── settlement metadata
```

Settlement is immutable.

The event must not be settled more than once.

---

# 16. Winning Outcomes

An event may have multiple winners.

Example:

```text
Event:
A
B
C

Winners:
A
C
```

Every bet whose selected outcome is a winning outcome is treated as a winning bet.

Every other bet loses.

There must be at least one winning outcome.

If there should be no winner, the event must be cancelled instead.

---

# 17. Payout

For a winning bet:

```text
profit = stake × (odds - 1)
total_payout = stake × odds
```

Round the final payout to two decimal places.

Example:

```text
stake = 100.00
odds = 2.555

payout = 255.50
profit = 155.50
```

The payout uses the bet's historical odds snapshot, not the current event odds.

---

# 18. Settlement Atomicity

Settlement is a single financial operation.

Conceptually:

```text
BEGIN TRANSACTION

validate event
validate winners

for each active bet:
    determine win/loss
    calculate payout
    create financial transaction
    update user balance
    mark bet terminal

record settlement
mark event SETTLED

COMMIT
```

If any operation fails:

```text
ROLLBACK
```

No partial settlement is acceptable.

---

# 19. Settlement Idempotency

Settlement must be safe to retry.

A second settlement request must not:

* pay users twice
* create duplicate payout transactions
* process bets twice
* change a terminal bet
* create another settlement

The domain should have a reliable way to detect an already completed settlement.

---

# 20. Economy

The economy consists of:

```text
UserAccount
    │
    ├── current balance
    │
    └── immutable transactions
```

The current balance is an operational representation of the user's available funds.

Transactions explain how the balance changed.

---

# 21. Transaction

A `Transaction` represents an immutable financial change.

Possible types:

```text
STARTING_BALANCE
DAILY_REWARD
BET
PAYOUT
REFUND
TRANSFER
ADMIN_ADJUSTMENT
```

Additional types may be introduced if required by the implementation.

Every balance-changing operation must have an auditable transaction.

---

# 22. Transaction Invariants

Transactions are immutable.

Corrections require additional transactions.

A transaction must:

* belong to a server
* identify the affected account
* contain an exact monetary amount
* contain a transaction type
* contain creation time
* contain sufficient metadata to explain its origin

Financial records must be auditable.

---

# 23. Balance Invariants

```text
balance >= 0
```

Currency must use exact decimal arithmetic.

No operation may commit a negative balance.

All balance-changing operations must be atomic.

---

# 24. Starting Balance

When a BetBot account is initialized:

```text
balance += configured_starting_balance
```

The starting amount is recorded as an immutable transaction.

Default:

```text
50.00
```

---

# 25. Daily Reward

A daily reward is identified by:

```text
server
user account
server-local calendar date
```

A user may receive at most one daily reward for a calendar day.

The operation must be safe under concurrent requests.

The recommended domain invariant is:

```text
unique(server_id, user_account_id, reward_date)
```

The reward transaction and eligibility record must be created atomically.

---

# 26. Transfers

A transfer has:

```text
sender
recipient
server
amount
timestamp
```

A transfer produces linked financial records for both parties.

Conceptually:

```text
Sender:
-amount

Recipient:
+amount
```

The operation must be atomic.

The sender cannot transfer more than their available balance.

Sender and recipient must belong to the same server.

Self-transfers are prohibited.

---

# 27. Admin Balance Adjustments

Administrators may:

* give coins
* remove coins
* set balance

Every adjustment creates an auditable transaction.

### Give

```text
balance += amount
```

### Remove

```text
balance -= amount
```

Removal cannot exceed the current balance.

### Set

Setting a balance does not overwrite history.

Instead:

```text
difference = requested_balance - current_balance
```

The difference becomes an adjustment transaction.

Setting a balance to zero is valid.

---

# 28. Server Configuration

Important server configuration includes:

```text
starting_balance
daily_reward_amount
currency_display
timezone
betting_enabled
notification_channel
```

Fixed product rules include:

```text
minimum_bet = 0.01
minimum_transfer = 0.01
currency_precision = 2
odds_precision = 3
```

These fixed rules should not become configurable without an explicit product decision.

---

# 29. Notifications

Notifications are side effects of domain events.

Examples:

```text
EventStarted
EventEnded
EventSettled
EventCancelled
BetWon
BetLost
BetRefunded
```

Notification delivery must not determine whether the underlying financial operation succeeds.

If notification delivery fails:

```text
financial operation remains successful
```

Notification processing should therefore be decoupled from core financial transactions where practical.

---

# 30. Authorization

Authorization is evaluated in the context of:

```text
Discord identity
+
server membership
+
Discord permissions
+
BetBot account state
+
requested operation
```

The backend must perform authorization checks.

The client cannot grant itself permission.

Administrative operations require current Discord Administrator permission.

---

# 31. Important Domain Invariants

The following invariants are considered critical:

```text
1. No negative balances.

2. Financial operations are atomic.

3. Financial history is immutable.

4. Settlement cannot pay twice.

5. Refunds cannot happen twice.

6. Transfers cannot partially complete.

7. Daily reward cannot be claimed twice for the same server day.

8. Existing bets retain their original odds.

9. Event structure cannot change after bets exist.

10. Betting closes when an event starts.

11. Settled events are immutable.

12. Cancelled events are terminal.

13. BetBot bans do not confiscate balances.

14. Server data cannot cross server boundaries.

15. Discord permissions are verified server-side.

16. Frontend authorization is never trusted.

17. Currency calculations use exact decimal arithmetic.

18. All balance changes have an auditable transaction.

19. Notification failure cannot corrupt core business operations.

20. Existing payouts/refunds continue even if a user becomes banned.
```

---

# 32. Domain Design Principle

The domain layer should contain the important business rules.

Discord handlers, HTTP handlers, UI components, background jobs, and other infrastructure must not independently implement competing versions of these rules.

A request coming from Discord and the equivalent request coming from the web should ultimately use the same domain/application behavior.

The goal is:

```text
Discord ─┐
         ├── Application/Domain ── Economy
Web ─────┘                       ├─ Events
                                 ├─ Bets
                                 ├─ Users
                                 └─ Transactions
```

Business rules should not be duplicated between clients.
