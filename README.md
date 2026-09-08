# Claude Capability Bridge Skill

> A procedural bridge for third-party and custom-provider models running inside Claude Desktop/Cowork-like Agent Skills runtimes.

[![Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20Capability%20Bridge-6f42c1)](./SKILL.md)
[![CI](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Abolfazlshahi/claude-capability-bridge-skill/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## The problem

A model can be excellent at reasoning and still be a weak agent inside a desktop runtime.

Claude Desktop/Cowork and Claude Code can expose files, shell/code execution, browsers, Chrome, computer use, MCP/connectors, Projects, Skills, Plugins, Artifacts, interactive apps, subagents, and scheduled or remote execution. Seeing a tool is not the same thing as knowing when to use it, how to sequence it, how to preserve state, how to recover, or what evidence is sufficient to declare success.

This project turns that missing workflow knowledge into a portable Agent Skill.

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
HOST / SESSION MODEL
        ↓
CAPABILITY DISCOVERY
        ↓
SCHEMA + PERMISSION CHECK
        ↓
ROUTE TO NARROWEST RELIABLE SURFACE
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

The bridge covers public capability classes such as browser/Chrome, computer use, MCP/connectors, local MCP/Desktop Extensions, Projects, Skills/Plugins, Artifacts/interactive surfaces, subagents, schedules, and local/cloud execution boundaries. Exact availability is always runtime-, plan-, platform-, admin-, endpoint-, and rollout-dependent.

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
INSPECT UI / TELEMETRY
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

## Custom-provider architecture

This is the part most directly tied to the original motivation of the project.

```text
Claude Desktop / Claude Code
          │
          ▼
   agent runtime + tools
          │
          ▼
 Anthropic API contract
          │
          ▼
 gateway / proxy / provider adapter
          │
          ▼
   third-party model
```

A compatible gateway does **not** make the target model behaviorally equivalent to Anthropic's models.

Claude Code documents `ANTHROPIC_BASE_URL` as an endpoint override for proxies and LLM gateways. It also documents custom model entries and provider-specific capability declarations. These are transport/configuration mechanisms; the target model still has its own tool-calling, vision, context, reasoning, and protocol capabilities.

One especially important consequence is MCP Tool Search: when `ANTHROPIC_BASE_URL` points to a non-first-party host, Claude Code disables Tool Search by default because many proxies do not forward `tool_reference` blocks. `ENABLE_TOOL_SEARCH=true` is an explicit override for compatible gateways; it is not a generic fix for every provider.

That distinction matters to the bridge:

```text
tool not discovered because endpoint/runtime mode changed
                 ≠
model saw the tool and ignored it
```

See [`references/custom-provider-transport.md`](./references/custom-provider-transport.md).

## Capability model

```text
┌─────────────────────────────┐
│ MODEL                       │
│ reasoning + tool ability    │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ SKILL                       │
│ procedural knowledge        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ RUNTIME                     │
│ tools + context + policy    │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ TRANSPORT / PROVIDER        │
│ API + gateway + model       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ ENVIRONMENT                 │
│ files + processes + network │
│ browser + services          │
└─────────────────────────────┘
```

A Skill primarily changes the procedural layer. It cannot create a missing browser, shell, MCP server, filesystem mount, network path, permission, or host integration.

## Why it can be useful

The claim is intentionally narrow and testable:

```text
SAME HOST
SAME TOOLS
SAME TASK
SAME PROVIDER
        │
        ├── BRIDGE OFF
        │
        └── BRIDGE ON
               ↓
        compare tool traces
```

Useful metrics include:

```text
tool-selection accuracy
schema-valid call rate
state-tracking accuracy
verification completion
false-success rate
recovery success
unnecessary-call rate
critical safety failures
```

The repository treats benchmark evidence—not Skill size—as the criterion for effectiveness.

## Activation

When the host exposes installed Skills as slash commands:

```text
/claude-capability-bridge
```

The host owns command registration. Installing this repository does not itself create a command or grant permissions.

After activation, the model should build a lightweight session capability map and apply the relevant procedures. It should not dump the entire map into the conversation unless useful.

## Installation

This GitHub repository is a distribution/project repository. The actual Skill name is `claude-capability-bridge`.

Build the spec-shaped Skill directory:

```bash
python3 scripts/package_skill.py
```

Output:

```text
dist/claude-capability-bridge/
```

Then install that generated directory with the host's Agent Skills mechanism.

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
│   ├── claude-desktop-current-map.md
│   ├── custom-provider-transport.md
│   ├── runtime-boundaries.md
│   ├── activation-and-memory.md
│   ├── session-memory.md
│   ├── capability-model.md
│   ├── capability-catalog.md
│   ├── capability-handshake.md
│   ├── tool-schema-literacy.md
│   ├── tool-use-patterns.md
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
    ├── scenarios.md
    └── custom-provider-transport.md
```

## Progressive disclosure

```text
metadata
   ↓
SKILL.md
   ↓
relevant reference
   ↓
recipe / script
   ↓
execution
   ↓
verification
```

The main Skill stays focused on activation, capability routing, state, verification, and recovery. Deep procedures remain in references.

## Validation

Repository checks:

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py
```

For spec conformance, use the official `skills-ref` validator against `dist/claude-capability-bridge` when available.

## Evaluation

The project has both structured evaluations and broader benchmark scenarios. The important comparison is controlled before/after behavior under the same runtime and provider.

A documentation-heavy Skill without a measurable behavioral improvement is not considered a finished success.

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
✓ security boundaries
✓ evidence-based reporting

CANNOT CREATE
✗ browser runtime
✗ computer-use runtime
✗ MCP server
✗ filesystem mount
✗ network access
✗ permissions
✗ provider protocol compatibility
✗ host slash-command registration
```

## Maintenance

When Claude Desktop/Cowork/Claude Code, browser surfaces, MCP/connectors, Skills, Plugins, Artifacts, provider-routing behavior, or the Agent Skills specification changes:

```text
refresh current capability map
        ↓
update affected procedure
        ↓
update provider boundary notes
        ↓
update evals / benchmarks
        ↓
run validator + package
        ↓
run controlled model evaluation
```

See [`references/source-notes.md`](./references/source-notes.md) for the primary-source set.

## License

MIT — see [`LICENSE`](./LICENSE).
