---
id: claude-code
title: Host profile - Claude Code (CLI / IDE terminal)
stability: relatively stable host contract; version-dependent items are marked
---

# Host profile: Claude Code

**This file describes contracts, not live state.** Nothing here asserts that a
tool exists, that a permission is granted, that the network is reachable, or
that any integration is connected in your current run. Those facts come only
from the evidence of the run you are in.

## How to confirm you are here

Evidence that usually indicates this profile:

- the host exposes shell/file/edit tooling against a real working directory;
- there is a project directory and often a git checkout;
- session lifecycle events exist (session start, compaction, resume, fork);
- host-owned mechanisms are configured in files, not created by you at runtime.

If the evidence is mixed, say so and use `profiles/generic.md` instead of
guessing.

## Execution environment

- Commands run on the machine that started the CLI, in a real filesystem, with
  the user's own environment and credentials.
- The working directory is authoritative. Resolve it from live evidence rather
  than assuming a repository root.
- Side effects are real: writes, deletes, installs, pushes, and network calls
  affect the user's machine and accounts.
- Long-running processes must be started so control returns. A blocking
  foreground server stalls the whole session.

## How tools become known

1. The host's exposed tool list for this session is the only authoritative
   source of what is callable.
2. The tool's own schema is the only authoritative source of arguments.
3. Names in documentation, in this repository, or from another host are
   **conceptual capability names**. They are not callable tool names.

When an operation is not in the exposed list, do not synthesize it. Classify:
not exposed, not configured, not running, or not permitted.

## Permissions

- Permission is separate from availability. A tool can be visible and still be
  refused at call time.
- Approval decisions belong to the host and the user. An earlier approval does
  not authorize a later, broader action.
- A denial is a result, not an obstacle to route around. Never look for an
  alternate path to do the thing that was just denied.
- Cached state about a permission is never a substitute for the host's current
  decision.

## Files, artifacts, and delivery

- Writing a file into the working tree is not delivery. The user receives
  something only through a delivery path the host actually provides.
- A local filesystem path is not a download link, and `file://` is not a served
  application.
- See `cards/artifacts-delivery.md`.

## Browser and GUI

- Browser automation, screenshots, and GUI control are **optional add-ons**,
  commonly absent. Do not plan a browser step before you have evidence that a
  browser path exists in this run.
- See `cards/browser-webapp.md` and `cards/computer-use.md`.

## Host-owned mechanisms (version-dependent)

These are configured by the user, not created by a model at runtime:

- project instruction files and skills;
- hooks bound to lifecycle events;
- subagents and delegated runs;
- MCP servers and connectors;
- permission rules and allowlists;
- output styles and status line.

Which event names, flags, and settings exist depends on the installed host
version. If a mechanism is not present in this installation, report that and
stop; do not fabricate a config surface. See
`references/claude-code-native-mechanisms.md` and
`references/claude-code-cli-operating-model.md`.

## Context lifecycle

- Long sessions can be compacted. After compaction, earlier procedural guidance
  and earlier observations may be gone or summarized.
- Clear starts a new context. Fork creates a sibling context that does **not**
  inherit your running processes, browser sessions, or authenticated state.
- Resume may or may not restore prior evidence. Treat prior observations as
  STALE until re-observed.
- See `cards/delegation-context.md`.

## Provider and gateway (version- and deployment-dependent)

- The model behind this host may be a third-party model reached through a
  gateway.
- Message-format compatibility with the Anthropic Messages API does **not**
  imply the same caching, tool, or streaming semantics.
- Cache behaviour, TTL, minimum cacheable length, and billing are owned by the
  provider and the gateway, never by this Skill.
- See `docs/cache-contract.md`, `references/provider-adaptation.md`, and
  `references/custom-provider-transport.md`.

## What this profile must never be read as

- proof that a browser, MCP server, or network egress exists;
- proof that any specific tool name is callable in this session;
- proof that a permission is granted;
- a substitute for reading the live tool contract.
