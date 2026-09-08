# Reusable Workflow Patterns

These compact state machines are intended to be copied mentally across tasks. They make sequencing explicit without hard-coding a provider's private tool names.

## Inspect → Act → Verify

```text
DISCOVER
→ SELECT
→ ACT
→ OBSERVE
→ ASSERT
→ NEXT / RECOVER
```

Use for almost every consequential tool call.

## Service launch

```text
INSPECT PROJECT
→ CHOOSE DECLARED COMMAND
→ START PROCESS
→ CAPTURE PID/LOGS
→ PROBE READINESS
→ READY?
   ├─ NO → DIAGNOSE
   └─ YES → CONTINUE
```

## Web-app verification

```text
SOURCE READY
→ SERVER READY
→ OPEN URL
→ OBSERVE RENDER
→ EXERCISE CRITICAL PATH
→ CHECK RESULT
→ CHECK TELEMETRY
→ PASS?
   ├─ YES → AUTOMATED CHECKS
   └─ NO → LOCALIZE → PATCH → REPEAT
```

## Connector mutation

```text
IDENTIFY SERVICE
→ INSPECT TOOL SCHEMA
→ CHECK AUTH/SCOPE
→ MUTATE
→ READ-BACK
→ ASSERT SIDE EFFECT
```

## Browser interaction

```text
OPEN
→ WAIT
→ OBSERVE
→ TARGET
→ ONE ACTION
→ OBSERVE
→ ASSERT
```

## GUI interaction

```text
OBSERVE SCREEN
→ IDENTIFY WINDOW
→ ONE ACTION
→ OBSERVE AGAIN
→ ASSERT STATE
```

## Failure recovery

```text
FAILURE
→ CLASSIFY
→ COLLECT MINIMUM EVIDENCE
→ CHANGE ONE VARIABLE OR TOOL PATH
→ RETRY
→ VERIFY
```

## Capability routing

```text
TASK
→ DIRECT STRUCTURED OPERATION?
   ├─ YES → CONNECTOR/API
   └─ NO → DETERMINISTIC LOCAL OPERATION?
             ├─ YES → FILESYSTEM/CODE
             └─ NO → WEB INTERACTION?
                       ├─ YES → BROWSER
                       └─ NO → GUI?
                                 ├─ YES → COMPUTER USE
                                 └─ NO → CHAT/REASONING
```

## Evidence ladder

```text
DIRECT USER-FACING OBSERVATION
↑ strongest
DETERMINISTIC TEST
STRUCTURED READ-BACK
LOG/TELEMETRY
INFERENCE
↓ weakest
```

Report the highest evidence level actually obtained, not the highest level theoretically possible.

## State handoff

When switching capability families, carry forward only verified state:

```text
verified URL
verified path
verified process/PID
verified auth state
verified current UI state
verified test result
```

Do not carry assumptions across a tool boundary.