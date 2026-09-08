# Runtime Boundaries: Local, Cloud, Browser, and Integration State

The same Claude conversation can span surfaces whose execution environments are not equivalent.

## Four independent axes

```text
CONVERSATION
  what the user asked and what the model remembers

EXECUTION SURFACE
  desktop / web / mobile / Chrome / Cowork / Code

RESOURCE LOCATION
  local machine / Anthropic cloud / remote SaaS / connected service

AUTHENTICATION CONTEXT
  isolated browser / existing Chrome profile / connector auth / local app session
```

Do not collapse these into one generic "Claude state".

## Local vs cloud

A desktop UI being present on the user's computer does not prove that every task computation, tool call, or connector request runs locally. Conversely, a local Desktop Extension or local MCP server can provide access to resources that a remote session cannot reach.

Before relying on local state, establish:

```text
local filesystem reachable?
local process reachable?
local localhost service reachable?
local browser profile required?
local extension/MCP server connected?
```

## Browser boundary

```text
Built-in browser
    ≠
Claude in Chrome
```

Authentication, tabs, cookies, extension state, and browser history must be treated as distinct until observed otherwise.

## Connector boundary

Remote connectors can be available across multiple Claude surfaces while local MCP/Desktop Extension integrations can be restricted to Desktop/Code. Do not infer availability from another surface.

## Scheduling boundary

Scheduled execution is a new run with its own environment state. Re-discover resources, permissions, and live state instead of assuming the interactive session's state persists.

## Handoff checklist

When a task crosses a surface or execution boundary, carry:

- user objective;
- verified artifacts/identifiers;
- assumptions clearly marked;
- unresolved blockers;
- next required observation.

Do not carry raw secrets unless the runtime explicitly requires them and policy allows it.

## Core invariant

```text
same conversation
    ≠
same runtime
    ≠
same resources
    ≠
same permissions
    ≠
same authentication state
```
