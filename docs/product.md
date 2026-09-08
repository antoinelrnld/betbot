# BetBot Product Specification

## 1. Product Overview

BetBot is a Discord-first virtual betting platform that allows users in Discord servers to wager virtual currency on events.

BetBot has two first-class interfaces:

* Discord
* Web

Both interfaces provide access to the same underlying BetBot functionality and business rules.

BetBot is **not a real-money gambling platform**. All currency is virtual and has no monetary value.

The product is designed around three principles:

1. Extremely simple user experience.
2. Strong server-side enforcement of business rules.
3. Consistent behavior across Discord and web.

---

## 2. Users and Servers

BetBot operates within Discord servers.

Each Discord server has its own isolated BetBot environment, including:

* events
* users/accounts
* balances
* bets
* transactions
* configuration
* bans
* betting restrictions

A user's BetBot account is therefore **server-scoped** even though their identity comes from their global Discord account.

### Server lifecycle

When BetBot is added to a Discord server:

1. The server is initialized automatically.
2. Server-specific configuration is created using defaults.
3. User accounts are created lazily when users first interact with BetBot.

When BetBot is removed from a server:

* The server is archived.
* Existing data is preserved.
* Historical data is not deleted.

If BetBot is later added to the same server again:

* The existing server data becomes available again.

---

## 3. Authentication

Discord is the sole identity provider.

There are no separate BetBot usernames or passwords.

The web application uses Discord OAuth authentication.

Discord is the source of truth for:

* user identity
* Discord display name
* Discord avatar
* server membership
* Discord Administrator permission

BetBot is the source of truth for:

* BetBot account state
* balance
* bets
* transactions
* BetBot bans
* betting restrictions
* server configuration

The backend must always verify authorization. Frontend visibility is never considered an authorization mechanism.

---

## 4. Server Access

A user must currently be a member of a Discord server to access that server through the web application.

BetBot must currently be installed in the server.

Leaving a server does not delete the user's BetBot account or history.

If the user later rejoins the server, their previous BetBot account and history become available again.

A Discord kick or Discord ban does not automatically create a BetBot ban.

---

# 5. Events

Events are the central betting object.

Events are server-specific and initially generic rather than tied to a particular sport or event provider.

An event contains:

* name
* description
* start date/time
* end date/time
* status
* one or more outcomes
* odds for each outcome
* creation metadata
* settlement/cancellation metadata as appropriate

Events may contain more than two outcomes.

---

## 5.1 Event lifecycle

The event lifecycle is:

```text
SCHEDULED
    ↓
STARTED
    ↓
AWAITING_RESULT
    ↓
SETTLED

SCHEDULED / STARTED / AWAITING_RESULT
    ↓
CANCELLED
```

### SCHEDULED

The event has been created and betting is available.

### STARTED

The event's start time has been reached.

At this point:

* betting closes
* new bets are rejected
* existing bets cannot be modified
* event details remain viewable

### AWAITING_RESULT

The event's end time has been reached.

The event is waiting for an administrator to determine the result.

The result is **never automatically determined**.

An event may remain in this state indefinitely until an administrator settles or cancels it.

### SETTLED

The result has been determined and all bets have been processed.

Settlement is immutable.

### CANCELLED

The event will not produce a result.

All bets are fully refunded.

Cancelled events remain available in historical views.

---

## 5.2 Event creation

Only Discord server administrators may create events.

Administrator status is determined using the user's current Discord Administrator permission.

There is no separate BetBot administrator role system in v1.

Event creation is a multi-step process.

### Discord

The intended flow is:

```text
Basic information
→ Schedule
→ Outcomes
→ Odds
→ Review
→ Create
```

### Web

The intended wizard is:

```text
1. Basic information
2. Schedule
3. Outcomes
4. Odds
5. Review & create
```

Start and end date/time must use an appropriate picker-based UI for a smooth user experience.

The start date may not be in the past.

The end date must be after the start date.

Betting becomes available immediately after event creation.

---

## 5.3 Event editing

Before any bets exist, administrators may edit:

* name
* description
* start date/time
* end date/time
* outcomes
* odds

Once at least one bet exists:

* name cannot change
* description cannot change
* start date/time cannot change
* end date/time cannot change
* outcomes cannot be added
* outcomes cannot be removed
* outcomes cannot be reordered
* odds may still be changed

Odds may be changed until the event is settled.

Changing odds does not modify existing bets.

Existing bets permanently retain the odds that were active when the bet was placed.

---

## 5.4 Event cancellation

An administrator may cancel an event at any time before settlement.

Cancellation is allowed while the event is:

* SCHEDULED
* STARTED
* AWAITING_RESULT

Cancellation is not allowed after settlement.

When an event is cancelled:

* every bet is fully refunded
* refund amount equals the final stake of that bet
* no profit is paid
* no winnings are generated
* refunds are recorded in the transaction ledger
* users receive appropriate refund notifications
* the event remains in history

Refund processing must be atomic and idempotent.

A refund must never be issued twice.

---

# 6. Settlement

Only administrators may settle events.

An administrator selects one or more winning outcomes.

At least one winning outcome must be selected.

If no outcome should win, the event must be cancelled instead.

Losing bets receive:

```text
0 payout
```

Winning bets receive a payout according to the odds snapshot stored on the bet.

Settlement must:

1. validate the event
2. validate the selected winners
3. calculate payouts
4. process all affected bets
5. create financial ledger transactions
6. update balances
7. mark bets as settled
8. mark the event as settled

All settlement operations must occur atomically.

If any part fails, the entire settlement must roll back.

Settlement must be retry-safe and idempotent.

A retry must never result in duplicate payouts.

---

## 6.1 Automatic settlement with no bets

When an event reaches its end time:

* if it has bets, it becomes `AWAITING_RESULT`
* if it has no bets, it is automatically settled

An event with no bets requires no administrator result selection because there are no financial consequences.

---

## 6.2 Settlement review

Before settlement, administrators should be shown a review containing:

* event information
* selected winning outcomes
* all outcomes
* current odds
* number of bets
* total stake per outcome
* affected users
* estimated payouts
* expected winners

After settlement, administrators should be able to inspect a complete settlement breakdown, including individual bets and payouts.

Users should be able to see:

* winning outcome(s)
* their own bets
* payout for each winning bet
* profit/loss
* updated balance
* settlement time

---

# 7. Betting

Users can place bets on available event outcomes.

The backend is responsible for enforcing all betting rules.

The frontend and Discord client must never be trusted to enforce business rules independently.

---

## 7.1 Betting availability

Betting is allowed only while an event is `SCHEDULED`.

Betting is not allowed when an event is:

* STARTED
* AWAITING_RESULT
* SETTLED
* CANCELLED

A server-wide betting-disabled setting also prevents new bets and bet modifications.

---

## 7.2 Bet limits

Minimum bet:

```text
0.01 coin
```

There is no configurable maximum bet.

The maximum practical bet is the user's available balance.

Negative balances are never permitted.

---

## 7.3 Multiple bets

Users may:

* place multiple bets on the same event
* place multiple bets on the same outcome
* bet on multiple outcomes within the same event
* place opposing bets within the same event

There is no requirement that a user have only one bet per event.

---

## 7.4 Bet odds snapshot

When a bet is placed, the bet permanently stores:

* event
* selected outcome
* stake
* odds at placement
* potential payout
* creation timestamp
* status

Changing event odds later does not affect existing bets.

---

## 7.5 Bet placement

When a bet is placed:

1. Validate user permissions.
2. Validate event state.
3. Validate outcome.
4. Validate stake.
5. Validate sufficient balance.
6. Snapshot current odds.
7. Deduct stake.
8. Create the bet.
9. Create the corresponding financial transaction.

The operation must be atomic.

The user must never end up with a deducted balance but no corresponding bet.

---

## 7.6 Bet modification

A user may modify an existing bet only while the event is `SCHEDULED`.

Once the event starts, modification is rejected.

The user may increase or decrease the stake.

The balance adjustment is:

```text
balance_change = old_stake - new_stake
```

Therefore:

* increasing the stake deducts the difference
* decreasing the stake refunds the difference

The modified bet keeps the same original odds snapshot unless the product explicitly introduces a new bet revision model later.

---

# 8. Economy

BetBot uses a virtual currency.

Currency has no real-world monetary value.

The economy is isolated per Discord server.

---

## 8.1 Balance

Each user has a server-specific BetBot balance.

Balances:

* may be zero
* may never be negative
* are represented using exact decimal arithmetic
* use two decimal places

The default starting balance is:

```text
50.00
```

The starting balance is configurable per server.

---

## 8.2 Daily reward

Users may claim one fixed daily reward per server calendar day.

Default reward:

```text
10.00
```

The amount is configurable per server.

The reset is based on the server's configured timezone.

A newly created account is immediately eligible.

Missed rewards do not accumulate.

A user can claim at most once per server calendar day.

Concurrent claims must be idempotent.

BetBot-banned users cannot claim the daily reward.

Users whose betting ability is disabled may still claim the daily reward.

The claim result is shown directly to the user.

---

## 8.3 Payouts

For a winning bet:

```text
profit = stake × (odds - 1)
total_payout = stake × odds
```

Payouts are rounded to two decimal places.

Example:

```text
stake = 200.00
odds = 2.500

profit = 300.00
payout = 500.00
```

Odds support up to three decimal places.

---

## 8.4 Financial precision

Currency calculations must not use binary floating-point arithmetic.

Use exact decimal arithmetic.

Currency:

```text
2 decimal places
```

Odds:

```text
up to 3 decimal places
```

Payouts:

```text
2 decimal places
```

---

# 9. Transaction Ledger

Financial history is immutable.

Every balance-changing operation must be explainable through the transaction ledger.

Possible transaction types include:

* starting balance
* daily reward
* bet
* payout
* refund
* transfer
* administrator adjustment

Balances may be stored or cached for efficient access, but the ledger remains the authoritative explanation of balance changes.

Corrections must be represented as new transactions.

Existing financial transactions must not be silently overwritten.

---

# 10. Transfers

Users may transfer virtual currency to other users within the same Discord server.

Minimum transfer:

```text
0.01 coin
```

Maximum transfer:

```text
entire available balance
```

Self-transfers are prohibited.

Sender and recipient must:

* belong to the same Discord server
* have active BetBot accounts
* not be BetBot-banned

Betting-disabled users may send and receive transfers.

BetBot-banned users may send and receive transfers.

Transfers are permanent and cannot be reversed by users.

Both sender and recipient must receive corresponding transaction history entries.

Transfers must be atomic:

```text
BEGIN
→ validate sender
→ validate recipient
→ validate balance
→ subtract sender
→ add recipient
→ create linked ledger entries
COMMIT
```

Partial transfers are never allowed.

---

# 11. Administration

Administrators are Discord users with the native Discord `Administrator` permission.

Administrator status must be verified server-side.

Administrators remain normal users and retain all standard user functionality.

Administrative functionality is additive.

Administrators can:

### Events

* create events
* edit events subject to lifecycle rules
* change odds
* cancel events
* settle events
* view event status
* view bets
* view settlement information
* archive events

### Economy

* view balances
* give coins
* remove coins
* set balances
* view transaction history

### Users

* view server users
* view betting history
* view transaction history
* disable betting for users
* BetBot-ban users
* unban users

### Server

* configure server settings
* configure currency display
* configure timezone
* configure daily reward
* configure starting balance
* configure notifications
* enable/disable server-wide betting

---

# 12. User Restrictions

BetBot has two distinct user-level restrictions.

## 12.1 Betting disabled

A betting-disabled user:

* cannot place bets
* cannot modify bets

They can still:

* view events
* view existing bets
* view balance
* view history
* claim daily reward
* transfer coins
* receive transfers
* receive winnings
* receive refunds

---

## 12.2 BetBot banned

A BetBot-banned user cannot perform new gameplay/reward actions.

They can:

* view events
* view balance
* view betting history
* view transaction history
* view existing bets
* send transfers
* receive transfers
* receive winnings
* receive refunds
* access personal settings

They cannot:

* place new bets
* modify existing bets
* claim daily reward
* access the BetBot web application for that server

A BetBot ban does not:

* confiscate balance
* delete history
* invalidate existing bets
* prevent pending winnings
* prevent pending refunds

Existing financial obligations continue normally.

A BetBot ban is separate from Discord membership and Discord bans.

---

# 13. Web Application

The web application is a first-class BetBot client.

It is not merely an administration panel.

Standard users can perform normal BetBot actions.

Administrators can perform all applicable administrative actions.

The web application is responsive and mobile-friendly from the beginning.

---

## 13.1 Web navigation

Standard navigation:

```text
Home
Events
Balance
History
Transfer
Settings
```

Administrator navigation adds:

```text
Manage Events
Economy
Users
Server
```

---

## 13.2 Dashboard

The dashboard should provide:

* current balance
* active bets
* upcoming events
* recent wins/losses
* recent transactions
* daily reward availability

---

## 13.3 Event experience

The event page displays:

* name
* description
* start date/time
* end date/time
* status
* all outcomes
* current odds
* user's existing bets
* total amount wagered by the user
* whether betting is currently available

Users can place and modify bets directly from the event page.

---

## 13.4 Administrator event wizard

Administrators create events through:

```text
Basic information
→ Schedule
→ Outcomes
→ Odds
→ Review & create
```

The web schedule step must use a picker-based date/time experience.

---

# 14. Discord Experience

BetBot must be extremely simple to use from Discord.

The interaction model is hybrid:

* slash commands
* buttons
* select menus
* modals
* interactive menus

The main entry point is:

```text
/betbot
```

The home menu conceptually contains:

```text
🎰 BetBot
────────────────────────
Balance: 500 coins

[🎯 Events]
[💰 Balance]
[🎁 Daily Reward]
[📜 History]
[💸 Transfer]
[❓ Help]
```

Direct subcommands are also supported:

```text
/betbot events
/betbot balance
/betbot daily
/betbot history
/betbot transfer
```

Administrators additionally see:

```text
──────── Administration ────────

[🎯 Manage Events]
[💰 Manage Economy]
[👥 Manage Users]
[⚙️ Server Settings]
```

---

# 15. Notifications

The server notification channel is configurable.

BetBot sends server notifications for:

* event start
* event end
* settlement/result
* cancellation

Users receive user-specific notifications for:

* winning bets
* losing bets
* refunds

Notification failures must never break betting, settlement, transfers, or the economy.

If the configured notification channel is deleted:

* notifications are automatically disabled for that server
* BetBot continues operating normally

The exact user notification transport may be finalized during architecture/design.

---

# 16. Real-Time Updates

The web application must provide real-time updates for important state changes, including:

* event status
* odds
* balances
* cancellations
* settlements
* relevant bet changes

The exact transport mechanism is an architectural decision.

The product requirement is real-time behavior, not a specific technology.

---

# 17. Time Handling

All timestamps are stored internally in UTC.

Server configuration contains a timezone.

User-facing dates/times are displayed using the appropriate configured timezone.

Daily rewards use the server's configured calendar day.

Event scheduling uses absolute timestamps.

---

# 18. Data Retention

Financial and betting history must be preserved.

User deletion requests must not destroy required financial records.

Where appropriate, user information should be anonymized while retaining required historical financial data.

Events should be archived rather than hard-deleted when historical records must be preserved.

---

# 19. Core Product Principles

### Server-side enforcement

Business rules must be enforced by the backend.

### Atomic financial operations

Balance-changing operations must be atomic.

### Immutable financial history

Financial history must never be silently rewritten.

### Server isolation

Users, balances, events, bets, transactions, restrictions, and settings are isolated per Discord server.

### Discord identity

Discord is the identity provider and source of truth for Discord permissions and membership.

### Consistent clients

Discord and web clients use the same underlying business rules.

### Simple UX

BetBot should minimize unnecessary steps and confirmations.

### Production quality

The system should be designed for reliability, observability, security, maintainability, and safe failure handling from the beginning.
