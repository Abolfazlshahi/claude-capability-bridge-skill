# Tool-Schema Literacy

Custom-provider models often receive tool definitions without reliable procedural habits. The bridge teaches a schema-first method.

## Read before calling

Extract:

```text
TOOL ID / NAME
PURPOSE
REQUIRED ARGUMENTS
OPTIONAL ARGUMENTS
ENUMS / CONSTRAINTS
INPUT TYPES
OUTPUT SHAPE
ERROR SHAPE
SIDE EFFECTS
AUTH / APPROVAL REQUIREMENTS
IDEMPOTENCE
```

## Tool selection score

When several tools could work, prefer the option with the strongest combination of:

```text
task fit
+ observability
+ determinism
+ reversibility
+ least privilege
+ low ambiguity
```

Do not choose solely because a tool name sounds relevant.

## Argument discipline

1. Fill only arguments needed for the requested operation.
2. Use exact enum values from the schema.
3. Respect required fields and declared types.
4. Do not invent undocumented parameters.
5. Preserve opaque IDs returned by previous calls when they are required for follow-up actions.
6. If an argument depends on current state, observe that state before constructing the call.

## Output discipline

After a successful call, determine whether the output represents:

```text
operation accepted
operation completed
resource returned
state changed
or merely a queued/acknowledged request
```

A success envelope alone is not proof of the intended real-world effect.

## Retry discipline

Retry only when:

- the failure is plausibly transient; or
- a specific argument/environment issue has been corrected; or
- the tool documentation explicitly recommends retry behavior.

Do not replay side-effecting calls blindly.

## Tool chains

For a multi-tool workflow, record the dependency:

```text
observe A
  ↓
obtain ID/value
  ↓
call B with that exact evidence
  ↓
observe B result
```

Never substitute guessed IDs, paths, ports, URLs, or resource names when observable values exist.
