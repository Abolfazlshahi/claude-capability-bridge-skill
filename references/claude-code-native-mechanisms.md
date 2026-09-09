# Claude Code Native Mechanisms

This file covers Claude Code's host-owned control-plane mechanisms: features that exist in the runtime independently of which model answers the request. Distinguish them from Skills/Plugins (procedural knowledge), MCP (external tools), and model behavior.

A custom-provider model can run inside a Claude Code surface where these mechanisms still apply. Their presence or enforcement must be discovered from the active host; never infer them from the model name.

## Enforcement layers

Use an explicit strength distinction:

```text
DETERMINISTIC HOST CONTROL
→ permission rules / approvals / command hooks that can block

MODEL-BASED HOST CONTROL
→ prompt/agent hooks that ask another model to evaluate a condition

ADVISORY HOST CONTEXT
→ CLAUDE.md / .claude/rules / output styles

MODEL PROCEDURE
→ Skill instructions and the model's own reasoning
```

Do not collapse these into a single category called "runtime enforcement". A runtime can invoke a hook while the hook itself delegates the decision to a model.

## Hooks

Hooks run at host lifecycle events. The event catalog is release-sensitive; treat names below as examples, not an exhaustive stable list. Discover the live event and hook contract before relying on one.

```text
PreToolUse        → runs before a matching tool call; can deny or alter input
PostToolUse       → runs after a successful tool call; cannot undo the action
PostToolUseFailure→ observes failed tool execution
PermissionRequest → participates in approval handling when supported
Stop              → can intervene when the agent tries to finish
UserPromptSubmit  → can inspect or enrich submitted prompts
SubagentStart/Stop→ observe delegated agent lifecycle
WorktreeCreate/Remove → observe worktree lifecycle
```

Two important distinctions:

```text
PreToolUse denial ≠ ordinary model advice
PostToolUse observation ≠ rollback
hook decision ≠ automatically the final permission decision
```

Command hooks can provide deterministic decisions. Prompt-based hooks use an LLM to return a structured decision; agent hooks can invoke an agentic verifier. Treat these as different assurance levels.

A minimal hook shape is illustrative only:

```json
{
  "event": "PreToolUse",
  "matcher": "Bash",
  "command": "scripts/check-dangerous-command.sh"
}
```

Never bypass a hook denial by routing the same consequential operation through a different interface. That is equivalent to bypassing a permission boundary.

## CLAUDE.md and `.claude/rules/`

These are persistent instruction/context mechanisms, not hard authorization controls:

```text
CLAUDE.md        → project/user/org guidance loaded into session context
.claude/rules/   → more narrowly scoped instruction files
```

Claude Code also has auto memory that records learnings separately from human-authored instructions.

Do not confuse:

```text
CLAUDE.md / rules   ≠ Skill
CLAUDE.md / rules   ≠ hook enforcement
auto memory         ≠ authorization policy
account memory      ≠ project-local Code memory
```

Treat CLAUDE.md and auto memory as context the model can follow, not as a deterministic policy engine. See `skills-and-plugins.md`, `session-memory.md`, and `office-and-collaboration-surfaces.md`.

## Slash commands

Three mechanisms can be encountered under the same mental label:

```text
Built-in CLI command   → shipped by the host
User-defined command   → .claude/commands/<name>.md or user-level commands
Skill-as-command       → a host may expose a Skill through a slash-command surface
```

Command registration is host-owned. A remembered command name is not evidence that the active surface exposes it.

## Output styles

Output styles modify the Claude Code system prompt to change response role, tone, or format. They are not the same thing as project instructions or Skills.

```text
Output style        → default response behavior across the session
CLAUDE.md            → project/user/org context
Skill                → task-specific procedural knowledge
```

Custom output styles may also affect whether built-in coding instructions remain present. Verify the active style and settings instead of treating a remembered style catalog as immutable.

## Checkpoints and Rewind

Checkpoints can restore relevant file/conversation state inside the session, but they do not reverse external side effects.

```text
checkpoint / rewind
→ file and session state can move backward

API call / database write / email / webhook
→ external effect remains unless independently reversed
```

Never use reversibility of the workspace as a reason to skip verification before a consequential action. Git remains the source of truth for version history where applicable.

## Git worktrees

A worktree is another working directory attached to the same repository, often used for isolated parallel work.

Before assuming `cwd` uniquely identifies the project:

```text
inspect repository/worktree topology
→ identify active worktree
→ identify branch
→ identify which worktree is being edited or served
```

See `workspace-map.md` and `runtime-boundary-matrix.md` for project-state distinctions.

## Agent teams

Agent teams are a peer coordination topology, not merely a larger subagent count.

```text
subagent model
→ parent session dispatches child and receives its result

team model
→ lead + peer teammates with direct inter-agent messaging
```

A teammate's "done" is still an intermediate claim. The lead must integrate and verify the final user-facing result. Team availability is release- and configuration-sensitive.

## Safe / minimal diagnostic modes

Some Claude Code troubleshooting modes can disable or bypass normal customization so that configuration problems can be isolated. Do not assume a remembered flag name or that every customization is disabled in every mode. Discover the current host behavior before using such a mode.

The diagnostic principle is:

```text
reproduce normally
→ isolate configuration
→ compare behavior with customization reduced
→ restore normal configuration
```

## SDK and non-interactive execution

Claude Code exposes programmatic/SDK paths and headless execution patterns. These are different execution surfaces from an interactive terminal.

```text
interactive terminal
→ user-visible approvals and live interaction may exist

headless / CI / SDK run
→ approval expectations, filesystem context, secrets, and available tools differ
```

Resolve permissions and required context before starting a non-interactive run. Do not assume an interactive browser or human approval can appear mid-run.

## CI/CD

A CI-triggered Claude Code run is its own execution context. Verification must come from artifacts such as diffs, tests, logs, reports, and pipeline status when no interactive browser/desktop is available.

```text
local interactive verification
≠
headless CI verification
```

See `verification.md` and `webapp-verification.md`.

## IDE and remote surfaces

IDE integration can change where the terminal, files, browser, and session state are exposed. Remote execution can also represent a distinct compute environment.

Do not conflate these:

```text
IDE integration       → same task, different host surface
Remote cloud session  → remote execution context
Remote Control        → remote control of an existing local session
```

Remote Control keeps Claude Code running on the user's machine; it is not equivalent to moving the session to cloud execution. Verify the active surface before depending on local files, processes, localhost, browser tabs, or credentials.

## Verification discipline

Every mechanism here is release-sensitive. Use `source-notes.md` discipline: confirm current availability and semantics from the active host or current first-party material before making a hard claim about an event, flag, plan, or default.

The central operating rule is:

```text
HOST MECHANISM PRESENT
≠
MODEL CAN USE IT CORRECTLY
≠
ACTION IS PERMITTED
≠
ACTION SUCCEEDED
≠
OUTCOME IS VERIFIED
```

Related references: `security-and-permissions.md`, `skills-and-plugins.md`, `workspace-map.md`, `runtime-boundary-matrix.md`, `async-subagents-and-remote.md`, `source-notes.md`.
