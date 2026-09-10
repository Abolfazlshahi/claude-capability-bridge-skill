# Always-On Bootstrap

A portable Agent Skill is procedural knowledge; it is not a universal lifecycle hook. If the host supports an always-on context or lifecycle mechanism, use that mechanism to remind the model to enter the bridge protocol before complex execution.

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

Keep this reminder advisory unless the host mechanism itself provides deterministic enforcement.

## Claude Code-style hosts

Claude Code exposes host-owned lifecycle/configuration mechanisms such as `CLAUDE.md` and hooks. These mechanisms are distinct from Skills. `CLAUDE.md` is suitable for a concise persistent operating rule; a lifecycle hook can prepare or inject a small session-start capability reminder when the host configuration permits it.

Example persistent rule:

```text
Before non-trivial work, identify runtime and execution context. Discover required capabilities from the live host, classify missing integrations, attempt authorized remediation when possible, then verify the requested outcome. Never assume Desktop, CLI, browser, Chrome, MCP, or provider capabilities from Skill text alone.
```

A SessionStart-style hook may generate a similarly small reminder or capability snapshot. Keep host-specific syntax in host configuration, not in the portable Skill kernel, because hook schemas and available events are runtime/version dependent.

## What bootstrap cannot do

Bootstrap does not:

`grant tools | bypass permissions | create browser access | make a third-party provider support a host feature | repair invalid tool protocols | guarantee model tool-calling`.

If the model still forgets after an always-on reminder and the capability is visibly exposed, classify that as a procedural/model behavior issue and prefer deterministic structured interfaces where possible.

## Evaluation

Compare three conditions when testing forgetting:

```text
CONTROL: no bridge
TREATMENT A: Skill only
TREATMENT B: Skill + always-on bootstrap
```

Measure whether the agent identifies the runtime, enters the capability loop before acting, distinguishes missing configuration from provider limits, and verifies the result. Do not claim bootstrap effectiveness without a controlled behavioral run.