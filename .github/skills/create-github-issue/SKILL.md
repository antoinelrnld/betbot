---
name: create-github-issue
description: Create a complete, implementation-ready GitHub issue for BetBot. Use when asked to create, refine, or improve a GitHub issue.
---

# Create GitHub Issue

Create GitHub issues that are clear enough for another engineer or GitHub Copilot to implement without guessing product behavior.

## Source of truth

Before writing the issue, consult:

* `docs/product.md`
* `docs/domain.md`
* existing architecture documentation
* related GitHub issues when available

Do not invent product requirements that conflict with these documents.

---

## Issue structure

Use this structure when applicable:

# Title

Use an action-oriented title.

Prefer:

```text
Add an end date to admin-created events
```

over vague titles such as:

```text
Event changes
```

---

## Context

Explain why the change is needed.

Keep this focused on the product problem.

---

## Problem

Describe the current limitation or missing behavior.

---

## Goal

State the desired result.

---

## Non-goals

Explicitly identify behavior that is intentionally outside the issue.

This prevents scope creep.

---

## Functional Requirements

Describe user-visible behavior.

Use precise language.

Avoid implementation details unless they are required.

---

## Technical Requirements

Include implementation constraints that matter for correctness.

Examples:

* server-side validation
* atomic database operation
* migration requirement
* idempotency
* authorization
* decimal arithmetic
* server isolation

Do not prescribe implementation details unnecessarily.

---

## Acceptance Criteria

Write objective criteria that can be verified.

Prefer:

```text
- [ ] An administrator can...
- [ ] A non-administrator cannot...
- [ ] The backend rejects...
- [ ] Existing bets remain...
```

over subjective criteria such as:

```text
- [ ] Make the UI nice
```

---

## Edge Cases

Include meaningful edge cases.

For BetBot, consider:

* event lifecycle boundaries
* zero balance
* concurrent requests
* retries
* server isolation
* user restrictions
* missing Discord permissions
* deleted Discord resources
* existing bets
* historical data

Only include relevant cases.

---

## Testing Requirements

Specify important behavior that must be tested.

Focus on:

* business rules
* authorization
* financial correctness
* lifecycle transitions
* concurrency
* regression behavior

---

## Dependencies

List known dependencies on:

* previous issues
* migrations
* architecture decisions
* external integrations

---

## Implementation Notes

Only include implementation guidance when it reduces ambiguity.

Do not prescribe a technology merely because it is familiar.

---

## Quality requirements

Every issue should be:

* specific
* independently understandable
* testable
* scoped
* consistent with product/domain documentation
* explicit about edge cases

Avoid combining unrelated features into one issue.

---

## Final check

Before producing the issue, verify:

1. Could an engineer understand the intended behavior?
2. Are acceptance criteria objectively testable?
3. Are authorization rules explicit?
4. Are financial invariants explicit when relevant?
5. Are important edge cases covered?
6. Is the scope clear?
7. Are non-goals identified?
8. Does it conflict with existing product documentation?

If an important product decision is unresolved, identify it instead of inventing an answer.
