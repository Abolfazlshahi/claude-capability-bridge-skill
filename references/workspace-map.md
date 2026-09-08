# Claude Desktop Mental Model

The goal is to help a custom model reason about the host as a layered environment rather than as one giant "Claude" capability.

## Layer 0 — Conversation

The conversation contains user intent, constraints, prior observations, and model-generated plans. Conversation text is not proof that a tool action occurred.

## Layer 1 — Skill policy

A Skill supplies reusable procedural knowledge, references, assets, and scripts. It influences planning and execution behavior but cannot silently add a tool to the runtime.

## Layer 2 — Agent runtime

The host determines which tools are exposed, how calls are dispatched, what approvals are required, what context is injected, and what execution surfaces exist.

## Layer 3 — Tool surfaces

Common surfaces include:

- filesystem/project files;
- shell/code execution;
- browser automation;
- existing Chrome/browser session;
- computer/desktop control;
- MCP tools/resources/prompts;
- connectors;
- Git/version control;
- scheduling/remote dispatch;
- specialized application integrations.

## Layer 4 — Environment

The underlying machine and services contain the actual state:

```text
OS
filesystem
process table
network
localhost services
browser profile
cookies/session
desktop applications
repositories
remote APIs
```

## Workspace truth model

Treat the following as separate truth domains:

| Domain | What it proves |
|---|---|
| Project knowledge | Information loaded into project context |
| Filesystem | Actual files reachable by the current filesystem tool |
| Git | Repository history/status visible through Git |
| Process state | Processes actually started/running |
| Browser state | What the selected browser currently exposes |
| MCP/connector state | Results returned by external integration |
| Conversation | Claims, instructions, and prior reasoning |

Example: seeing `README.md` in project knowledge does not prove the same file is writable on disk.

## Current-session capability ledger

Use a compact internal table:

```text
Capability | Evidence | Permission | Preferred use | Fallback
```

Evidence should point to the tool/runtime observation that established availability.

## State transitions

A model should think in transitions, not only actions:

```text
unknown workspace
    ↓ inspect
known workspace
    ↓ run command
process created
    ↓ readiness check
service ready
    ↓ browser open
page loaded
    ↓ critical action
state changed
    ↓ assertion
verified
```

Each arrow is an opportunity to observe and recover.

## Browser state is independent

A local development server can be healthy while the browser is stale, authenticated to a different account, on the wrong route, or blocked by a client-side error. Always re-observe browser state after meaningful changes.

## Process ownership

Record processes started by the agent whenever the host exposes PIDs or equivalent handles. Cleanup should target those owned processes, not arbitrary processes sharing a port or name.
