# Runtime Detection and Profiles

Runtime identity is the first execution fact. Do not route tools, launch projects, or choose a browser surface until the active host and execution context are sufficiently understood.

## Detection order

Use the smallest safe observations available:

```text
OBSERVE HOST SIGNALS
→ CLASSIFY HOST
→ CLASSIFY EXECUTION LOCATION
→ CLASSIFY PROVIDER
→ BUILD RUNTIME PROFILE
→ DISCOVER RELEVANT CAPABILITIES
```

Possible host classes:
`CLAUDE_CODE_CLI | CLAUDE_DESKTOP | COWORK/DESKTOP_SURFACE | WEB/CLOUD | OTHER_AGENT_RUNTIME | UNKNOWN`.

Possible execution locations:
`LOCAL | CLOUD | REMOTE | MIXED | UNKNOWN`.

Do not identify a host from one weak clue. Prefer converging signals such as visible command-line context, host-specific controls, available tools, working directory behavior, session metadata, and documented host mechanisms already exposed by the live runtime.

## Runtime profile

Keep a compact profile and update it when the boundary changes:

```yaml
host: unknown
execution: unknown
provider: unknown
confidence: low
shell: unknown
filesystem: unknown
git: unknown
browser: unknown
chrome: unknown
computer_use: unknown
mcp: unknown
connectors: unknown
artifacts: unknown
remote_or_scheduled: unknown
auth_context: unknown
```

`available` means observed usable now. `unknown` means not tested. `blocked` means the surface exists but access is denied or gated. `unavailable` means evidence shows the surface cannot be used in this context. `stale` means the previous observation is invalid after a material boundary change.

## Decision gates

Use these gates before escalating:

```text
HOST UNKNOWN?
→ inspect runtime-visible signals; do not assume Desktop or CLI

HOST KNOWN, EXECUTION UNKNOWN?
→ establish local/cloud/remote context before touching local state

PROVIDER UNKNOWN?
→ use observable provider/model metadata when available

TASK NEEDS A CAPABILITY?
→ probe only that capability family
```

A runtime profile is an execution aid, not proof that every listed surface exists. Tool schemas and actual results remain authoritative.

## CLI versus Desktop

CLI evidence should bias toward terminal/filesystem/Git/project execution and host-native CLI mechanisms. Desktop/Cowork evidence should bias toward visible application surfaces, native GUI/browser/computer-use paths, local integrations, and desktop session state.

Do not transplant a Desktop-only workflow into CLI merely because the conceptual capability has the same name. Conversely, do not force GUI work when a CLI or structured interface is authoritative and available.

## Provider is a separate axis

`HOST = Claude Code CLI` does not imply `PROVIDER = first-party Anthropic`, and a third-party provider can change which host features are actually usable. Treat provider restrictions as a runtime/provider boundary, not as a Skill failure.

For browser integrations, distinguish:

```text
host supports browser integration
vs
current provider/session permits that integration
vs
required executable/session is connected
```

A capability may therefore be `BLOCKED` or `UNAVAILABLE` for the current provider even when the host product supports it elsewhere.

## Freshness

Invalidate the profile after:

`model/provider switch | runtime restart | /remote or teleport-style boundary change | browser/context switch | permission change | MCP reconnect | session migration | scheduled run | workspace change`.

Re-probe only the affected fields instead of rebuilding everything blindly.

## Minimum evidence report

Before a high-impact branch, be able to state internally:

```text
HOST = ?
EXECUTION = ?
PROVIDER = ?
RELEVANT CAPABILITIES = ?
AUTH/SESSION CONTEXT = ?
CONFIDENCE = ?
```

If the answer is still ambiguous, choose a reversible probe or a route that does not depend on the ambiguous assumption.