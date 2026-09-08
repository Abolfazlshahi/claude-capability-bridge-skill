# Custom-provider transport and feature gaps

This reference exists because a model-facing Skill cannot fix every failure caused by replacing the underlying model or routing layer. Claude Code can be pointed at gateways and provider-specific endpoints, and the behavior of some runtime features changes when the endpoint is not a first-party Anthropic endpoint.

## 1. Separate the three layers

```text
Claude Desktop / Claude Code runtime
        ↓
model API contract / gateway
        ↓
underlying model provider
```

A request can reach the runtime successfully while the model behind the endpoint still differs in tool-use ability, context behavior, vision, reasoning, or structured-output reliability.

## 2. The important routing knob

Claude Code documents `ANTHROPIC_BASE_URL` as an endpoint override for a proxy or LLM gateway. A custom endpoint changes where requests are sent; it does not by itself make the target model equivalent to an Anthropic Claude model.

Related model-selection controls include:

```text
ANTHROPIC_MODEL
ANTHROPIC_CUSTOM_MODEL_OPTION
ANTHROPIC_CUSTOM_MODEL_OPTION_NAME
ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION
ANTHROPIC_DEFAULT_OPUS_MODEL
ANTHROPIC_DEFAULT_SONNET_MODEL
ANTHROPIC_DEFAULT_HAIKU_MODEL
```

Use only variables that the current Claude Code release documents and only for the deployment mode actually in use.

## 3. Gateway compatibility is not model compatibility

A gateway may correctly implement the Anthropic Messages format while the target model still lacks capabilities or behaviors expected by Claude Code.

Check separately:

```text
transport compatibility
        ↓
request/response compatibility
        ↓
tool-call compatibility
        ↓
context compatibility
        ↓
model capability compatibility
```

Do not infer the last layer from the first.

## 4. MCP Tool Search is a major custom-endpoint trap

Claude Code documents that MCP Tool Search is disabled by default when `ANTHROPIC_BASE_URL` points to a non-first-party host because many proxies do not forward `tool_reference` blocks.

Consequences:

```text
first-party endpoint
→ deferred MCP discovery may be available by default

non-first-party endpoint
→ tool schemas may be loaded up front unless explicitly overridden
```

A gateway that supports tool references can opt into deferred search with the documented `ENABLE_TOOL_SEARCH=true` setting. Do not enable it merely because the provider is custom: first verify that the gateway forwards the required protocol blocks and that the target model supports the feature.

For a bridge Skill this creates two distinct failure modes:

```text
tool not discovered because runtime/gateway mode changed
        ≠
model saw the tool but did not know how to use it
```

The Skill must diagnose the first as a transport/runtime issue, not attempt to solve it with more prompt text.

## 5. Runtime feature detection must be evidence-based

A model-facing bridge should test or inspect the current session for:

```text
endpoint mode
model identity
MCP discovery mode
visible tools
available tool schemas
vision/image support when relevant
context/length constraints when relevant
streaming/tool-result behavior when relevant
permission state
```

Do not assume that a feature enabled for a native Claude deployment remains enabled for the custom endpoint.

## 6. Capability declaration and the `/model` picker

Claude Code can expose custom model entries and provider-specific model IDs. Current releases also document companion `*_SUPPORTED_CAPABILITIES` variables for pinned third-party deployments. These declarations can enable features such as effort levels, thinking, adaptive thinking, interleaved thinking, and related UI/runtime behavior when the deployment actually supports them.

This declaration is metadata, not proof. A provider should only declare a capability when it has verified that the underlying deployment supports the required semantics.

## 7. Server-managed settings boundary

Claude Code documents that server-managed settings require a direct Anthropic API connection and are not available when using third-party providers or a non-default `ANTHROPIC_BASE_URL`/LLM gateway.

Therefore:

```text
native Anthropic connection
→ some server-managed controls may apply

third-party/gateway connection
→ those controls are not equivalent
```

A bridge Skill must never tell a custom-provider model that a server-managed policy is enforced if the current deployment bypasses it.

## 8. Model behavior versus host behavior

Use this diagnosis table:

| Symptom | Likely layer |
|---|---|
| request never reaches endpoint | host/network/auth |
| endpoint returns invalid protocol shape | gateway/adapter |
| tool list differs from expected | runtime/gateway discovery |
| tool is visible but ignored | model awareness/routing |
| arguments are malformed | model schema/tool-call ability |
| tool succeeds but workflow is wrong | procedural knowledge |
| workflow succeeds but agent claims success early | verification |
| vision/tool-result interpretation is unreliable | model capability |
| long context collapses | provider context/runtime configuration |

## 9. Never bake a gateway brand into the Skill

LiteLLM is one documented example, not the universal abstraction. The bridge should teach the concept of a gateway/compatible endpoint and use live runtime evidence. It should not require LiteLLM, Bifrost, OpenRouter, or any other specific proxy.

## 10. Practical bridge behavior

When a user says a custom provider is “installed”:

```text
identify runtime surface
→ identify model/provider path if observable
→ inspect `/status` or equivalent runtime status when available
→ inspect actual visible tools
→ determine MCP discovery mode
→ determine relevant feature declarations
→ run the smallest safe capability probe
→ classify failures by layer
→ only then apply Skill workflow guidance
```

The goal is not to make a third-party model pretend to be Claude. The goal is to make the agent accurately understand what the current stack can do and behave well within those limits.
