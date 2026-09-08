# Claude Capability Bridge Skill

A deep procedural capability bridge for third-party/custom-provider models running inside Claude Desktop-like Agent Skills runtimes.

## Purpose

Some models can reason about code and text well but lack strong procedural familiarity with an agentic desktop environment: which tool to choose, how to sequence actions, how to test a local web app in a browser, how to diagnose tool failures, and how to prove the requested result.

This Skill turns that implicit workflow knowledge into explicit, reusable procedures.

It is designed around one invariant:

> **Capability available ≠ capability understood ≠ task completed ≠ task verified.**

## Activation

When the host exposes installed Skills as slash commands, the expected invocation is:

```text
/claude-capability-bridge
```

The host controls command registration. Installation of this repository does not itself create a slash-command UI or grant new permissions.

Once the host reports that the Skill is active, its procedures become the model's working policy for the applicable task/session.

## What it teaches

### Host awareness

- model vs runtime vs tool vs environment boundaries;
- project knowledge vs live filesystem vs Git vs browser state;
- capability availability states and evidence tracking;
- permission and approval boundaries;
- process ownership and localhost readiness.

### Capability routing

- structured MCP/connectors before GUI when appropriate;
- filesystem/Git for source state;
- shell/code for deterministic operations;
- browser for user-facing web behavior;
- existing Chrome context when materially required;
- computer use as a GUI escalation path;
- Skills and Plugins as procedural packaging;
- scheduling/remote dispatch as orchestration when exposed.

### Web development

- inspect the existing project before modifying it;
- infer commands from repository configuration rather than memory;
- launch and detect the actual development server;
- open the real localhost URL;
- test critical user journeys;
- inspect browser-visible/runtime/network failures when supported;
- patch, reload, and re-test;
- combine browser evidence with deterministic checks;
- clean up agent-owned processes.

### Reliability

- explicit observation checkpoints;
- idempotence-aware retries;
- failure classification;
- one-material-variable recovery;
- acceptance-criteria verification;
- evidence-oriented completion reports;
- no fabricated tool use or verification.

### Safety

- least-privilege behavior;
- explicit authorization for consequential external side effects;
- credential/secret hygiene;
- prompt-injection resistance for web pages, documents, MCP results, and repository content.

## Repository map

```text
.
├── SKILL.md                         # Core routing/orchestration policy
├── README.md
├── LICENSE
├── references/
│   ├── activation-and-memory.md    # Slash invocation + session-scoped state
│   ├── browser-workflows.md        # Browser/Chrome selection and navigation
│   ├── capability-catalog.md       # Capability inventory
│   ├── capability-model.md         # Model/runtime/tool/environment boundary
│   ├── code-and-shell.md           # Deterministic execution and process control
│   ├── computer-use.md             # GUI escalation
│   ├── desktop-workflows.md        # Desktop/Cowork-oriented patterns
│   ├── failure-recovery.md         # Failure taxonomy and repair loops
│   ├── mcp-and-connectors.md       # Integration selection
│   ├── mcp-deep-dive.md            # MCP semantics and trust boundary
│   ├── projects-and-files.md       # Context/state separation
│   ├── provider-adaptation.md      # Custom-provider gap diagnosis
│   ├── security-and-permissions.md # Security and authorization
│   ├── skills-and-plugins.md       # Skill/plugin mechanics
│   ├── task-recipes.md             # Reusable high-level recipes
│   ├── tool-use-patterns.md        # General tool-call discipline
│   ├── verification.md             # Evidence model
│   └── webapp-verification.md      # End-to-end live app verification
├── scripts/
│   └── validate_skill.py            # Offline structural validator
└── tests/
    └── scenarios.md                # Model-facing behavioral scenarios
```

## Design boundary

This is intentionally a **knowledge/workflow layer**. It cannot create a browser, computer-use interface, MCP server, filesystem mount, shell, permission, or other runtime capability that the host does not expose.

The correct response to a missing runtime capability is honest fallback and explicit disclosure—not a fabricated claim.

## Progressive disclosure

`SKILL.md` is the routing layer. It points to focused references rather than forcing every detail into the first prompt context.

Typical flow:

```text
Skill metadata
   ↓
SKILL.md
   ↓
relevant reference
   ↓
optional script / recipe
   ↓
execution + verification
```

## Validation

Run:

```bash
python scripts/validate_skill.py
```

The validator performs offline structural checks; it does not prove that a particular Claude Desktop version exposes every capability described by the references.

## Scope and maintenance

This project models public, reproducible agent workflows. It does not claim to reproduce Anthropic's private system prompts or proprietary internal implementation.

When the host runtime, Claude Desktop capabilities, MCP behavior, or Agent Skills specification changes, update the capability catalog and affected workflows first, then revise `SKILL.md` routing if necessary.
