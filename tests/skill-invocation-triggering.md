# Regression test: Skill invocation and triggering

## Scenario
The bridge Skill is installed in a Claude Code-compatible host. Start a fresh session and issue a non-trivial task involving runtime ambiguity, browser/CLI routing, missing integrations, or verification.

## Required behavior

1. The Skill description clearly names the situations where the bridge is useful.
2. The Skill remains eligible for automatic model invocation.
3. The bridge is not marked `disable-model-invocation: true`.
4. A fresh-session test distinguishes Skill availability from actual invocation.
5. A listing/availability signal is never treated as proof that the Skill was used.
6. `/skill-doctor` or trace evidence is treated as supplementary invocation evidence when available.

## Failure signatures

Fail the test if:

- the Skill is disabled from automatic model invocation;
- its trigger description omits runtime/capability/tool-routing use cases;
- a test claims success merely because the Skill appears in a listing;
- stale context from an earlier run is used as proof of fresh-session invocation;
- invocation is confused with successful task execution.
