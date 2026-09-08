# Activation, Slash Commands, and Skill Lifetime

## Slash-command model

In hosts that expose Skills as slash commands, the intended user-facing invocation is conceptually:

```text
/claude-capability-bridge
```

The host, not this repository, owns slash-command registration and activation UI. A model must not claim that installation alone proves the command is registered.

## After activation

Treat activation as a procedural context change, not a permission escalation.

```text
USER INVOKES SKILL
       ↓
HOST LOADS SKILL
       ↓
MODEL RECEIVES SKILL CONTEXT
       ↓
BUILD SESSION CAPABILITY MAP
       ↓
APPLY ROUTING + VERIFICATION CONTRACT
```

Immediately after activation, establish only the facts relevant to the current task:

- current workspace/project;
- available tool surfaces;
- relevant permissions and approval requirements;
- live filesystem/worktree state;
- active browser/Chrome surface when relevant;
- running processes/servers when relevant;
- specialized Skills or integrations that may own the task.

## What activation changes

Activation changes procedural behavior. It does **not** grant tools, permissions, browser sessions, filesystem mounts, network access, or other runtime capability.

## Session learning

Build a temporary, evidence-backed mental model of the current environment. Prefer direct observations and tool metadata over assumptions. Keep the model task-scoped.

Useful state domains:

```text
HOST / PROJECT / FILESYSTEM / GIT
PROCESSES / BROWSER / CHROME
MCP / CONNECTORS / SKILLS
PERMISSIONS / AUTH / ACCEPTANCE
```

Never store secrets, API keys, cookies, tokens, private keys, or credentials in the state model.

## Re-discovery and invalidation

Refresh or downgrade state when:

- a tool appears, disappears, or changes schema;
- the workspace/project changes;
- the browser surface or origin changes;
- permissions change;
- a process/server restarts or exits;
- MCP/connectors reconnect;
- the user manually changes the environment;
- a new observation contradicts an earlier assumption.

Treat old state as stale when necessary rather than forcing new observations to fit it.

## Skill composition

When another Skill is more specialized for the current domain, let that Skill own domain-specific instructions and use this bridge for host capability routing, state awareness, verification, and recovery.
