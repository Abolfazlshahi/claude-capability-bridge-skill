# Custom Provider Adaptation

## What this Skill can and cannot fix

A third-party model can receive runtime tools and still behave differently from an Anthropic model because tool schemas do not automatically provide the workflow knowledge needed to choose, sequence, verify, and recover from those tools.

The bridge targets the **knowledge and procedure side** of that gap. It cannot create a missing runtime capability, repair a broken gateway/adapter, or upgrade a model's fundamental ability to emit valid tool calls.

See `custom-provider-transport.md` for the concrete Claude Code gateway and custom-endpoint boundaries that matter when the underlying model is swapped.

## Five independent dimensions

### 1. Runtime capability
Can the current host execute the operation?

### 2. Model awareness
Does the model recognize that an exposed capability exists and understand its task class?

### 3. Schema competence
Can the model map a live tool schema to valid arguments and interpret its returned data?

### 4. Procedural competence
Can it sequence tools, maintain state, handle dependencies, and recover?

### 5. Verification competence
Does it know what evidence is sufficient for the actual acceptance criterion?

A Skill can directly influence dimensions 2–5, but only probabilistically.

## The custom-provider stack

```text
Claude Desktop / Claude Code host
        ↓
agent runtime + tool surface
        ↓
Anthropic-compatible API contract
        ↓
gateway / proxy / provider adapter
        ↓
third-party model
```

Every layer can fail independently.

A transport-compatible gateway does not imply model-compatible behavior.

## Concrete Claude Code cases

Claude Code documents several mechanisms for routing requests away from the direct Anthropic API, including `ANTHROPIC_BASE_URL` for proxies/LLM gateways and provider-specific environment variables for Bedrock, Vertex, and Foundry.

Important consequences for this Skill:

```text
endpoint override
  ≠
Anthropic model replacement that behaves identically
```

The current runtime can also use custom model IDs and, for supported third-party deployment modes, explicit capability metadata. Treat those declarations as runtime configuration, not evidence that the model genuinely supports every declared behavior.

## MCP Tool Search trap

One especially important custom-endpoint difference is MCP Tool Search. Claude Code documents that Tool Search is disabled by default when `ANTHROPIC_BASE_URL` points to a non-first-party host because many proxies do not forward `tool_reference` blocks.

Therefore:

```text
MCP server exists
      ↓
Tool Search disabled/default-changed by endpoint mode
      ↓
tool discovery behavior differs
```

This is **not** necessarily a model-awareness failure.

Only recommend enabling `ENABLE_TOOL_SEARCH=true` after establishing that the proxy forwards the required tool-reference protocol and the target model supports the feature.

## Server-managed settings boundary

Claude Code also documents that server-managed settings require a direct Anthropic API connection and are unavailable for third-party providers and non-default `ANTHROPIC_BASE_URL`/LLM gateway configurations.

The Skill must therefore distinguish:

```text
runtime-enforced policy
        ≠
Skill guidance
```

Never tell a custom-provider model that a server-managed control is active unless the current deployment proves it.

## Diagnostic matrix

```text
Request never reaches provider
→ host/network/auth

Gateway rejects protocol
→ adapter/transport

Gateway succeeds but tool/reference blocks disappear
→ gateway feature compatibility

Tool absent from model-visible context
→ runtime/discovery configuration

Tool visible, but model ignores it
→ awareness/routing

Tool visible, arguments malformed
→ schema/tool-call competence

Correct calls, wrong sequence
→ procedural competence

Correct sequence, premature success claim
→ verification competence

Vision/context/tool-result interpretation fails
→ model/provider capability
```

## Attribution protocol

To determine whether this Skill actually helps, keep the runtime and task fixed:

```text
same host
same tools
same schemas
same files
same permissions
same task

custom model
├── bridge OFF
└── bridge ON
```

Measure:

```text
tool-selection accuracy
schema-valid call rate
state-tracking accuracy
verification completion
false-success rate
recovery success
critical safety failures
```

Run multiple trials. One successful completion is not evidence of a robust behavioral gain.

## High-value symptoms the bridge should improve

- exposed tool ignored by the model;
- incorrect tool ordering;
- server started but never verified;
- browser opened but critical journey never exercised;
- identical failed calls repeated without diagnosis;
- success reported without evidence;
- state (path, URL, port, returned ID, process) guessed instead of observed.

## High-value non-fixes

Do not try to repair runtime problems with more prose:

```text
"There is definitely a browser tool."
"MCP Tool Search must be enabled."
"The gateway supports every Claude feature."
```

Inspect the current runtime and endpoint mode first.

## Model adaptation strategy

For a weaker third-party model, prefer compact executable protocols over encyclopedia-style prose:

```text
WHEN condition
→ CHECK current capability state
→ READ live contract/schema
→ CALL minimally
→ OBSERVE result
→ ASSERT expected state
→ CONTINUE / RECOVER
```

Then load only the relevant deep reference.

## Success criterion

The bridge is successful only when controlled evaluation shows a repeatable improvement in agent behavior. Documentation volume, number of files, or apparent completeness are not evidence.

## Non-goals

This project does not attempt to reproduce private system prompts, model weights, proprietary classifiers, hidden orchestration, or undocumented tool contracts.
