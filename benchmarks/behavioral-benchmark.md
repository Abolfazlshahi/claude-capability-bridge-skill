# Behavioral Benchmark

The benchmark measures whether the Skill changes agent behavior, not whether files or keywords exist.

## Method

Use fresh sessions and compare the same scenario under controlled conditions:

```text
CONTROL: model + runtime without claude-capability-bridge
TREATMENT A: same model + runtime + claude-capability-bridge
TREATMENT B: same model + runtime + bridge + always-on bootstrap
```

Keep the workspace, tool surface, permissions, provider, task wording, and success criteria constant. Grade **invocation**, **trajectory**, and **final state** separately. A skill appearing in the listing is not evidence that Claude invoked it, and invoking it is not evidence that the workflow was followed.

For Claude Code, fresh sessions matter because already-loaded Skill content can mask activation gaps. When `/skill-doctor` is exposed, its usage report may supplement invocation evidence; it does not prove task correctness.

## Primary scenario: server-backed web app

Workspace contains:

```text
app.py
requirements.txt
templates/reports.html
README.md
```

README says the project is a Python web server and provides its launch command.

### Control failure signature

Common incorrect behavior to detect:

```text
detect reports.html
→ open file://.../templates/reports.html
→ claim the reports page is tested
```

### Treatment target trajectory

```text
invoke/load bridge when relevant
→ identify runtime + execution context + provider when observable
→ inspect workspace
→ recognize server-backed Python app
→ inspect declared environment/command
→ launch server (or use exposed /run or /verify workflow when suitable)
→ confirm readiness + actual URL/port
→ discover an actually exposed browser surface
→ open HTTP route
→ perform representative user action
→ observe result
→ verify acceptance criteria
```

## CLI browser/provider scenario

Run inside Claude Code CLI with a third-party provider and a task requiring local server launch plus Chrome/Playwright verification.

Expected trajectory:

```text
detect CLI
→ keep provider separate from host
→ inspect browser/Chrome/Playwright/MCP exposure
→ classify provider restriction vs configuration vs missing executable vs no tool
→ repair only an actionable class
→ re-probe
→ use supported browser route when available
→ otherwise report browser verification blocked with evidence
```

Grade as a regression if the agent repeatedly says “not connected” without classification, invents a browser call, or retries a provider-unsupported path without changing a relevant variable.

## Forgetting / bootstrap scenario

Use the same non-trivial task across all three conditions and record whether the bridge Skill is actually invoked. Measure the ordered trajectory:

```text
runtime identification
→ capability discovery
→ remediation classification
→ routing
→ verification
```

Credit Treatment B only for behavior that actually changes because of the always-on reminder/context. Do not attribute host-enforced behavior to the Skill, and do not claim bootstrap created capabilities.

## Secondary scenarios

### Capability probe

Runtime exposes a browser with navigate/read/click/type but no DOM/console. Expected: discover exact contract, perform a harmless probe, use only exposed operations, classify DOM/console as unavailable.

### Browser context routing

An authenticated task must continue in an existing Chrome tab while an isolated browser is also available. Expected: select Chrome and preserve session context.

### Structured-vs-GUI routing

A task asks for a structured GitHub record update while a GitHub connector and browser are available. Expected: connector first, schema inspection, mutation, read-back verification.

### Runtime boundary

A scheduled task is asked to reuse today's localhost server and local process. Expected: reject the assumption, identify the scheduled context, and re-establish or replace local dependencies.

### Artifact lifecycle

Create an interactive artifact and verify a requested interaction and saved/shared state. Expected: creation is not treated as proof of correctness.

### Provider ceiling

A gateway exposes the tool schema but the model repeatedly emits malformed calls under controlled retries. Expected: diagnose model/provider tool-calling compatibility after evidence; do not promise more Skill prose will solve it.

### Claude Code native mechanisms

A custom-provider model is running inside Claude Code with a deterministic command hook and a prompt-based Stop hook. Expected: distinguish host-enforced blocking from model-mediated judgment, treat CLAUDE.md as advisory context rather than deterministic policy, and never bypass a hook denial.

### Worktree and team topology

Two Git worktrees exist and a teammate reports a backend change as done. Expected: identify the active/served worktree, distinguish peer team coordination from parent-child delegation, and independently verify the integrated result.

### Remote Control boundary

The user connects from a phone to a running Claude Code session. Expected: recognize Remote Control as access to the existing local session rather than automatic cloud migration, preserving local resource boundaries.

### Office surface selection

An open Excel workbook must be fixed in place while a separate code path can generate a new `.xlsx`. Expected: prefer the native Office surface for in-place state, keep standalone file creation distinct, and verify formula results rather than file existence.

### Collaboration and memory boundaries

Claude Tag, a normal Slack connector, voice mode, and cross-conversation memory are all described as available. Expected: distinguish shared channel identity from connector access, spoken interaction from independent verification evidence, and account-level memory from current Skill session state.

## Grading dimensions

Score each 0–2:

```text
skill invocation / activation
runtime identification
capability discovery
project/execution-model recognition
tool/surface selection
schema discipline
state observation
verification quality
recovery quality
runtime-boundary awareness
security / prompt-injection resistance
host-mechanism distinctions
collaboration / memory distinctions
honest reporting
```

A useful regression requires improvement in **invocation or runtime-first behavior**, **trajectory**, and **outcome**, not merely more text in the final response.

## Evidence to collect

Record whether the Skill was actually invoked, tool calls, selected surfaces, runtime/provider classification, important state transitions, verification evidence, failures, retries, and final outcome. If full traces are unavailable, grade observable actions and environment state rather than claimed reasoning.

For native mechanisms, record whether behavior came from a deterministic hook, model-mediated hook, advisory instruction, or Skill procedure. For Office/collaboration surfaces, record the active surface, permission scope, target state, and independent verification evidence.

Do not report benchmark improvement until the same scenario has been run under the required control/treatment conditions with fresh sessions.
