# Async Work, Subagents, Scheduling, and Remote Execution

Claude Desktop/Cowork can run work beyond a single short synchronous turn. Public Anthropic material describes subagents, long-running work, scheduled tasks, and cross-surface sessions. These are orchestration capabilities, not substitutes for the underlying tools.

## Subagents

Delegate only a bounded subtask with a clear input, output, and completion condition when parallelism or context isolation provides a real benefit.

Good delegation:

```text
Main task
├─ investigate dependency choice
├─ inspect unrelated subsystem
└─ compare two implementation approaches
```

Bad delegation:

```text
delegate entire task
→ no explicit output contract
→ duplicate work
→ unclear authority
```

The parent agent remains responsible for integrating results and verifying the final user-facing outcome.

## Long-running work

For extended execution, maintain:

```text
objective
current phase
owned processes
expected outputs
last verified checkpoint
next recovery point
```

Do not infer completion from elapsed time or a still-open session. Look for actual output or a host-provided completion signal.

## Scheduled tasks

A scheduled task is a separate execution session. Treat it as a new environment initialization, even when it reuses the user's prompt/configuration.

At scheduled-run start:

1. re-establish capabilities;
2. verify accessible files/connectors/skills/plugins;
3. confirm the intended time-scoped data;
4. perform the task;
5. verify outputs;
6. record failures or missing capabilities.

Do not assume the user's computer is awake, a local server is running, or local-only state exists during a scheduled run.

## Remote / cross-surface execution

When work moves between desktop, web, or mobile surfaces, preserve the task objective but re-check environment-specific capabilities.

```text
same conversation/session
        ≠
same execution surface
        ≠
same local resources
        ≠
same browser state
```

Remote connectors may be brokered from cloud infrastructure while local Desktop Extensions/MCP servers run on the user's machine. Verify which boundary applies before depending on local access.

## Handoff contract

When transferring work:

```text
verified objective
+ verified artifacts/state
+ known limitations
+ next required observation
```

Never transfer secrets unnecessarily.

## Completion rule

Async or delegated execution increases the need for explicit checkpoints; it does not reduce it.
