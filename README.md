# Claude Capability Bridge Skill

A procedural capability bridge for third-party/custom-provider models running in Claude Desktop-like agent runtimes.

## Why this exists

Anthropic's models can arrive with strong built-in procedural familiarity: they often know when to use a connector, when to execute code, when to open a browser, when to escalate to computer use, and when to verify the user-facing result. A custom provider can expose the same runtime tools while lacking those learned workflows.

This Skill makes those procedures explicit.

## What it covers

- capability discovery and routing
- filesystem and code/shell execution
- browser and Chrome workflow selection
- localhost web-app launch and verification
- console/network-aware debugging
- computer-use escalation
- MCP/connectors and result verification
- Skills and Plugins as procedural packaging
- project knowledge vs live filesystem state
- evidence-based verification
- failure recovery and retry discipline
- security, permissions, secrets, and prompt-injection defense
- Claude Desktop/Cowork-oriented orchestration patterns

## Design boundary

This project is a **knowledge/workflow layer**, not a runtime implementation. It cannot create a browser, computer-use tool, MCP server, filesystem mount, or code executor that the host has not exposed.

Its central invariant is:

> Capability available ≠ capability understood ≠ task completed ≠ task verified.

## Layout

```text
SKILL.md
references/
  browser-workflows.md
  capability-model.md
  code-and-shell.md
  computer-use.md
  desktop-workflows.md
  failure-recovery.md
  mcp-and-connectors.md
  projects-and-files.md
  security-and-permissions.md
  skills-and-plugins.md
  verification.md
  webapp-verification.md
  README.md
```

## Installation

Install the repository as an Agent Skill according to the host runtime's Skill installation mechanism. The required entry point is `SKILL.md`.

## Scope

The repository intentionally models behavior and decision rules instead of pretending to reproduce Anthropic's private system prompts or proprietary internal implementation. It should be updated when public runtime behavior, tooling, or the Agent Skills specification changes.

## Verification philosophy

For software tasks, the default completion loop is:

```text
inspect → implement → launch → browser-test → diagnose → repair → deterministic checks → verify → report
```

Browser verification is user-facing evidence; tests/builds are deterministic evidence. Neither automatically substitutes for the other.
