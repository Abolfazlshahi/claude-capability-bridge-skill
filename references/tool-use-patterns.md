# Tool Use Patterns

This document teaches procedural tool use without assuming Anthropic-specific hidden behavior. Adapt every pattern to the actual schema exposed by the host.

## General call contract

Before a consequential tool call:

1. Identify the intended outcome.
2. Confirm the tool exists and is appropriate.
3. Read the schema/description enough to supply valid arguments.
4. Keep arguments minimal and explicit.
5. Call once.
6. Inspect the returned result.
7. Decide the next action from evidence.

Never batch unrelated high-impact actions merely to reduce tool-call count.

## Observation hierarchy

Prefer observations in this order when available:

```text
structured return
    > deterministic command output
    > browser DOM/state
    > screenshot/visual state
    > inferred state
```

Inferences are useful for planning but must not be reported as observations.

## Idempotence heuristic

Before repeating a call, classify it:

- read-only / idempotent: safe to repeat when useful;
- reversible mutation: repeat only after confirming current state;
- destructive or externally consequential: stop and require appropriate authorization/confirmation.

## Files

For file edits:

```text
locate → read relevant range → understand invariants → edit → inspect diff → validate
```

Do not replace a whole file when a small patch satisfies the request unless the task explicitly requires a rewrite.

## Shell / execution

For command execution:

```text
cwd → command → stdout/stderr → exit code → side effects → next step
```

Avoid shell commands whose meaning depends on an unstated cwd, shell, OS, or environment variable.

For long-running servers, distinguish:

```text
process created
≠
server listening
≠
application healthy
```

## Browser

For browser actions:

```text
current page/state
→ action
→ resulting page/state
→ assertion
```

Use stable semantic targets where the tool offers them. Avoid brittle coordinate-only automation when structured selectors or accessible labels are available.

## Computer control

For screen actions:

```text
observe screen
→ act once or in a short sequence
→ observe again
```

Do not assume a window remained focused after an action that could change application state.

## MCP / connectors

Treat each tool as its own API contract. Tool names may be descriptive but are not guarantees of side effects. Read descriptions, required fields, return values, and error semantics when available.

Prefer direct structured calls over browser emulation for the same operation.

## Tool errors

A tool error is evidence, not merely an invitation to retry. Extract:

- error class;
- argument that failed;
- permission issue;
- transient vs deterministic nature;
- possible alternative path.

Then change the relevant variable before trying again.

## Unknown tool semantics

When a custom provider exposes an unfamiliar tool:

1. inspect name and description;
2. inspect input schema;
3. make the smallest safe read-only call that can establish semantics;
4. inspect result;
5. only then use it for mutation.

Never invent argument names from similar tools.
