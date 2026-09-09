# Runtime Boundary Matrix

Current capability access depends on execution surface and whether the Claude Desktop bridge is connected. Treat this as a model for reasoning, not a promise that every deployment has every feature.

| Capability | Cloud session | Desktop-connected/local bridge | Needs Desktop connection |
|---|---|---|---|
| Cloud session state | Yes | Yes | No |
| Projects | Yes | Yes | No |
| Skills / plugins | Yes | Yes | No |
| Local files | Through connected desktop/local folders | Yes | Yes |
| Local connectors / local MCP | Through desktop bridge where supported | Yes | Yes |
| Built-in browser | Via connected desktop browser | Yes | Yes for local browser bridge |
| Claude in Chrome | Connected Chrome context | Yes | Connected desktop context; app-open requirement depends on current surface |
| Computer use | Via desktop bridge where supported | Yes | Yes |
| Scheduled cloud task | Yes | — | No |
| Local process / localhost | Not assumed | Yes | Yes |
| Native desktop application | Not assumed | Yes | Yes |

## Rules

1. A cloud session continuing after a desktop disconnect does **not** prove that local files, local MCP, localhost, browser, or computer-use access remains available.
2. A session resumed on another surface must re-discover capabilities relevant to the next action.
3. Scheduled execution is a distinct execution context. Never assume today's PID, port, tab, credentials, local server, or filesystem state exists later.
4. For browser use, distinguish the built-in browser from the user's Chrome context. Authentication and tabs are not interchangeable unless the runtime explicitly bridges them.
5. When a capability is marked `LOCAL`, verify the desktop bridge and permissions before depending on it.

## Current-source nuance

Cowork sessions run in the cloud across surfaces, while local file access, local connectors, browser use, and computer use can depend on the Claude Desktop connection. Current Cowork also supports scheduled cloud tasks without the computer staying awake. Always check the live runtime because rollout and plan availability can change.
