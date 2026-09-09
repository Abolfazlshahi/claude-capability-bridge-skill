# Capability Model

## Purpose

Claude Desktop-like agent systems combine distinct layers. Keep them separate when reasoning about a custom provider.

### Layer A — Model cognition
The model supplies planning, reasoning, tool-choice judgment, interpretation of tool results, and procedural habits learned during training or supplied in context.

### Layer B — Agent runtime
The host decides which tools, resources, permissions, and context sources are exposed and how calls are dispatched.

### Layer C — Tools and integrations
Examples: filesystem, shell/code execution, browser automation, Chrome integration, computer use, MCP servers, connectors, Git operations, extensions, and schedulers.

### Layer D — Environment
The actual OS, repository, running processes, credentials, local network, browser profiles, desktop apps, and external services.

A successful action requires the relevant capability at every required layer.

## Capability states

| State | Meaning | Behavior |
|---|---|---|
| AVAILABLE | Observed and callable | Use according to schema/workflow |
| POSSIBLE | Suggested by host/docs but unverified | Discover/probe before depending on it |
| UNKNOWN | Not enough information | Do not claim it exists; choose a safer alternative |
| UNAVAILABLE | Explicitly absent/disabled | Stop identical calls; use fallback |
| BLOCKED | Exists but permission/approval prevents use | Resolve authorization or use a permitted path |
| STALE | Previously observed but context may have changed | Refresh before use |

Also track **procedural confidence**: HIGH when a specialized workflow is present; MEDIUM when the tool is understood but task guidance is weak; LOW when only a raw tool schema is visible.

## Discovery versus probing

Discovery establishes what the runtime exposes. Probing establishes what is actually usable now.

Use the dedicated protocol in `references/capability-probing.md` when a capability is important but only UNKNOWN/POSSIBLE, when a context boundary may have changed, or when a small safe test can distinguish competing explanations.

Core sequence:

```text
ENUMERATE → INSPECT → SAFE PROBE → OBSERVE → CLASSIFY → USE
```

Never turn a documentation claim, model label, stale observation, or conceptual capability name into `AVAILABLE` without current evidence.

## Capability contract

Before selecting a tool, ask:

1. **Existence:** Is it exposed?
2. **Authority:** Am I permitted to use it?
3. **Suitability:** Is it the narrowest reliable path?
4. **Verification:** What evidence will prove success?

## Capability families

### Filesystem
Best for source inspection, edits, logs, artifacts, and deterministic repository operations. Project knowledge does not imply writable local filesystem access.

### Code / shell execution
Best for builds, tests, scripts, package management, process startup, HTTP checks, and static analysis. Track processes started by the agent.

### Browser
Best for user-facing web behavior, navigation, forms, visual layout, and acceptance flows. Browser state must be observed, not inferred.

### Chrome integration
Best when an existing Chrome session, extension state, or authenticated context matters. Never assume state is shared with an isolated browser.

### Computer use
Best for native GUI or behavior unreachable through a narrower semantic interface. Treat it as escalation because screen interaction is more ambiguous.

### MCP / connectors
Best for structured access to external systems. Prefer direct server-defined operations over GUI automation when the task maps cleanly.

### Skills
Best for procedural knowledge: repeatable task decomposition, domain instructions, scripts, references, and verification recipes. A Skill does not create runtime tools.

### Plugins
Best for packaging Skills, connectors, and related workflows.

### Scheduling / remote dispatch
Best for tasks initiated remotely or on a schedule. It orchestrates underlying capabilities rather than replacing them.

### Artifacts
Best for interactive deliverables with their own persistence, versioning, sharing, and web-access lifecycle. Creation must be separated from correctness and access verification.

## Diagnosing custom-provider failures

```text
Missing runtime tool?
  → integration/runtime problem

Tool exists but model never selects it?
  → capability-awareness/routing problem

Model selects tool but arguments are wrong?
  → schema-use/procedural problem

Tool succeeds but goal is not achieved?
  → workflow/verification problem

Goal achieved but report is wrong?
  → evidence/reporting problem
```

This prevents the Skill from trying to solve a runtime integration defect with additional prompt text.
