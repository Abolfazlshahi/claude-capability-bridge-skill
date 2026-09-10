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

The hook should not dump the whole Skill or perform arbitrary setup on every session.

## 3. Stronger host enforcement

Use deterministic command hooks or permission controls for concrete safety rules that must hold independently of model judgment. Use prompt/agent hooks only when model judgment is intentionally part of the control. Never describe a model-mediated hook as equivalent to deterministic enforcement, and never use the bootstrap to bypass a host denial.

## 4. Skill invocation

Keep the bridge Skill's normal model invocation enabled so Claude can load it when relevant. `disable-model-invocation: true` is for intentionally user-triggered workflows and would work against this Skill's purpose as background procedural knowledge.

A host bootstrap can improve recall, but it does not guarantee that the Skill body is loaded on every turn. Measure that behavior instead of assuming it.

## 5. Verification

Test three conditions on the same task:

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

Do not report bootstrap effectiveness from static inspection alone.

## Boundary

A portable Skill can ship the recipe and example files, but only the Claude Code host can register its lifecycle hooks. For hosts without such a mechanism, degrade to the portable Skill and explicit invocation rather than pretending enforcement exists.
