# Workspace Map

Claude Desktop-like agent environments are best understood as overlapping state domains rather than one monolithic "Claude" capability.

```text
┌────────────────────────────────────────────┐
│ HOST RUNTIME                               │
│ permissions • tools • platform • session   │
├───────────────┬────────────────────────────┤
│ CONVERSATION  │ SKILL POLICY               │
│ intent/context│ procedures/references      │
├───────────────┼────────────────────────────┤
│ PROJECT       │ FILESYSTEM / GIT           │
│ knowledge     │ live source/history        │
├───────────────┼────────────────────────────┤
│ PROCESSES     │ BROWSER / CHROME           │
│ servers/jobs  │ tabs • origin • auth state │
├───────────────┼────────────────────────────┤
│ MCP / CONNECTORS / INTEGRATIONS            │
│ external structured state and actions      │
└────────────────────────────────────────────┘
```

## Layers

### Conversation
Contains user intent, constraints, observations, and prior discussion. Conversation text is not proof that a tool action occurred.

### Skill policy
Supplies reusable procedural knowledge, references, scripts, and assets. It influences model behavior but does not silently create runtime capability.

### Agent runtime
Controls which tools are exposed, how calls are dispatched, which context is injected, and what approvals/permissions apply.

### Tool surfaces
Typical surfaces include filesystem/project files, shell/code execution, browser automation, existing Chrome/browser sessions, computer control, MCP tools/resources/prompts, connectors, Git, scheduling/remote dispatch, and application integrations.

### Environment
The actual OS, filesystem, processes, network, localhost services, browser profile, desktop applications, repositories, and remote APIs.

## Truth hierarchy

For a concrete environmental fact, prefer evidence closest to the live state:

```text
current tool observation
    > live process/log output
    > filesystem/Git inspection
    > explicit project configuration
    > prior conversation statement
    > model memory
```

The best source depends on the fact. Project configuration is authoritative for declared commands; live process observation is authoritative for whether a process is currently running.

## Separate truth domains

| Domain | Proves |
|---|---|
| Project knowledge | What is loaded into project context |
| Filesystem | What the current filesystem interface can reach |
| Git | Repository state/history visible through Git |
| Process state | Processes actually observed/running |
| Browser state | Current page/origin/UI state in the chosen browser |
| MCP/connectors | Results returned by integrations |
| Conversation | Instructions and claims, not execution proof |

Seeing `README.md` in project knowledge does not prove the file is writable on disk.

## Session capability ledger

Maintain internally:

```text
Capability | Evidence | Permission | Preferred use | Fallback | Freshness
```

Downgrade or invalidate stale entries after environment changes.

## State transitions

Think in observable state transitions:

```text
unknown workspace
    ↓ inspect
known workspace
    ↓ execute
process created
    ↓ readiness probe
service ready
    ↓ browser navigation
page loaded
    ↓ user action
state changed
    ↓ assertion
verified
```

Each transition is an observation checkpoint.

## Workspace changes

When switching projects/repositories/workspaces, reconsider:

- cwd and filesystem roots;
- Git worktree/status;
- package manager and scripts;
- running servers/processes;
- browser origin and test URL;
- credentials/authentication context;
- available integrations;
- permissions.

Do not carry ports, URLs, auth assumptions, paths, or tool choices from the old workspace without evidence.
