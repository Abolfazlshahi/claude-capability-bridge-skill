# Capability Remediation

`UNAVAILABLE` is not the same as `not configured`. When a required capability is missing, diagnose the cause before stopping or inventing a workaround.

## Remediation loop

```text
DETECT → CLASSIFY → REPAIR IF POSSIBLE → RE-PROBE
→ ROUTE → VERIFY
```

The repair step is conditional. A Skill may teach the diagnosis and recovery procedure, but it cannot grant a provider capability, bypass host permissions, or create a nonexistent tool interface.

## Failure classes

Use the narrowest evidence-supported class:

| Class | Meaning | Typical next step |
|---|---|---|
| `NOT_EXPOSED` | No matching tool/surface is visible | inspect other exposed interfaces; do not invent a call |
| `NOT_CONFIGURED` | Host supports the integration but it is not set up | use the host's available setup/configuration path |
| `NOT_INSTALLED` | Required local executable/package is absent | inspect package/runtime state; install only when authorized |
| `NOT_RUNNING` | Required local server/process is absent | inspect process/listener and start the intended service |
| `PERMISSION_DENIED` | Surface exists but access is gated | request/obtain permitted access; never route around it |
| `PROVIDER_UNSUPPORTED` | Current provider/endpoint cannot use the host feature | classify boundary and choose a supported alternative |
| `AUTH_SESSION` | Browser/account/session state is wrong or missing | use the correct session or authenticate through the permitted surface |
| `PROTOCOL_FAILURE` | Tool is exposed but calls fail schema/transport expectations | inspect live contract; correct call shape; stop if incompatibility persists |
| `MODEL_PROCEDURAL_FAILURE` | Tool exists and is usable, but the model repeatedly fails to call/use it correctly | use stronger bootstrap/context or simpler deterministic path |
| `UNKNOWN` | Evidence is insufficient | perform the smallest safe discriminating probe |

Do not collapse all of these into “not connected.”

## Repair rules

Only repair a cause the current runtime can actually affect:

```text
configuration problem → configure if exposed/authorized
missing local dependency → install if authorized and deterministic
server not running → launch intended project process
permission gate → request/obtain permission
provider limitation → alternate supported surface or honest block
host capability absent → do not pretend Skill prose can create it
```

After every repair, re-probe the affected capability. A successful setup command is not proof of usable capability.

## Browser / Chrome / Playwright example

For a task such as “open localhost and test the UI”:

```text
1. Identify runtime: CLI, Desktop/Cowork, cloud/remote, other.
2. Check whether a browser surface is actually exposed.
3. If no browser surface, check exposed structured integrations/MCP and local shell.
4. If Playwright is expected, distinguish:
   tool not exposed / MCP not configured / executable missing /
   browser not running / provider unsupported.
5. If a local app is required, recognize and launch the project separately.
6. Re-probe browser readiness.
7. Use the authoritative surface and verify the rendered result.
```

Never infer that Playwright can be “connected” merely because the project contains Playwright dependencies. Never infer that Chrome is available merely because the host product supports Chrome somewhere else.

## Provider-boundary rule

When a host feature is documented for one provider but the current session uses another provider, stop treating repeated connection attempts as the primary remedy. Confirm the provider/endpoint boundary, test any supported alternative, and report the resulting classification.

A `PROVIDER_UNSUPPORTED` result is a successful diagnosis, not an execution failure caused by the Skill.

## Bounded retries

Retry only when the diagnosis suggests a changed variable:

```text
wrong args → correct schema
not ready → wait/readiness probe
stale session → re-observe/reconnect
missing process → start intended process
configuration → apply authorized configuration
provider ceiling → do not retry indefinitely
```

A second identical failure with no changed variable is evidence against another blind retry.