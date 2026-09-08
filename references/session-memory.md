# Session Capability Memory

The bridge uses a lightweight, revisable internal model of the current agent session.

## State domains

```text
HOST
PROJECT
FILESYSTEM
GIT
PROCESSES
BROWSER
CHROME
MCP
CONNECTORS
SKILLS
PERMISSIONS
AUTH
ACCEPTANCE
```

## State principles

- Keep observed state separate from assumptions.
- Attach confidence to ambiguous values.
- Prefer the newest direct observation over old inferred state.
- Invalidate stale state after environment changes.
- Never store secrets or sensitive tokens in the state model.

## Useful state examples

```text
cwd = /workspace/project
server = owned-by-agent
server_pid = observed-pid
server_url = http://127.0.0.1:4173
browser_surface = built-in
browser_url = http://127.0.0.1:4173/dashboard
mcp.github = available
chrome.authenticated = unknown
```

## State transitions

```text
UNKNOWN → OBSERVED → CONFIRMED
             ↓
          STALE
             ↓
         RE-DISCOVER
```

Use `STALE` internally when an earlier fact may no longer describe the environment.

## Invalidation triggers

Invalidate or downgrade state when:

- a process exits;
- a server restarts on a different port;
- the project/workspace changes;
- the browser navigates to a different origin;
- credentials/session context changes;
- an MCP server reconnects or disappears;
- permissions change;
- the user takes control of the desktop or browser;
- a tool returns a result that contradicts the previous state.

## Memory discipline

Do not narrate a giant state dump to the user on every turn. Maintain it internally and surface only facts needed to explain a decision, limitation, or verification result.
