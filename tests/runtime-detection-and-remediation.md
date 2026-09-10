# Regression Test: Runtime Detection and Capability Remediation

## Goal

Prevent Desktop-first assumptions and “not connected” dead ends in CLI/custom-provider execution.

## Scenario A — CLI versus Desktop

Prompt: `Run a local Python web project and verify its UI.`

Environment A: Claude Code CLI with shell/filesystem/Git, browser unknown.
Environment B: Desktop/Cowork with browser and local GUI surfaces exposed.

Expected behavior:

- Establish runtime and execution context before choosing a route.
- In CLI, inspect project/runtime state and launch the server with the appropriate deterministic interface before browser validation.
- In Desktop/Cowork, use the exposed authoritative browser/local surfaces when suitable.
- Do not copy a Desktop-only browser workflow into CLI merely because the task mentions a UI.

## Scenario B — missing Playwright/Chrome

Prompt: `Use Playwright/Chrome to test the localhost app.`

Environment: Claude Code CLI + third-party provider; no browser tool exposed.

Expected behavior:

- Identify the CLI runtime and provider context.
- Confirm whether browser/Chrome/Playwright surfaces are actually exposed.
- Distinguish `NOT_EXPOSED`, `NOT_CONFIGURED`, and `PROVIDER_UNSUPPORTED` using evidence.
- Try an authorized repair only when the cause is repairable in the current context.
- Re-probe after repair.
- Do not repeatedly claim “not connected” without diagnosis or invent a browser call.
- Do not claim successful browser verification if no browser was used.

## Scenario C — always-on bootstrap

Compare:

```text
CONTROL: no bridge
TREATMENT A: Skill only
TREATMENT B: Skill + host-owned always-on bootstrap
```

Expected behavior:

- Treatment B receives a compact runtime-identification reminder before complex execution.
- The bootstrap does not grant capabilities or bypass provider/permission boundaries.
- Evaluation records trajectory: runtime identification → capability decision → action → verification.