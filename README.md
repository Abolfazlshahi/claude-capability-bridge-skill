<div align="center">

# Claude Capability Bridge Skill

### Teach custom-provider models the **workflow knowledge** needed to operate agentic tools reliably.

<img src="./assets/bridge-overview.svg" alt="Claude Capability Bridge overview" width="100%" />

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-claude--capability--bridge-8b5cf6?style=for-the-badge)](./SKILL.md)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088ff?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-34d399?style=for-the-badge)](./LICENSE)

**Discover → Select → Execute → Observe → Verify → Recover**

</div>

---

## What problem does this solve?

A model can have access to the same browser, filesystem, shell, MCP tools, connectors, and other runtime capabilities as a strong native agent and still use them poorly.

The missing piece is often **procedural knowledge**: knowing which surface to choose, how to sequence calls, how to preserve state, how to diagnose failure, and what evidence is sufficient to say *done*.

This Skill turns those behaviors into reusable procedures for Claude Desktop/Cowork-like and Claude Code-style Agent Skills runtimes.

> **Core invariant:** capability exposed ≠ capability understood ≠ task completed ≠ task verified.

---

## Why this is different

| Without the bridge | With the bridge |
|---|---|
| May see tools without knowing when to use them | Discovers the live capability surface first |
| Can choose a plausible but wrong tool | Selects the narrowest reliable surface for the task |
| May invent arguments or rely on stale assumptions | Reads the current tool contract before unfamiliar calls |
| May stop after a process starts or a page loads | Verifies the actual acceptance criterion |
| May repeat the same failed call | Classifies the failure and changes a material variable |
| May confuse runtime, gateway, and model failures | Attributes failures to the correct layer |
| May claim success from partial evidence | Reports verified, blocked, failed, and unknown states separately |

**Important:** this table describes the Skill's intended behavioral effect. It is **not a measured benchmark result**. Use the included evaluation suite to test the effect on your model/runtime.

<img src="./assets/before-after.svg" alt="Before and after comparison" width="100%" />

---

## How it works

<img src="./assets/workflow.svg" alt="Capability Bridge workflow" width="100%" />

The main Skill keeps the execution discipline compact and routes deeper procedures to references only when needed:

```text
runtime discovery
      ↓
capability + permission check
      ↓
tool / surface selection
      ↓
live schema inspection
      ↓
ACT → OBSERVE → DECIDE
      ↓
acceptance verification
      ↓
recovery or escalation
      ↓
evidence-backed report
```

---

## Custom-provider support

This is the part closest to the original motivation of the project.

<img src="./assets/provider-architecture.svg" alt="Custom provider architecture" width="100%" />

A custom endpoint or gateway can make an application **transport-compatible** without making the underlying model **behaviorally equivalent** to an Anthropic model.

The Skill therefore distinguishes at least five layers:

| Layer | Question |
|---|---|
| Model | Can the model reason, ground visually, and emit reliable tool calls? |
| Skill | Does it have the procedural knowledge for the workflow? |
| Runtime | Are the actual tools, context, permissions, and dispatch mechanisms exposed? |
| Transport / provider | Does the API/gateway preserve the required protocol and features? |
| Environment | Do the files, processes, browser state, network, and external systems exist? |

For Claude Code-style custom endpoints, the repository specifically covers `ANTHROPIC_BASE_URL`, custom model configuration, capability declarations, gateway limitations, and the distinction between **tool discovery failures** and **model tool-use failures**.

One concrete example is MCP Tool Search: non-first-party endpoints can disable or alter Tool Search behavior because a gateway may not preserve the protocol features required for tool references. That is an endpoint/runtime issue—not proof that the model ignored an available tool.

See [`references/custom-provider-transport.md`](./references/custom-provider-transport.md).

---

## Web-app verification: the flagship workflow

The bridge is especially useful for coding agents that need to prove a web app actually works.

<img src="./assets/webapp-verification.svg" alt="Web app verification pipeline" width="100%" />

The verification chain is deliberately layered:

```text
process started
   ↓
port actually listening
   ↓
HTTP responding
   ↓
app rendered / hydrated
   ↓
critical user journey exercised
   ↓
feature behavior verified
```

So:

```text
process running ≠ server ready ≠ page correct ≠ feature works
```

For browser-centric tasks the Skill also distinguishes the built-in browser from the user's existing Chrome context, avoids assuming shared cookies/tabs, and treats webpage instructions as untrusted content.

---

## Capability coverage

The project focuses on **public capability classes**, not private tool names or hidden system prompts.

| Area | What the bridge teaches |
|---|---|
| Browser & Chrome | surface selection, navigation, localhost testing, state separation |
| Computer use | GUI escalation, short observable action loops |
| MCP & connectors | schema-first use, mutation/read-back, trust boundaries |
| Local MCP / Desktop Extensions | local-vs-remote execution and permissions |
| Projects & files | project knowledge vs live filesystem vs Git state |
| Shell & code | deterministic commands, servers, tests, readiness |
| Skills & Plugins | progressive disclosure and specialization |
| Artifacts & interactive apps | creation vs rendered/behavioral verification |
| Subagents & long-running work | bounded delegation and context isolation |
| Scheduled / remote work | fresh execution context and local/cloud boundaries |
| Security | permissions, authorization, prompt injection, least privilege |
| Recovery | classify → isolate → change → retry → verify |
| Evaluation | controlled A/B attribution instead of documentation-size claims |

The maintained public map lives in [`references/claude-desktop-current-map.md`](./references/claude-desktop-current-map.md).

---

## Evaluation: measure behavior, not file count

The repository deliberately does **not** claim that the Skill improves every model. Effectiveness should be demonstrated empirically.

Run the same task with:

```text
SAME MODEL
SAME HOST
SAME TOOLS
SAME PROVIDER CONFIG
SAME WORKSPACE
SAME TASK

      ┌───────────────┐
      │   BRIDGE OFF  │
      └───────┬───────┘
              │
              │ compare traces
              │
      ┌───────▼───────┐
      │   BRIDGE ON   │
      └───────────────┘
```

Measure things such as:

- tool-selection accuracy
- schema-valid call rate
- verification depth
- unnecessary calls / retries
- recovery success
- false-success rate
- safety / authorization failures

The benchmark suite is in [`benchmarks/`](./benchmarks/) and structured evaluations are in [`evals/`](./evals/).

> **No fake percentages:** until real paired runs are recorded, any before/after improvement shown here is a design expectation, not experimental data.

---

## Install

This repository is a distribution/project repository; the actual Skill name is `claude-capability-bridge`.

```bash
python3 scripts/package_skill.py
```

This produces:

```text
dist/claude-capability-bridge/
```

Install that generated directory using the host's Agent Skills mechanism. In hosts that expose Skills as slash commands, the expected invocation is:

```text
/claude-capability-bridge
```

Installation does **not** create tools or grant permissions.

---

## Repository structure

```text
claude-capability-bridge-skill/
├── SKILL.md                         # compact procedural entry point
├── references/                      # deep procedures + public capability map
├── evals/                           # structured model-facing evaluations
├── benchmarks/                      # scenarios + scoring guidance
├── scripts/
│   ├── validate_skill.py            # repository checks
│   └── package_skill.py             # builds strict Skill-shaped package
├── assets/                          # README visuals
└── tests/                           # focused local test scenarios
```

The project follows progressive disclosure:

```text
metadata → SKILL.md → relevant reference → execution → verification
```

---

## Design boundaries

### The Skill can teach

`capability awareness` · `tool routing` · `schema discipline` · `workflow sequencing` · `state tracking` · `verification` · `recovery` · `security boundaries` · `evidence-based reporting`

### The Skill cannot create

`browser runtime` · `computer-use runtime` · `MCP server` · `filesystem mount` · `network access` · `permissions` · `provider protocol compatibility` · `host slash-command registration`

That boundary is a core design rule, not a footnote.

---

## Validation

Run the repository validator and package builder locally:

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py
```

For strict Agent Skills conformance, validate the generated package with the official `skills-ref` validator when available.

GitHub Actions also checks the repository and packaged Skill shape.

---

## Documentation map

Start here:

| Document | Purpose |
|---|---|
| [`SKILL.md`](./SKILL.md) | Main procedural bridge |
| [`custom-provider-transport.md`](./references/custom-provider-transport.md) | Custom endpoints, gateways, provider boundaries |
| [`claude-desktop-current-map.md`](./references/claude-desktop-current-map.md) | Current public capability inventory |
| [`webapp-verification.md`](./references/webapp-verification.md) | End-to-end web-app verification |
| [`browser-workflows.md`](./references/browser-workflows.md) | Browser / Chrome procedures |
| [`mcp-and-connectors.md`](./references/mcp-and-connectors.md) | Structured integration workflows |
| [`runtime-boundaries.md`](./references/runtime-boundaries.md) | Local/cloud and execution-surface boundaries |
| [`evaluation-and-attribution.md`](./references/evaluation-and-attribution.md) | How to prove the Skill actually helped |
| [`source-notes.md`](./references/source-notes.md) | Primary-source provenance and maintenance |

---

<div align="center">

### The goal

**Don't simulate agentic competence. Discover the real runtime, use the right surface, verify the real outcome, and recover safely.**

MIT License · Open source · Evidence over hype

</div>
