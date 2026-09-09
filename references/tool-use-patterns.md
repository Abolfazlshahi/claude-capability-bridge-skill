# Tool Use Patterns

This document teaches procedural tool use without assuming Anthropic-specific hidden behavior. Adapt every pattern to the actual schema exposed by the host.

## General call contract

Before a consequential tool call:

1. Identify the intended outcome.
2. Identify the capability family required (files, shell/process, browser, computer use, MCP/connector, Git, artifact, project, etc.).
3. Confirm the tool exists and is appropriate.
4. Read the schema/description enough to supply valid arguments.
5. Keep arguments minimal and explicit.
6. Call once.
7. Inspect the returned result.
8. Decide the next action from evidence.

Never batch unrelated high-impact actions merely to reduce tool-call count.

## Capability-trigger questions

Do not select a tool merely because its name looks relevant. Ask the smallest set of routing questions first:

```text
What state must change?
Where does that state live?
Which interface is the authoritative way to change it?
What evidence will prove the change?
```

Examples:

| Task signal | Preferred first consideration |
|---|---|
| inspect/edit repository files | filesystem/file-edit interface |
| run tests/build/start a server | shell/code/process interface |
| inspect a rendered website | browser interface |
| interact with an application whose UI is itself the target | computer use / GUI surface |
| update a remote record/service with a structured API | MCP/connector/tool interface |
| inspect version history or branch state | Git interface |
| create a user-facing generated deliverable | artifact/document/file surface |
| work with project-scoped instructions/knowledge | project context |

These are routing triggers, not hard-coded tool names. The runtime's actual exposed surface always wins.

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
execution model known
→ actual URL/state
→ action
→ resulting page/state
→ assertion
```

A browser is an observation and interaction surface, not a substitute for determining how the target application executes. For server-backed projects, use the real served route rather than a source/template file. Use `references/project-recognition-and-launch.md` and `references/webapp-verification.md` when relevant.

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
