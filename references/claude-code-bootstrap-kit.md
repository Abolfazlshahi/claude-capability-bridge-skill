# Claude Code Bootstrap Kit

This is an optional host-configuration pattern for making the bridge protocol harder to forget. It does not turn the Skill into a hook and does not grant capabilities.

## 1. Persistent `CLAUDE.md` rule

Place a compact rule in the project or user-level `CLAUDE.md`:

```text
For non-trivial execution, first identify the active runtime and execution location, then identify the provider when observable. Discover only the capabilities required by the task from the live host. A missing capability must be classified before stopping; repair only when the current context can affect the cause. Re-probe after repair or a boundary change. Verify the requested result directly and never claim a tool action that did not occur.
```

Use this when a persistent advisory instruction is sufficient.

## 2. Session-start reminder

Where the host permits a SessionStart lifecycle hook, have the hook emit a short reminder or capability snapshot instead of the whole Skill:

```text
BRIDGE BOOT:
- detect host: CLI/Desktop/Cowork/remote/other
- detect execution: local/cloud/remote
- detect provider when observable
- for non-trivial work: discover → probe → remediate → route → act → verify
- never treat “not connected” as a final diagnosis
```

Keep the hook payload small so it reinforces behavior without flooding every session with reference material.

## 3. Optional deterministic guard

Use host hooks or permissions for deterministic controls such as blocking known-dangerous operations. Do not describe a prompt-based hook as equivalent to a deterministic command hook, and do not use the bootstrap as a way to bypass a host denial.

## 4. Verification

Test the bootstrap rather than assuming it works:

```text
new session
→ issue a task that needs browser + local execution
→ record whether runtime detection happened before routing
→ record whether missing browser capability was classified
→ compare with Skill-only control
```

The correct claim is “bootstrap supplied always-on reminder/context” unless a host-enforced control actually provided stronger enforcement.

## Boundary

A portable Skill can ship this recipe, but cannot install or activate host hooks on every runtime. Actual lifecycle configuration remains owned by the host. If the host has no always-on mechanism, the Skill must degrade gracefully rather than pretending enforcement exists.
