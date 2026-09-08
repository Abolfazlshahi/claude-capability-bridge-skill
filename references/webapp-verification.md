# Web App Verification Playbook

This is the canonical end-to-end workflow for the common task: build/fix a web application and prove that the resulting application actually works.

## Definition of done

A web app task is complete only when:

- relevant source changes are present;
- the app starts or builds successfully in the target environment;
- required routes/pages render;
- critical user journeys work;
- relevant deterministic checks pass;
- relevant browser/runtime errors were examined;
- no claim exceeds the evidence collected.

## Phase 0 — Understand

Extract acceptance criteria from the user request. Separate implementation, visual, behavioral, data/API, and environment requirements. Choose reasonable defaults for genuinely unspecified details and report those assumptions when they materially affect verification.

## Phase 1 — Inspect

Inspect the project before changing it. Determine framework/runtime, package manager, entry points, scripts, environment variables, build/test commands, dev-server command, expected ports, host binding, existing tests, and generated directories. Prefer project-declared commands over remembered framework conventions.

## Phase 2 — Baseline

Before making changes when practical, run the cheapest useful baseline: tests, type checking, lint, build/compile, and application startup. Record pre-existing failures so they are not incorrectly attributed to the current change.

## Phase 3 — Implement

Make the smallest coherent change that satisfies the request. Preserve existing architecture and conventions unless refactoring is requested. For UI work, use short edit → verify cycles rather than one giant unverified rewrite.

## Phase 4 — Launch

Start the application using the declared development or preview command. Track command, working directory, PID, stdout/stderr, port, and URL when available. A live process is not proof of readiness.

## Phase 5 — Open and inspect

Open the actual server URL using the best available browser. Inspect route/title, major regions, loading state, missing assets, obvious runtime errors, layout issues, and initial API failures.

## Phase 6 — Critical-path tests

Create a minimal journey set from the request. For a typical dashboard:

```text
load dashboard
→ verify navigation
→ open primary page
→ interact with primary control
→ submit/finalize action
→ verify resulting state
→ navigate back/forward if relevant
```

Do not test only whether a button exists. Test the state transition the control is meant to cause.

## Phase 7 — Diagnostics

When a journey fails, gather the smallest useful evidence set:

```text
visible UI
→ current URL/state
→ console error
→ failed network request
→ server log
→ source location
```

Classify the failure before changing code.

## Phase 8 — Repair loop

```text
FAIL
↓
REPRODUCE
↓
LOCALIZE
↓
PATCH
↓
RELOAD/RESTART ONLY AS NECESSARY
↓
RE-RUN FAILED ASSERTION
↓
RE-RUN RELATED CRITICAL PATHS
```

Do not declare success merely because an error disappeared. Re-run the user-visible assertion.

## Phase 9 — Deterministic checks

Run available automated checks after browser verification: unit/integration tests, type checker, linter, production build, API smoke tests, and project-specific validation. Browser verification and deterministic checks complement rather than replace each other.

## Phase 10 — Visual review

When visual fidelity matters, inspect relevant viewports for clipping/overflow, horizontal scrolling, alignment, spacing, hierarchy, typography, responsive breakpoints, fixed overlays, loading/error states, and readability. Use native screenshots or visual inspection when available.

## Phase 11 — Cleanup

Stop processes started by the agent when safe and appropriate. Never terminate an unrelated service merely because it uses a common port. Remove temporary test artifacts unless requested otherwise.

## Evidence ledger

| Criterion | Evidence | Status |
|---|---|---|
| App starts | readiness + actual URL | PASS/FAIL |
| Route renders | observed route/page | PASS/FAIL |
| Primary journey | observed state transition | PASS/FAIL |
| Network/API health | relevant requests | PASS/FAIL |
| Automated checks | command result | PASS/FAIL |
| Visual requirement | screenshot/inspection | PASS/FAIL |

## Anti-patterns

**Build succeeded, so it works:** build proves compilation/bundling, not runtime behavior.

**Page loaded, so feature works:** critical interactions can still be broken.

**No console errors, so correct:** behavior can be wrong without throwing.

**Port is probably 3000:** use the actual reported/discovered URL.

**Just retry:** re-observe and change the failed variable or tool path.

**Browser unavailable, pretend:** never fabricate verification; report the missing capability.