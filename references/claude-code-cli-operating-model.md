# Claude Code CLI Operating Model

Treat Claude Code CLI as a first-class operating profile, not as a thin variant of Desktop. CLI work normally centers on terminal execution, filesystem, Git/worktrees, MCP, Skills/plugins, hooks, project processes, and explicit remote/cloud boundaries. GUI/browser surfaces are conditional and must be discovered.

## CLI entry gate

Before host-specific routing:

```text
IDENTIFY CLI
→ IDENTIFY LOCAL/CLOUD/REMOTE CONTEXT
→ IDENTIFY PROVIDER/ENDPOINT
→ DISCOVER EXPOSED TOOLS
→ SELECT CLI-AUTHORITATIVE PATH
```

Strong CLI signals include an actual command-line host, shell/terminal operations, CLI-native project execution, and Code-specific lifecycle/configuration surfaces. Do not infer CLI merely because a task is about code.

## Provider axis

Keep host and provider separate:

```text
HOST = Claude Code CLI
PROVIDER = first-party / third-party / unknown
```

A host feature may be unavailable to the current provider. Treat that as a boundary to diagnose, not as a reason to repeat setup attempts indefinitely. Empirical tool exposure and successful calls remain authoritative.

## CLI routing defaults

Prefer the narrowest authoritative interface:

```text
edit code/files → filesystem/editor operations
run tests/builds → shell
Git state → Git/CLI
local server → shell/process + readiness probe
structured integration → MCP/connector
browser verification → exposed browser surface
GUI-only state → computer use when exposed
```

For standard app-running tasks, use native Claude Code run/verify workflows when they are exposed and suitable; do not assume they replace project-specific launch discovery for databases, env files, graphical sessions, or multi-service apps. Never turn a source/template file into browser testing merely because it is easy to open. Server-backed projects need a real process and served HTTP route.

## Browser in CLI

Browser capability is a separate axis from “CLI can run code.” Check independently for:

```text
BROWSER TOOL EXPOSED?
CHROME SESSION EXPOSED?
PLAYWRIGHT/MCP EXPOSED?
LOCAL BROWSER REACHABLE?
CURRENT PROVIDER ALLOWS THE INTEGRATION?
```

For Claude Code Chrome integration, use only the commands/surfaces actually exposed by the current host. Current official Claude Code documentation describes `--chrome` / `/chrome`, while also documenting that Chrome integration is unavailable through third-party providers. Do not fabricate the integration when the current provider/session does not expose it.

If Chrome is unavailable but Playwright/MCP is exposed and suitable, route there. If neither is exposed, use shell/project evidence for server health and report browser verification as blocked rather than pretending to have tested the UI.

## Skill and host-control verification

A Skill is still model-invoked procedural context. Do not confuse its availability with execution. In Claude Code, use host surfaces such as `/skills` or `/hooks` when exposed to inspect whether the Skill/hook is actually registered. `CLAUDE.md` is persistent advisory context; command hooks can provide stronger deterministic control where the host supports it. A bootstrap reminder is not a permission bypass.

## Local app verification

For a Python/Node/etc. repository:

```text
inspect project
→ identify framework + environment
→ find declared launch command
→ start intended process
→ observe readiness/port
→ open served HTTP route through an exposed browser
→ exercise critical path
→ verify
```

`file://` opening a server-side template is not application verification.

## Remote and cloud boundary

`Remote Control`, cloud/web execution, scheduled work, CI, and local CLI sessions are distinct contexts. Re-discover filesystem, process, browser, authentication, network, and permissions after crossing a boundary. Do not assume a localhost PID or Chrome tab follows the session.

## Recovery contract

When a requested CLI integration is missing:

```text
NOT_EXPOSED / NOT_CONFIGURED / NOT_INSTALLED / NOT_RUNNING
/ PERMISSION_DENIED / PROVIDER_UNSUPPORTED / AUTH_SESSION
/ PROTOCOL_FAILURE / MODEL_PROCEDURAL_FAILURE / UNKNOWN
```

Then repair only the class the current context can affect, re-probe, and select a fallback. A provider-unsupported browser feature is not repaired by installing more local packages.

## Evidence target

For consequential CLI claims, preserve:

```text
host + execution context + provider
actual interface used
command/tool result
readiness/target evidence
final verification evidence
```

A successful CLI command, a visible tool schema, or a server PID alone does not prove the user's requested result.
