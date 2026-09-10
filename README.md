<div align="center">

# Claude Capability Bridge Skill

### Teach custom-provider models the **workflow knowledge** needed to operate agentic tools reliably.

<p>
  <img src="./assets/benner.jpeg" alt="Claude Capability Bridge overview" width="100%" />
</p>

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-claude--capability--bridge-8b5cf6?style=for-the-badge)](./SKILL.md)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088ff?style=for-the-badge&logo=githubactions&logoColor=white)](./.github/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-34d399?style=for-the-badge)](./LICENSE)

**Detect Runtime → Discover → Remediate → Route → Execute → Verify → Recover**

</div>

---

## What problem does this solve?

A model can have access to the same browser, filesystem, shell, MCP tools, connectors, and other runtime capabilities as a strong native agent and still use them poorly.

The missing piece is often **procedural knowledge**: first identifying the actual runtime and execution boundary, then choosing the right interface, preserving state, diagnosing missing capabilities, and gathering enough evidence to say *done*.

This Skill turns those behaviors into reusable procedures for Claude Code CLI, Claude Desktop/Cowork-style, and other Agent Skills-compatible runtimes.

> **Core invariant:** capability exposed ≠ capability understood ≠ task completed ≠ task verified.

---

## Runtime-first architecture

Before routing a tool or launching a project, the bridge establishes the operating profile:

```text
HOST: CLI / Desktop / Cowork / Cloud / Remote / Other
EXECUTION: local / cloud / remote / mixed
PROVIDER: first-party / third-party / unknown
CAPABILITIES: shell / files / Git / browser / Chrome / MCP / GUI / etc.
             ↓
       discover relevant capability
             ↓
       classify missing capability
             ↓
       repair only when possible
             ↓
       route → execute → verify
```

CLI is treated as a first-class profile rather than a Desktop variant. Browser/Chrome availability is checked separately from shell or project execution, and provider restrictions remain a separate axis.

See [`references/runtime-detection-and-profiles.md`](./references/runtime-detection-and-profiles.md), [`references/claude-code-cli-operating-model.md`](./references/claude-code-cli-operating-model.md), and [`references/capability-remediation.md`](./references/capability-remediation.md).

---

## Before vs After

| Without the bridge | With the bridge |
|---|---|
| May assume the wrong host or execution location | Detects runtime and execution boundary first |
| May see tools without knowing when to use them | Discovers the live capability surface relevant to the task |
| Can choose a plausible but wrong tool | Selects the narrowest authoritative surface |
| May stop at “not connected” | Classifies the missing capability and attempts justified remediation |
| May invent arguments or rely on stale assumptions | Reads current contracts and invalidates stale observations |
| May confuse a running process with a working app | Verifies readiness, rendered state, and critical behavior |
| May claim success from partial evidence | Reports verified, blocked, failed, and unknown states separately |

<p align="center">
  <img src="./assets/before-after.svg" alt="Before and after workflow comparison" width="100%" />
</p>

> **Honesty note:** this table describes intended behavior, not measured performance. Empirical claims belong in the benchmark results.

---

## How it works

```text
1. Runtime detection
2. Execution/provider profile
3. Capability discovery + safe probing
4. Missing-capability classification/remediation
5. Authoritative tool/surface selection
6. Short observable execution loops
7. Direct verification
8. Recovery / fallback
9. Evidence-backed report
```

The main `SKILL.md` stays compact. Detailed procedures are progressively loaded from [`references/`](./references/) only when a task enters that capability family.

---

## Custom-provider support

A custom endpoint or gateway can be transport-compatible without making the underlying model behaviorally equivalent to an Anthropic model.

| Layer | Question |
|---|---|
| **Model** | Can the model reason, use required modalities, and emit reliable tool calls? |
| **Skill** | Does it have the procedural knowledge required by the workflow? |
| **Runtime** | Are tools, context, permissions, and dispatch exposed? |
| **Transport / provider** | Does the gateway preserve the required protocol features? |
| **Environment** | Do files, processes, browser state, network, and services actually exist? |

The bridge explicitly distinguishes provider/runtime limits from procedural failures. A provider-unsupported browser integration should not trigger endless local setup attempts.

<p align="center">
  <img src="./assets/provider-architecture.svg" alt="Custom-provider architecture" width="100%" />
</p>

---

## Web-app verification

The bridge is especially useful when an agent builds or repairs a web app and must prove that the **real user flow** works.

```text
project recognition
   ↓
launch contract
   ↓
process running
   ↓
port listening / HTTP ready
   ↓
browser surface selected
   ↓
critical user journey exercised
   ↓
feature behavior verified
```

So:

```text
process running ≠ server ready ≠ page correct ≠ feature works
```

A server-side template opened with `file://` is not equivalent to running the application.

<p align="center">
  <img src="./assets/webapp-verification.svg" alt="Web-app verification workflow" width="100%" />
</p>

---

## Capability coverage

| Area | What the bridge teaches |
|---|---|
| Runtime detection | CLI/Desktop/Cowork/cloud/remote classification and execution profiles |
| Browser & Chrome | surface selection, localhost testing, browser context separation |
| Capability remediation | classify → repair → re-probe → fallback instead of “not connected” |
| Computer use | GUI escalation and short observable action loops |
| MCP & connectors | schema-first use, mutation/read-back, trust boundaries |
| Projects & files | project knowledge vs live filesystem vs Git state |
| Shell & code | deterministic commands, servers, tests, readiness |
| Skills & Plugins | progressive disclosure, host controls, invocation boundaries |
| Artifacts & interactive apps | creation vs rendered/behavioral verification |
| Subagents & long-running work | bounded delegation and context isolation |
| Scheduled / remote work | fresh execution context and local/cloud boundaries |
| Security | permissions, authorization, prompt injection, least privilege |
| Evidence & recovery | direct proof, failure classification, bounded retries |

---

## Always-on bootstrap

A portable Skill cannot universally force its own invocation. For Claude Code, the repository includes a practical bootstrap path for host-owned persistent context and `SessionStart` hooks:

```text
CLAUDE.md reminder
        +
SessionStart hook (when configured)
        ↓
bridge protocol is present before complex work
        ↓
Skill supplies the detailed procedure when invoked
```

Concrete examples live under [`bootstrap/`](./bootstrap/) and [`references/claude-code-bootstrap-kit.md`](./references/claude-code-bootstrap-kit.md).

The bootstrap does **not** create tools, bypass permissions, or make a third-party provider support an unsupported host feature.

---

## Evaluation & benchmarking

The repository deliberately does **not** claim that the Skill improves every model. Effectiveness should be demonstrated empirically.

For forgetting and runtime-first behavior, compare:

```text
CONTROL: no bridge
TREATMENT A: bridge Skill only
TREATMENT B: bridge Skill + always-on bootstrap
```

Keep model, host, tools, provider config, workspace, task wording, and success criteria constant. Grade the trajectory and final state separately.

Useful metrics include runtime identification before host-specific routing, tool-selection accuracy, schema-valid call rate, recovery quality, verification depth, false-success rate, unnecessary retries, and safety/authorization failures.

See [`benchmarks/README.md`](./benchmarks/README.md), [`benchmarks/behavioral-benchmark.md`](./benchmarks/behavioral-benchmark.md), and [`evals/evals.json`](./evals/evals.json).

> **No fake percentages:** until paired runs are recorded, improvement is an engineering hypothesis, not experimental data.

---

## Installation

This repository is a distribution/project repository; the actual Skill name is `claude-capability-bridge`.

```bash
python3 scripts/package_skill.py
```

This produces:

```text
dist/claude-capability-bridge/
```

Install that generated directory using your host's Agent Skills mechanism.

When the host exposes Skills as slash commands:

```text
/claude-capability-bridge
```

Validate locally with:

```bash
python3 scripts/validate_skill.py
```

---

## Repository structure

```text
claude-capability-bridge-skill/
├── SKILL.md
├── references/
├── benchmarks/
├── evals/
├── scripts/
├── tests/
├── bootstrap/                 # optional Claude Code host bootstrap examples
├── assets/
├── i18n/
└── LICENSE
```

The project follows progressive disclosure:

```text
metadata → SKILL.md → relevant reference → execution → verification
```

---

## Design boundaries

### The Skill can teach

`runtime awareness` · `capability discovery` · `tool routing` · `schema discipline` · `workflow sequencing` · `state tracking` · `verification` · `recovery` · `security boundaries` · `evidence-based reporting`

### The Skill cannot create

`browser runtime` · `computer-use runtime` · `MCP server` · `filesystem mount` · `network access` · `permissions` · `provider protocol compatibility` · `missing model capabilities` · `host hook registration`

That boundary is a core design rule.

---

## Validation

Run repository checks locally:

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py
bash -n bootstrap/session-start.sh
python3 -m json.tool bootstrap/settings.json.example
```

For strict Agent Skills conformance, validate the generated package with the official `skills-ref` validator when available.

GitHub Actions runs the structural, packaging, Agent Skills, evaluation, and benchmark-definition checks.

---

## Documentation map

| Document | Purpose |
|---|---|
| [`SKILL.md`](./SKILL.md) | Main runtime-first procedural bridge |
| [`Runtime detection`](./references/runtime-detection-and-profiles.md) | Host/execution/provider profiling |
| [`CLI operating model`](./references/claude-code-cli-operating-model.md) | CLI-first routing and browser/provider boundaries |
| [`Bootstrap kit`](./references/claude-code-bootstrap-kit.md) | Always-on Claude Code context/hook path |
| [`Capability remediation`](./references/capability-remediation.md) | Diagnose and repair missing integrations |
| [`Custom Provider`](./references/custom-provider-transport.md) | Endpoint, gateway and provider boundaries |
| [`Web App Verification`](./references/webapp-verification.md) | End-to-end web-app verification |
| [`Browser Workflows`](./references/browser-workflows.md) | Browser / Chrome procedures |
| [`MCP & Connectors`](./references/mcp-and-connectors.md) | Structured integration workflows |
| [`Evaluation`](./references/evaluation-and-attribution.md) | Controlled behavioral attribution |
| [`References`](./references/README.md) | Full reference map |

---

## Telegram

Project updates, releases, experiments and more:

<p align="center">
  <a href="https://t.me/pythash"><strong>@pythash</strong></a>
</p>

---

## Language versions

| Language | README |
|---|---|
| English | [`README.md`](./README.md) |
| 简体中文 | [`README_ZH.md`](./i18n/README_ZH.md) |
| Español | [`README_ES.md`](./i18n/README_ES.md) |
| हिन्दी | [`README_HI.md`](./i18n/README_HI.md) |
| العربية | [`README_AR.md`](./i18n/README_AR.md) |
| Français | [`README_FR.md`](./i18n/README_FR.md) |
| فارسی | [`README_FA.md`](./i18n/README_FA.md) |

---

## License

Claude Capability Bridge Skill is released under the **[MIT License](./LICENSE)**.

---

<div align="center">

### The goal

**Don't simulate agentic competence. Detect the real runtime, use the right surface, verify the real outcome, and recover safely.**

[GitHub](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [Issues](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/issues) · [Discussions](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/discussions) · [Telegram](https://t.me/pythash) · [MIT License](./LICENSE)

</div>
