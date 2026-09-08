---
applyTo: "frontend/**"
---

# BetBot Frontend Instructions

The web application is a first-class BetBot client.

It must provide the same core functionality as Discord while providing a responsive, mobile-friendly experience.

## Core Principle

The frontend is responsible for:

* presentation
* interaction
* client-side UX
* loading/error states
* optimistic behavior only where safe
* communicating with the backend

The frontend is NOT responsible for authoritative business rules.

## Backend Authority

Never assume an operation is valid because the UI allows it.

The backend must validate:

* authentication
* authorization
* server membership
* BetBot restrictions
* event state
* balances
* betting rules
* transfers
* administrative permissions

Frontend validation exists for user experience, not security.

## Server Context

Users may belong to multiple BetBot-enabled Discord servers.

The UI must always make the active server context clear.

Never accidentally display or mutate data from another server.

Server switching should reset or revalidate server-scoped data appropriately.

## Responsive Design

Mobile is a first-class target.

Do not design desktop-only workflows and attempt to make them responsive later.

Important workflows must remain usable on small screens:

* event browsing
* event details
* placing bets
* modifying bets
* daily reward
* transfers
* transaction history
* administrator event creation
* administrator settlement
* user management

## UX

BetBot should feel simple and fast.

Avoid unnecessary:

* confirmation dialogs
* multi-page navigation
* repeated data entry
* technical terminology
* excessive configuration

Use clear feedback for:

* success
* validation errors
* unavailable actions
* loading
* permission errors
* stale data
* server changes

## Event UI

Event pages should clearly communicate:

* event state
* start/end time
* betting availability
* outcomes
* current odds
* user's bets
* total wagered
* relevant restrictions

Do not display outdated odds or betting availability as though they are authoritative.

## Real-Time Data

The UI should react to relevant server changes such as:

* event status
* odds
* balance
* settlement
* cancellation
* bet changes

The backend remains authoritative when local state conflicts with server state.

## Accessibility

Use semantic controls and accessible interaction patterns.

Important actions must be usable without relying solely on:

* color
* hover
* animation
* tiny click targets

Forms should have meaningful labels and accessible validation.

## Error Handling

User-facing errors should explain what happened and, where appropriate, what the user can do next.

Do not expose stack traces, internal identifiers, or implementation details.

## State Management

Use the simplest state-management approach that fits the selected frontend stack.

Avoid introducing global state merely because a component has several related values.

Server state and UI state should be conceptually separated where practical.

## Testing

Test important user workflows and business-rule boundaries.

Particularly important:

* event browsing
* bet placement
* bet modification
* unavailable betting
* server switching
* daily reward
* transfers
* administrator workflows
* settlement UI
* error states
* responsive-critical interactions
