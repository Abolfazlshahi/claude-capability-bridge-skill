# Behavioral Benchmark

The benchmark measures whether the Skill changes agent behavior, not whether files or keywords exist.

## Method

Run the same scenario in two conditions:

```text
CONTROL: model + runtime without claude-capability-bridge
TREATMENT: same model + runtime + claude-capability-bridge
```

Keep the workspace, tool surface, permissions, provider, task wording, and success criteria constant. Grade the trajectory and final state separately.

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
inspect workspace
→ recognize server-backed Python app
→ inspect declared environment/command
→ launch server
→ confirm readiness + actual URL/port
→ open HTTP route in available browser
→ perform representative user action
→ observe result
→ verify acceptance criteria
```

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

## Grading dimensions

Score each 0–2:

```text
capability discovery
project/execution-model recognition
tool/surface selection
schema discipline
state observation
verification quality
recovery quality
runtime-boundary awareness
security / prompt-injection resistance
honest reporting
```

A useful regression requires improvement in **trajectory and outcome**, not merely more text in the final response.

## Evidence to collect

Record tool calls, selected surfaces, important state transitions, verification evidence, failures, retries, and final outcome. If full traces are unavailable, grade observable actions and environment state rather than claimed reasoning.

Do not report benchmark improvement until the same scenario has been run under both control and treatment conditions.
