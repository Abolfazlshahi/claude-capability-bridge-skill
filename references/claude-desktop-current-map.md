# Current Claude Desktop Capability Map

_Last reviewed against public Anthropic documentation on 2026-09-08._

This is a public-behavior map, not a reproduction of private prompts or internal implementation. Availability is plan-, platform-, admin-, rollout-, endpoint-, and session-dependent.

## Capability families

| Family | Current public behavior | Bridge implication |
|---|---|---|
| Chat / conversation | Conversational interaction and task steering | Context, not proof of execution |
| Cowork | Agentic knowledge work with files, connected apps, long-running work and scheduled/remote workflows | Treat as an agent runtime |
| Claude Code | Agentic coding/work engine with tools, skills, MCP, subagents and multiple execution environments | Model the engine separately from UI surface |
| Skills | File-based procedural knowledge loaded by the host | Primary mechanism for procedure injection |
| Plugins | Bundles of skills, connectors, slash commands and sub-agents | Composition layer |
| Projects | Scoped knowledge/context | Not the same as live local filesystem state |
| Files / Git | Local file and repository access when exposed | Verify path, writeability, branch and diff |
| Shell / code | Commands, builds, tests, scripts and diagnostics where exposed | Prefer deterministic operations |
| Background processes | Long-running servers/jobs | Track ownership, PID, listener and health separately |
| Built-in Cowork browser | Isolated browser in Desktop side panel; can navigate, read, click, type and fill forms | Use for clean/public web work and localhost verification |
| Claude in Chrome | Existing browser context through extension | Use when existing tabs/auth/session materially matter |
| Computer use | Screen, mouse, keyboard, apps, browser and dev-tool interaction | GUI fallback/escalation; observe state after actions |
| MCP / remote connectors | Structured access to remote tools/data; remote calls are brokered through Anthropic infrastructure | Direct structured path when supported |
| Local MCP / Desktop Extensions | Local MCP processes/extensions for Desktop/Code | Separate local trust and OS boundary |
| Interactive connector apps | Connected services may render interactive UI | Verify state, not just tool text |
| Artifacts | Interactive deliverables can be created, viewed and shared/saved | Verify the artifact itself |
| Sub-agents | Delegate bounded work to separate contexts | Define scope/output and verify delegated result |
| Schedules / routines | Scheduled tasks execute as distinct runs; local and remote modes differ | Never assume interactive local state persists |
| Remote Control / cross-surface work | Sessions can be accessed or triggered from other surfaces | Re-check execution environment |

## Custom-provider / gateway surface

Claude Code documents several ways to route model requests through providers or gateways. The most general custom endpoint mechanism is `ANTHROPIC_BASE_URL`; provider-specific modes also exist for Bedrock, Vertex AI, Foundry and other supported deployments.

Important rule:

```text
endpoint compatibility
      ≠
model capability compatibility
```

A gateway can preserve the Anthropic request format while the target model differs in tool calling, context handling, vision, reasoning, or other capabilities.

Current Claude Code documentation also notes that a non-first-party `ANTHROPIC_BASE_URL` changes MCP Tool Search behavior: Tool Search is disabled by default because many proxies do not forward `tool_reference` blocks. The documented override is `ENABLE_TOOL_SEARCH=true`, but it should only be used when the gateway and target model actually support the required protocol behavior.

Claude Code also supports custom model entries and, for documented third-party deployment modes, explicit supported-capability metadata. Capability declarations are configuration, not proof; the underlying model must really support the declared feature.

Server-managed settings are a separate boundary: current Claude Code documentation says they require a direct Anthropic API connection and are not available for third-party providers or non-default `ANTHROPIC_BASE_URL`/LLM gateway configurations.

## Browser-specific facts

The built-in Cowork browser and Claude in Chrome are different surfaces. The built-in browser is isolated from the user's normal browser; Chrome integration works with the user's existing browser context. Never infer shared cookies, tabs, passwords or authentication state.

## Local / cloud boundary

Cloud execution, local Desktop execution, Remote Control, remote MCP connectors, local MCP/Desktop Extensions, and scheduled runs can have different filesystem, process, network, authentication and permission boundaries. Re-discover state after crossing an execution boundary.

## Normalized capability states

```text
OBSERVED_AVAILABLE
SUPPORTED_BUT_UNVERIFIED
BLOCKED_BY_PERMISSION
UNAVAILABLE
ROLLOUT_OR_PLAN_DEPENDENT
UNKNOWN
STALE
```

## Maintenance rule

When public behavior changes, update this map first, then the affected procedural reference, source notes, and evaluation scenarios. Keep private tool names and private orchestration details out of the Skill.
