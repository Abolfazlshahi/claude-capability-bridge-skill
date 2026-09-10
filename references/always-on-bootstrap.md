# Always-On Bootstrap

A portable Agent Skill is procedural knowledge; it is not a universal lifecycle hook. When the host supports lifecycle hooks, use them to keep the bridge protocol present before work starts, before each submitted turn, and immediately after a tool failure.

## Architecture

```text
HOST-OWNED BOOTSTRAP
→ tiny runtime/capability reminder
→ CLAUDE CAPABILITY BRIDGE
→ discover → probe → remediate → route → act → verify
```

The bootstrap must stay small. Do not inject the full Skill on every turn. Its job is to prevent procedural forgetting, not to duplicate the reference library.

## Bootstrap contract

A useful bootstrap should tell the model:

```text
1. Identify the active runtime (CLI/Desktop/Cowork/remote/other).
2. Identify execution location and provider when observable.
3. Before a non-trivial action, discover only the capabilities the task needs.
4. Treat missing capability as something to classify, not an automatic stop.
5. Re-probe after repair or boundary changes.
6. Verify the requested outcome with direct evidence.
```

A session-start reminder establishes the operating protocol. A per-turn reminder is stronger against model procedural forgetting because it is injected immediately before the submitted prompt. A post-tool-failure reminder catches the other critical failure mode: stopping after a generic error or blindly repeating the same call. Keep all reminders short and factual; the Skill body remains the source of the full procedure.

## Claude Code-style hosts

Claude Code exposes host-owned lifecycle/configuration mechanisms such as `CLAUDE.md` and hooks. `CLAUDE.md` is suitable for concise persistent project rules. `SessionStart` can inject a small bootstrap at session start/resume, `UserPromptSubmit` can inject a compact reminder before every submitted prompt, and `PostToolUseFailure` can inject recovery guidance after a tool failure.

Example persistent rule:

```text
Before non-trivial work, identify runtime and execution context. Discover required capabilities from the live host, classify missing integrations, attempt authorized remediation when possible, then verify the requested outcome. Never assume Desktop, CLI, browser, Chrome, MCP, or provider capabilities from Skill text alone.
```

Use the failure hook for procedure recovery, not as a blind retry engine:

```text
TOOL FAILURE → inspect actual error → classify cause
→ change one material variable → re-probe when appropriate
→ retry only when justified → verify
```

Keep host-specific syntax in host configuration or a plugin rather than in the portable Skill kernel. Hook schemas and available events are runtime/version dependent. The bundled Claude Code plugin packages `SessionStart`, `UserPromptSubmit`, and `PostToolUseFailure` around the same authoritative Skill.

## What bootstrap cannot do

Bootstrap does not:

`grant tools | bypass permissions | create browser access | make a third-party provider support a host feature | repair invalid tool protocols | guarantee model tool-calling`.

A per-turn or failure reminder improves procedural recall but is still context, not a new capability. If the model still forgets after the reminders and the capability is visibly exposed, classify that as a procedural/model behavior issue. Prefer deterministic structured interfaces or host-enforced controls for requirements that must not depend on model compliance.

## Evaluation

Compare at least three conditions when testing forgetting and failure recovery:

```text
CONTROL: no bridge
TREATMENT A: Skill only
TREATMENT B: Skill + session/per-turn/failure bootstrap
```

Use fresh sessions. Measure Skill invocation separately from task execution, and record whether the agent identifies the runtime, enters the capability loop before acting, distinguishes missing configuration from provider limits, recovers after a failed tool call, and verifies the result. Do not claim bootstrap effectiveness without a controlled behavioral run.
