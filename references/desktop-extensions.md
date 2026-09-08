# Desktop Extensions / Local MCP

Desktop Extensions are a local integration boundary. They package MCP servers for installation and management in Claude Desktop, allowing local resources, internal systems, desktop applications, local files, databases, clipboard access, or processes to be reached through structured tools.

## Mental model

```text
Desktop Extension
      ↓
local MCP server/process
      ↓
OS / local network / local applications
      ↓
model-visible tools
```

Do not treat a Desktop Extension as equivalent to a remote connector.

## Use when

Prefer a local extension when the requested resource or operation is fundamentally local, such as:

- local files;
- localhost databases or services;
- desktop applications;
- OS-level resources;
- internal systems reachable from the user's network.

## Discovery

Before relying on an extension:

```text
extension installed?
→ server running?
→ tools exposed?
→ permissions/approvals understood?
→ target resource reachable?
```

A successful extension installation does not prove that the target operation works.

## Security boundary

Local MCP/extension software runs with the privileges granted by the host/OS. Treat unfamiliar extensions as executable code, not passive documentation. Evaluate requested permissions, network access, file scope, process execution, persistence, and credentials before use.

## Remote vs local

Remote MCP connectors are brokered through Anthropic infrastructure; local Desktop Extensions/MCP servers use the user's local machine/network. A resource accessible through one does not imply access through the other.

## Failure diagnosis

```text
not installed
→ integration setup

installed but no server
→ local process/runtime problem

server running but tool absent
→ registration/schema problem

tool present but access denied
→ permission/auth boundary

tool succeeds but target state wrong
→ workflow/verification problem
```

## Rule

Use the most direct structured local integration available, but never infer local access from the mere existence of Claude Desktop or a connected remote connector.
