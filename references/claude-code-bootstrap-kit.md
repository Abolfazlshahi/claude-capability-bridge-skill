# Claude Code Bootstrap Kit

This is the concrete host-configuration path for making the bridge protocol harder to forget. It does not turn the portable Skill into a universal hook and does not grant capabilities.

## 1. Persistent `CLAUDE.md` rule

Place a compact rule in the project or user-level `CLAUDE.md`:

```text
For non-trivial execution, first identify the active runtime and execution location, then identify the provider when observable. Discover only the capabilities required by the task from the live host. A missing capability must be classified before stopping; repair only when the current context can affect the cause. Re-probe after repair or a boundary change. Verify the requested result directly and never claim a tool action that did not occur.
```

Use this when persistent advisory context is sufficient.

## 2. SessionStart hook

Claude Code's current `SessionStart` hook can add `additionalContext` before the first prompt and after resume/clear/compact/fork. Keep the output tiny and fast. The repository ships working examples in `bootstrap/session-start.sh` and `bootstrap/session-start.ps1`; `bootstrap/settings.json.example` shows the hook registration shape.

A good hook emits only the bridge reminder:

```text
BRIDGE BOOT:
- detect host: CLI/Desktop/Cowork/remote/other
- detect execution: local/cloud/remote
- detect provider when observable
- non-trivial work: discover → probe → remediate → route → act → verify
- never treat “not connected” as a final diagnosis
```

The hook should not dump the whole Skill or perform arbitrary setup on every session. `SessionStart` is a context-only event: it cannot block the session, so do not call the reminder deterministic enforcement. See the current Claude Code Hooks reference for the event semantics.

## 3. Plugin distribution

For Claude Code distribution, bundle the Skill and SessionStart hook as one plugin. The repository provides `scripts/package_claude_code_plugin.py`, which generates a plugin under `dist/claude-capability-bridge-plugin/` from the current source files. The generated plugin uses `${CLAUDE_PLUGIN_ROOT}` for its hook script, avoiding assumptions about the project checkout.

Test the generated plugin locally with:

```text
claude --plugin-dir ./dist/claude-capability-bridge-plugin
```

Plugins can package Skills and hooks together, and plugin hooks live in `hooks/hooks.json`.

## 4. Stronger host enforcement

Use deterministic command hooks or permission controls for concrete safety rules that must hold independently of model judgment. Use prompt/agent hooks only when model judgment is intentionally part of the control. Never describe a model-mediated hook as equivalent to deterministic enforcement, and never use the bootstrap to bypass a host denial.

## 5. Skill invocation

Keep the bridge Skill's normal model invocation enabled so Claude can load it when relevant. `disable-model-invocation: true` prevents automatic loading and would work against this Skill's purpose as background procedural knowledge. Claude's current Skills reference also distinguishes the Skill's always-present description from its full body, which loads only when invoked.

A host bootstrap can improve recall, but it does not guarantee that the Skill body is loaded on every turn. `/skill-doctor` can show whether skills are being invoked and should be used as supplementary evidence during local testing.

## 6. Verification

Test three conditions on the same task in fresh sessions:

```text
CONTROL: no bridge
TREATMENT A: bridge Skill only
TREATMENT B: bridge Skill + always-on bootstrap
```

Record whether the agent:

```text
identifies runtime before host-specific routing
→ classifies missing capabilities
→ attempts only justified remediation
→ re-probes after repair
→ chooses an authoritative interface
→ verifies the requested outcome
```

Do not report bootstrap effectiveness from static inspection alone. Current Claude Code skill-evaluation guidance recommends fresh-session comparison and separate measurement of invocation from what the Skill does after invocation.

## Boundary

A portable Skill can ship the recipe and examples, but only the Claude Code host can register lifecycle hooks. For hosts without such a mechanism, degrade to the portable Skill and explicit invocation rather than pretending enforcement exists. A bootstrap may keep the protocol present, but it cannot grant tools, bypass permissions, or make a third-party provider support an unsupported host feature.
