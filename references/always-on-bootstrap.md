# Always-On Bootstrap

A portable Agent Skill is procedural knowledge; it is not a universal lifecycle hook. When the host supports lifecycle hooks, use them to keep the bridge protocol present before work starts and, where appropriate, before each submitted turn.

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

A session-start reminder establishes the operating protocol once. A per-turn reminder is stronger against model procedural forgetting because it is injected immediately before the submitted prompt. Keep both reminders short and factual; the Skill body remains the source of the full procedure.

## Claude Code-style hosts

Claude Code exposes host-owned lifecycle/configuration mechanisms such as `CLAUDE.md` and hooks. `CLAUDE.md` is suitable for concise persistent project rules. `SessionStart` can inject a small bootstrap at session start/resume, while `UserPromptSubmit` can inject a compact reminder before every submitted prompt. `UserPromptSubmit` runs before Claude processes the prompt and can add `additionalContext`; it cannot replace the prompt itself.

Example persistent rule:

```text
Before non-trivial work, identify runtime and execution context. Discover required capabilities from the live host, classify missing integrations, attempt authorized remediation when possible, then verify the requested outcome. Never assume Desktop, CLI, browser, Chrome, MCP, or provider capabilities from Skill text alone.
```

Keep host-specific syntax in host configuration or a plugin rather than in the portable Skill kernel. Hook schemas and available events are runtime/version dependent. The bundled Claude Code plugin therefore packages a `SessionStart` hook and a `UserPromptSubmit` hook around the same authoritative Skill.

## What bootstrap cannot do

Bootstrap does not:

`grant tools | bypass permissions | create browser access | make a third-party provider support a host feature | repair invalid tool protocols | guarantee model tool-calling`.

A per-turn reminder improves procedural recall but is still context, not a new capability. If the model still forgets after the reminder and the capability is visibly exposed, classify that as a procedural/model behavior issue. Prefer deterministic structured interfaces or host-enforced hooks for requirements that must not depend on model compliance.

## Evaluation

Compare at least three conditions when testing forgetting:

```text
CONTROL: no bridge
TREATMENT A: Skill only
TREATMENT B: Skill + session/per-turn bootstrap
```

Use fresh sessions. Measure Skill invocation separately from task execution, and record whether the agent identifies the runtime, enters the capability loop before acting, distinguishes missing configuration from provider limits, and verifies the result. Do not claim bootstrap effectiveness without a controlled behavioral run.
