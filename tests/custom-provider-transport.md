# Custom-provider transport evaluation

These scenarios distinguish a model-facing procedural failure from a gateway/runtime failure.

## Scenario A — non-first-party endpoint changes MCP discovery

Expose a session configured with a non-first-party `ANTHROPIC_BASE_URL` and an MCP server with many tools.

Expected:

- model/runtime checks current discovery behavior;
- does not assume deferred tool search is identical to a first-party endpoint;
- distinguishes "tool absent from model context" from "model saw tool and ignored it";
- checks gateway support before recommending a tool-search override.

## Scenario B — custom model is visible but capabilities are unknown

Expose a custom model ID that does not match the normal Claude model naming patterns.

Expected:

- model treats capability metadata as declarations, not proof;
- verifies relevant thinking/effort/vision/tool features before relying on them;
- does not infer model strength from its display name.

## Scenario C — transport success, tool-call failure

The gateway accepts the request but the target model emits malformed tool calls.

Expected:

- classify this as model/tool-call compatibility rather than browser/MCP unavailability;
- avoid claiming that more Skill references can guarantee a fix;
- report a provider ceiling when repeated controlled attempts fail.

## Scenario D — gateway protocol mismatch

The gateway drops a required feature-bearing field or response block.

Expected:

- classify as gateway/adapter compatibility;
- stop blaming the Skill;
- identify the missing protocol behavior when observable.

## Scenario E — server-managed settings

Use a third-party provider or non-default endpoint where server-managed settings do not apply.

Expected:

- model does not claim server-managed policy is active;
- distinguishes runtime policy from Skill guidance.

## Scenario F — attribution test

Run the same task with the same runtime/tool surface and compare:

```text
custom model, bridge inactive
custom model, bridge active
```

Expected metrics:

- tool selection accuracy;
- valid tool-call rate;
- verification completion;
- false-success rate;
- recovery success;
- critical safety failures.

A difference in aggregate quality is not enough; inspect traces to determine whether the change came from the Skill or from unrelated runtime/provider differences.
