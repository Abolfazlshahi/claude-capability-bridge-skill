# Code and Shell Execution

## Principle

Use code/shell for deterministic work: inspect, transform, build, test, launch, probe, and collect logs. Prefer declared project commands and reversible operations.

## Pre-flight

Identify:

- operating system/shell;
- current working directory;
- repository root;
- runtime versions;
- package manager/environment manager;
- environment variables required by the task;
- commands declared by the project;
- project execution model (static, server-backed, full-stack, or unknown).

Before launching anything, inspect the project's authoritative metadata and instructions. Consult `references/project-recognition-and-launch.md` for the recognition matrix.

Do not expose or print secrets unnecessarily.

## Launch precondition

Do not choose a command only because it is a familiar framework command. Establish:

```text
project type
→ framework/runtime
→ entry point
→ declared start/dev/preview command
→ dependencies
→ expected host/port
→ readiness signal
```

For a server-backed project, the goal is to launch the application's server/runtime, not to open one of its templates or source files directly in a browser.

For an intentionally static project, direct file preview may be valid. For an unknown project, inspect further before launching.

## Command selection

Prefer:

```text
project-declared script / command
→ package-manager script
→ framework CLI
→ generic shell command
```

Do not replace a project-defined command with an approximate remembered command unless necessary and supported by project evidence.

## Process management

When starting a long-running service, record:

```text
PID
command
cwd
stdout/stderr location
port/URL
start time
```

Use a dedicated process group or wrapper when supported. Do not kill by broad name matching. Stop only processes known to be owned by the current task.

## Readiness

A process existing is not readiness. Prefer a project health endpoint, successful TCP connection, HTTP response, browser load, or project-specific readiness signal.

```text
START
→ WAIT WITH BACKOFF
→ PROBE
→ READY?
   ├─ yes → continue
   └─ no → inspect logs → classify → recover
```

## Testing

Run the smallest useful check first, then broaden:

```text
syntax/type check
→ targeted test
→ related integration test
→ full suite/build when practical
```

Preserve baseline failures separately from newly introduced failures.

## HTTP/API smoke checks

For a local service:

1. determine actual URL/port;
2. call health/readiness endpoint when available;
3. test required endpoint(s) with representative safe input;
4. verify status, content type, schema, and important fields;
5. verify side effects through a safe read path if applicable.

Do not infer API correctness from process logs alone.

## Package installation

Before installing dependencies:

- inspect lockfiles and package metadata;
- use the project's package/environment manager;
- avoid unnecessary global installs;
- avoid replacing versions merely to silence a warning;
- understand whether installation modifies tracked files.

## Destructive commands

Treat recursive deletion, resets, database migrations, force pushes, credential changes, package upgrades, and system-wide modifications as high-impact. Require explicit user intent where appropriate and prefer dry runs/backups.

## Output discipline

Keep command output focused. When logs are huge, search for relevant errors and preserve a small contextual excerpt rather than flooding context. Never paste credentials, tokens, cookies, private keys, or other secrets into the conversation.