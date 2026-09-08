# Claude Capability Bridge Skill

> A procedural bridge for third-party and custom-provider models running inside Claude Desktop/Cowork-like Agent Skills runtimes.

[![Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20Capability%20Bridge-6f42c1)](./SKILL.md)
[![CI](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## The problem

A model can be excellent at reasoning and still be a weak agent inside a desktop runtime.

The runtime may expose files, shell/code execution, browsers, Chrome, computer use, MCP/connectors, Projects, Skills, Plugins, Artifacts, interactive apps, subagents, and scheduled or remote execution. Seeing those tools is not the same thing as knowing **when to use them, how to sequence them, how to maintain state, how to recover, or what evidence is sufficient to call the task complete**.

Anthropic explicitly positions Skills as reusable procedural knowledge that complements Projects, MCP, prompts, and subagents. citeturn384783search0turn688364search4

This project turns that missing workflow knowledge into a portable Skill.

## Core invariant

```text
┌──────────────────────┐
│ Capability is exposed│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Model understands it │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Task reaches target  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Result is verified   │
└──────────────────────┘
```

**Capability available ≠ capability understood ≠ task completed ≠ task verified.**

## What the bridge teaches

```text
HOST MODEL
    ↓
CAPABILITY DISCOVERY
    ↓
SCHEMA / PERMISSION CHECK
    ↓
NARROWEST TOOL SELECTION
    ↓
EXECUTE
    ↓
OBSERVE
    ↓
ASSERT
    ↓
RECOVER IF NEEDED
    ↓
VERIFY
    ↓
REPORT EVIDENCE
```

It covers the important public capability classes documented for modern Claude Desktop/Cowork environments: built-in browser and Chrome, computer use, MCP/connectors, Desktop Extensions/local MCP, Projects, Skills/Plugins, Artifacts and interactive surfaces, subagents, scheduled tasks, and local/cloud execution boundaries. Exact availability remains runtime-, plan-, platform-, admin-, and rollout-dependent. citeturn384783search5turn384783search1turn688364search0

## The flagship workflow: web development

```text
UNDERSTAND
   ↓
INSPECT REPO
   ↓
BASELINE
   ↓
IMPLEMENT
   ↓
START SERVER
   ↓
CONFIRM REAL READINESS
   ↓
DISCOVER REAL URL/PORT
   ↓
OPEN BROWSER
   ↓
TEST CRITICAL USER JOURNEY
   ↓
INSPECT UI / CONSOLE / NETWORK
   ↓
DIAGNOSE
   ↓
PATCH
   ↓
RE-TEST FAILED ASSERTION
   ↓
DETERMINISTIC CHECKS
   ↓
VISUAL CHECK
   ↓
CLEANUP
   ↓
EVIDENCE REPORT
```

The bridge deliberately separates:

```text
process running
      ≠
server listening
      ≠
HTTP responding
      ≠
app hydrated
      ≠
page correct
      ≠
feature works
```

Claude's built-in Cowork browser can open sites, read pages, click, type, and fill forms inside the desktop app, while Claude in Chrome provides an existing-browser-context path. Those surfaces have different state and authentication boundaries. citeturn384783search4turn384783search7

## Capability model

```text
┌─────────────────────────────┐
│ MODEL                       │
│ reasoning + tool habits     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ SKILL                       │
│ procedural knowledge        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ RUNTIME                     │
│ tools + context + perms     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ ENVIRONMENT                 │
│ files + processes + network │
│ browser + external services │
└─────────────────────────────┘
```

A Skill can improve the **procedural layer**. It cannot manufacture a missing browser, shell, MCP server, permission, filesystem mount, or host integration.

## Why the Skill can be useful

The value proposition is narrow and testable:

```text
SAME RUNTIME
SAME TOOLS
SAME TASK
      │
      ├── MODEL WITHOUT BRIDGE
      │
      └── MODEL + BRIDGE
                ↓
          compare traces
```

We care about behavioral deltas such as:

```text
tool-selection accuracy
schema-valid calls
unnecessary calls
state-tracking accuracy
verification completion
false-success rate
recovery success
safety/authorization compliance
```

The repository therefore treats benchmark evidence—not file count—as the criterion for a successful Skill release.

## Current public capability map

The maintained map is in [`references/current-claude-desktop-map.md`](./references/current-claude-desktop-map.md). It deliberately models capability **classes** rather than private tool names.

Current public areas covered:

```text
Conversation / Projects
Skills / Plugins
Files / Git
Shell / Code Execution
Built-in Cowork Browser
Claude in Chrome
Computer Use
MCP / Remote Connectors
Local MCP / Desktop Extensions
Interactive Connector Apps
Artifacts
Subagents
Scheduled Tasks
Remote / Cross-Surface Sessions
Security / Permissions
Verification / Recovery
```

Anthropic's current documentation also makes the local/cloud boundary explicit: cloud Cowork sessions run in isolated cloud sandboxes, while local files and local integrations can be reached through the desktop app under the documented conditions. Scheduled tasks are separate cloud runs and should not be assumed to inherit live local state. citeturn688364search0turn384783search1turn384783search9

## Installation

This GitHub repository is a **distribution/project repository**, not a strict one-folder Skill checkout.

The Agent Skills specification requires the Skill's `name` to match its parent directory name. This repository intentionally keeps the repository name `claude-capability-bridge-skill` while the actual Skill name and slash command are `claude-capability-bridge`. citeturn688364search1

Build the spec-shaped installable directory:

```bash
python3 scripts/package_skill.py
```

The output is:

```text
dist/claude-capability-bridge/
```

Install that generated directory using the host's Skill installation mechanism. In a host that exposes Skills as slash commands, the expected invocation is:

```text
/claude-capability-bridge
```

Installation does not grant tools or permissions; the host still determines the actual runtime surface.

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── evals/
│   └── evals.json
├── benchmarks/
│   ├── README.md
│   └── scenarios.yaml
├── references/
│   ├── current-claude-desktop-map.md
│   ├── runtime-boundaries.md
│   ├── activation-and-memory.md
│   ├── capability-model.md
│   ├── capability-catalog.md
│   ├── capability-handshake.md
│   ├── tool-schema-literacy.md
│   ├── browser-workflows.md
│   ├── webapp-verification.md
│   ├── interactive-surfaces.md
│   ├── desktop-extensions.md
│   ├── computer-use.md
│   ├── mcp-and-connectors.md
│   ├── mcp-deep-dive.md
│   ├── async-subagents-and-remote.md
│   ├── skills-and-plugins.md
│   ├── projects-and-files.md
│   ├── provider-adaptation.md
│   ├── evaluation-and-attribution.md
│   ├── verification.md
│   ├── failure-recovery.md
│   ├── security-and-permissions.md
│   ├── task-recipes.md
│   ├── desktop-workflows.md
│   └── source-notes.md
├── scripts/
│   ├── validate_skill.py
│   └── package_skill.py
└── tests/
    └── scenarios.md
```

## Progressive disclosure

The project follows the Skill specification's intended loading pattern:

```text
metadata
   ↓
SKILL.md
   ↓
relevant reference
   ↓
script / recipe / asset
   ↓
execution
   ↓
verification
```

The main `SKILL.md` stays focused on routing and invariants; detailed procedures live in references. The official specification recommends keeping the main file under 500 lines and validating Skills with `skills-ref`. citeturn688364search1

## Validation

Repository validator:

```bash
python3 scripts/validate_skill.py
```

Spec-shaped package validator:

```bash
python3 scripts/package_skill.py
python3 -m pip install skills-ref
skills-ref validate dist/claude-capability-bridge
```

The GitHub Actions workflow runs repository checks and validates the generated installable Skill shape.

## Evaluation

The repository contains two complementary evaluation layers:

- `evals/evals.json` — structured model-facing evaluations.
- `benchmarks/scenarios.yaml` — broader scenario coverage for runtime/tool behavior.

Use paired baseline vs Skill-enabled runs under a controlled runtime. The Skill should only be considered effective when the trace shows repeatable improvement.

## Design boundaries

```text
CAN TEACH
✓ capability awareness
✓ tool routing
✓ schema discipline
✓ workflow sequencing
✓ state tracking
✓ verification
✓ recovery
✓ safety boundaries
✓ evidence-based reporting

CANNOT CREATE
✗ browser runtime
✗ computer-use runtime
✗ MCP server
✗ filesystem mount
✗ network access
✗ permissions
✗ host slash-command registration
```

## Maintenance

When Claude Desktop/Cowork, browser surfaces, MCP/connectors, Skills, Plugins, Artifacts, or the Agent Skills specification changes:

```text
refresh public capability map
        ↓
update affected reference
        ↓
update evals/benchmarks
        ↓
run validator + package
        ↓
run controlled model evaluation
```

See [`references/source-notes.md`](./references/source-notes.md) for the maintained primary-source list.

## License

MIT — see [`LICENSE`](./LICENSE).
