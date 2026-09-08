# Verification and Evidence

## Core rule

Verification is an evidence problem. A successful tool invocation only proves that the invocation completed according to the tool's own contract.

## Evidence hierarchy

Prefer evidence from strongest to weakest:

1. direct observed state matching acceptance criteria;
2. deterministic test/assertion result;
3. structured tool read-back confirming state;
4. logs/telemetry consistent with success;
5. indirect inference.

Use the strongest available evidence and label uncertainty.

## Acceptance criteria

Translate each requirement into an observable assertion:

```text
Requirement
→ Observable state
→ Tool/action needed
→ Evidence
→ PASS/FAIL/UNKNOWN
```

Example:

```text
Requirement: user can submit the form
Observable state: successful request + confirmation state
Evidence: browser interaction and response/visible confirmation
```

## Verification levels

### L0 — syntactic
Code parses or command is accepted.

### L1 — deterministic
Tests/build/type/lint checks pass.

### L2 — runtime
Application starts and required services respond.

### L3 — user-facing
Critical user journey works through the actual interface.

### L4 — visual
Relevant appearance/layout requirements are directly inspected.

### L5 — integrated
External dependencies, persistence, or multi-system side effects are verified.

Do not report an L1 result as L3 or higher.

## Regression scope

After a fix, always re-run:

- the failed assertion;
- closely related paths;
- the cheapest high-value deterministic checks.

Broaden to the full suite when practical or when the change has wide impact.

## Negative evidence

A failed check is evidence even when the task later succeeds. Preserve enough information to know whether a failure was fixed, pre-existing, flaky, or environmental.

## Final status vocabulary

Use:

- **VERIFIED** — directly tested against the relevant criterion.
- **PARTIALLY VERIFIED** — some but not all evidence collected.
- **BLOCKED** — required capability/environment unavailable.
- **UNKNOWN** — insufficient evidence.
- **FAILED** — criterion tested and did not pass.

Avoid "works" or "done" when a more precise status is possible.
