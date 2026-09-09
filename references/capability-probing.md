# Capability Probing Protocol

## Purpose

Discovery tells the agent what appears to exist. Probing establishes what is usable **in the current runtime and context**.

Never turn a documentation claim, model label, stale session observation, or conceptual capability name into an `AVAILABLE` capability without current evidence.

## Capability state

Use:

```text
UNKNOWN → PROBING → OBSERVED_AVAILABLE
                    ↘ OBSERVED_LIMITED
                    ↘ BLOCKED
                    ↘ UNAVAILABLE
```

`STALE` is not a usable state. Refresh it after a material runtime, permission, session, provider, or context change.

## Probe contract

For a candidate capability:

```text
1. IDENTIFY the exact capability required by the acceptance criterion.
2. ENUMERATE the live surface that could provide it.
3. INSPECT the live schema/contract and permission state.
4. CHOOSE the smallest harmless, reversible probe.
5. EXECUTE exactly one probe where practical.
6. OBSERVE the returned evidence, not merely call success.
7. CLASSIFY the capability state and limitations.
8. USE it only within the observed contract.
9. INVALIDATE the result after a material context change.
```

Do not probe by causing a consequential mutation when a read-only or reversible probe can establish the same fact.

## Probe quality

A good probe is:

```text
minimal | safe | reversible | specific | observable | representative
```

Avoid broad "test everything" probes. They waste context and can create side effects.

## Examples

### Browser

```text
Browser surface visible
→ navigation capability UNKNOWN
→ inspect actual navigation operation/schema
→ navigate to a safe, known page
→ observe URL/page result
→ NAVIGATION = OBSERVED_AVAILABLE
```

If navigation works but screenshots are unavailable:

```text
NAVIGATION = AVAILABLE
SCREENSHOT = UNAVAILABLE
```

Do not upgrade one capability because another succeeded.

### MCP / connector

```text
server visible
→ target read operation visible
→ inspect schema + authorization
→ call harmless read-only operation
→ inspect structured result
→ READ = OBSERVED_AVAILABLE
```

A visible mutation tool is not proof that mutation is authorized or safe to perform.

### Shell / code

```text
shell visible
→ inspect command constraints
→ run a harmless identity/version probe
→ observe exit status + output
→ SHELL = OBSERVED_AVAILABLE
```

Do not infer that a particular package, interpreter, network route, or port is available from shell existence alone.

### Computer use

```text
computer-use surface visible
→ inspect permission/scope
→ perform minimal non-destructive observation
→ observe screen result
→ SCREEN OBSERVATION = OBSERVED_AVAILABLE
```

Do not click merely to prove clicking exists when observation is enough.

## Context invalidation

Invalidate capability observations after events such as:

```text
runtime restart | provider/model change | browser switch
permission change | extension disconnect | MCP reconnect
session migration | scheduled/remote execution | major workspace change
```

Re-probe the affected capability instead of relying on an old `AVAILABLE` result.

## Reporting

Record only what was actually established:

```text
CAPABILITY: browser.navigate
STATE: OBSERVED_AVAILABLE
SURFACE: built-in browser
EVIDENCE: returned URL + page identity
LIMITS: no DOM operation exposed
VALID FOR: current session/context
```

A probe establishes capability, not task success. Task success still requires the task's own acceptance criteria and verification evidence.
