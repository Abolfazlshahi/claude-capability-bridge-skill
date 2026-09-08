# Capability Handshake

The bridge must distinguish a capability being documented from a capability being usable in the current session.

## Handshake

```text
ANNOUNCED
   ↓
DISCOVERED
   ↓
SCHEMA UNDERSTOOD
   ↓
MINIMAL PROBE (only when safe and useful)
   ↓
OBSERVED RESULT
   ↓
REGISTERED STATE
```

## Capability record

Maintain an internal record with:

| Field | Meaning |
|---|---|
| id | stable conceptual capability name |
| exposed_name | current tool/server/host name if known |
| state | AVAILABLE / POSSIBLE / UNKNOWN / UNAVAILABLE |
| schema_confidence | LOW / MEDIUM / HIGH |
| permission | allowed / approval-required / blocked / unknown |
| side_effect | read / write / external / destructive |
| preferred_for | task classes where it is strongest |
| fallback | next safest capability |
| evidence | tool metadata, successful call, host signal, or direct observation |
| last_verified | current session checkpoint |

## Probe rules

A probe is appropriate when all of these hold:

1. the capability appears potentially useful;
2. the probe is low-risk and reversible;
3. the result materially changes routing decisions;
4. no stronger direct evidence already exists.

Do not probe destructive endpoints, sensitive accounts, production systems, purchases, messages, or irreversible operations merely to discover whether a capability works.

## Example

```text
Browser mentioned by host
→ state = POSSIBLE

Browser tool actually exposed
→ inspect schema
→ state = DISCOVERED/usable

Navigate to safe local page
→ successful observation
→ state = AVAILABLE

Authenticated browser state not established
→ auth_state = UNKNOWN
```

## Negative capability evidence

A failed call is not always proof that a capability is absent. Distinguish:

```text
NOT EXPOSED
CALL REJECTED
PERMISSION BLOCKED
BAD ARGUMENT
ENVIRONMENT FAILURE
TRANSIENT FAILURE
```

Only classify `UNAVAILABLE` when the evidence supports absence/disablement rather than a malformed request or unrelated environment failure.

## Session refresh

Refresh capability state after:

- switching project/workspace;
- connecting/disconnecting an MCP server;
- browser surface changes;
- permission changes;
- tool installation/removal;
- a long-lived process or server becomes unhealthy;
- a tool call reveals a previously unknown constraint.
