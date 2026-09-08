# Claude Desktop-Oriented Workflows

## Runtime mindset

Treat Desktop as an agent host, not a single monolithic model feature. A task can move among conversation, project context, Skills, connectors/MCP, code execution, browser, Chrome, computer use, and remote/scheduled execution.

## Cowork-style task routing

For general knowledge/work tasks:

```text
Understand request
→ inspect available integrations
→ choose structured connector when appropriate
→ otherwise use local files/code
→ use browser for web-facing work
→ use computer control for GUI-only work
→ verify result
```

The important behavior is not the exact UI label; it is choosing the narrowest capable execution surface and validating the result.

## Developer-oriented routing

For coding work:

```text
inspect repository
→ identify stack
→ edit
→ run tests/build
→ start app when relevant
→ browser-test user flows
→ diagnose failures
→ patch
→ re-test
→ report evidence
```

A developer agent should not stop at source generation when the user's request implies a working application.

## Browser handoff

A Desktop environment can provide an isolated browser as well as an integration with a user's existing Chrome context. Keep their state separate.

Use the isolated browser for public/clean tasks and local application verification. Use Chrome when existing authenticated context or tabs materially matter.

## Computer-use handoff

If a connector or browser can perform the requested operation, prefer it. Escalate to computer use when the application or required interaction is fundamentally GUI-based.

## Skills as behavior injection

A custom provider model may see the same tools but behave less reliably because it lacks the host-specific procedural patterns learned by Anthropic models. Load this Skill before choosing execution paths and apply explicit observe → act → verify loops.

## Dispatch / remote workflows

When the runtime exposes a remote or scheduled execution surface, treat it as an orchestration layer. The underlying task still requires the same capability discovery, authorization, and verification rules.

Never assume a remote task has access to local state simply because the originating conversation has it.

## Completion

Desktop completion is not equivalent to UI feedback such as a green status or a successful tool transport response. Use evidence from the actual requested outcome.