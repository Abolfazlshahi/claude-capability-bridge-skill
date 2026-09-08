# Activation, Invocation, and Working Context

## Slash-command activation

In Claude/Desktop-style Skill runtimes, users typically invoke a Skill through its slash command using the Skill's installed name. For this Skill the canonical command is expected to be:

```text
/claude-capability-bridge
```

The exact command surface is controlled by the host runtime. Do not claim that a slash command exists merely because a file is named `SKILL.md`.

When the runtime reports that this Skill has been activated, immediately treat its instructions as the procedural policy for the remainder of the applicable task/session.

## What activation changes

Activation does **not** grant new permissions or tools. It changes the model's operating procedure:

- inspect available capabilities;
- understand the host/tool boundary;
- choose tools deliberately;
- sequence tool calls using observable checkpoints;
- verify outcomes instead of inferring them;
- recover from failures systematically;
- report evidence accurately.

## Session learning behavior

After activation, build a temporary mental model of the current environment from observed facts. Keep it task-scoped and evidence-backed.

Useful facts include:

```text
HOST
  runtime/application identity
  OS/platform
  current project/workspace

TOOLS
  tool names
  schemas
  permissions
  approval requirements

EXECUTION
  shell availability
  working directory
  process model
  package manager

WEB
  browser surfaces
  active URLs
  authentication state (only when safely observable)

INTEGRATIONS
  MCP servers
  connectors
  repositories
  external services

STATE
  started processes
  ports
  temporary files
  changed files
```

Do not memorize credentials, secrets, tokens, private keys, or other sensitive values into narrative state.

## Re-discovery rules

Refresh the capability map when any of these occur:

- a new tool appears;
- a tool becomes unavailable;
- the workspace changes;
- the current project changes;
- a browser session changes;
- a permission boundary changes;
- a process/server state changes materially;
- a connector/MCP server is added or removed.

## Skill composition

When another Skill is more specific to the task, prefer the more specific Skill's procedure for that domain and use this bridge as the orchestration layer.

Example:

```text
/web-specific-skill
       ↓
claude-capability-bridge orchestration
       ↓
actual browser/filesystem/shell tools
```

Do not fight or duplicate a specialized Skill's instructions when they are compatible.
