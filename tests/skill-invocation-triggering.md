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
7. When the Claude Code bootstrap plugin is installed, `SessionStart` establishes the protocol and `UserPromptSubmit` re-injects a compact reminder before each turn.
8. `PostToolUseFailure` re-injects recovery guidance after a failed tool call so the model is reminded to classify and recover instead of stopping at a generic error.
9. The per-turn and failure bootstraps are treated as context reinforcement, not as proof that the Skill body loaded or that the task succeeded.
10. Tests also cover the failure mode where a model forgets the Skill mid-session: with the bootstrap active, the prompt still receives the bridge operating reminder before processing and a failed tool call receives recovery guidance afterward.

## Failure signatures

Fail the test if:

- the Skill is disabled from automatic model invocation;
- its trigger description omits runtime/capability/tool-routing use cases;
- a test claims success merely because the Skill appears in a listing;
- stale context from an earlier run is used as proof of fresh-session invocation;
- invocation is confused with successful task execution;
- the plugin omits the per-turn `UserPromptSubmit` reinforcement;
- the plugin omits the `PostToolUseFailure` recovery reinforcement;
- the bootstrap is described as granting tools, fixing provider incompatibility, or otherwise creating capabilities it cannot create.

## Verification notes

Use Claude Code hook debug output or an equivalent host trace to confirm that `UserPromptSubmit` and `PostToolUseFailure` fired and their `additionalContext` reached the model. Keep this separate from evidence that the Skill itself was invoked. The questions are:

```text
DID THE BRIDGE PROCEDURE GET INTO CONTEXT?
DID THE FAILURE RECOVERY PROCEDURE GET INTO CONTEXT?
DID THE MODEL ACTUALLY FOLLOW THEM?
```
