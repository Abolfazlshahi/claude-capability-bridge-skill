---
id: generic
title: Host profile - unknown or mixed host
stability: intentionally minimal; use when host evidence is incomplete
---

# Host profile: generic / unknown host

**This file describes contracts, not live state.** It proves nothing about
which tools exist, which permissions apply, or what is connected in your
current run.

Use this profile when the host cannot be identified with confidence, when the
evidence is mixed, or when you are running behind an unfamiliar gateway.

The correct behaviour here is **not** to guess a richer profile. It is to work
from the narrow set of facts you can actually observe.

## Starting assumptions

Assume nothing beyond this:

- you can read the conversation;
- you can call exactly the tools the host exposed for this session;
- every tool call may be refused;
- every capability not proven present is UNKNOWN, not absent and not available.

Do not assume: shell access, a writable filesystem, network egress, a browser,
GUI control, connected integrations, background execution, or persistent state
between sessions.

## Minimal identification pass

Run this only when the task actually needs a tool:

1. Read the exposed tool list. Group it by task family, not by name similarity.
2. Pick the single capability the task needs first.
3. Read that tool's live schema.
4. Make the smallest safe, non-destructive call that produces evidence.
5. Record what that evidence proves - and only that.

Stop as soon as you know enough to act. A full environment sweep on every turn
is waste, not diligence.

## Status vocabulary (same everywhere in this Skill)

- `ANNOUNCED` - mentioned somewhere; nothing verified.
- `SCHEMA_SEEN` - the live contract was inspected.
- `USED_OK` - a call succeeded in this context.
- `PERMISSION_BLOCKED` - present but gated. Availability is not permission.
- `UNAVAILABLE` - evidence shows this context cannot use it.
- `STALE` - an earlier observation is no longer trustworthy.
- `UNKNOWN` - untested. Never silently promoted to available.

## Reporting under uncertainty

When you cannot determine something, say which of these it is:

- **not exposed** - no such tool in this session;
- **not configured** - the tool exists but has no target/credential;
- **not running** - the target process or service is not up;
- **not permitted** - the host or user refused;
- **unobservable** - the host gives no signal either way.

"It didn't work" is not a diagnosis. "UNKNOWN because the host exposes no way to
check" is a legitimate, complete answer.

## Cache and provider notes

Behind an unknown gateway, assume nothing about prompt caching, tool semantics,
streaming, or token accounting. Compatibility with a message format does not
imply compatibility of cache behaviour. See `docs/cache-contract.md`.

## Related

- `references/runtime-detection-and-profiles.md`
- `references/runtime-boundary-matrix.md`
- `references/capability-probing.md`
- `cards/index.json` for task-family routing
