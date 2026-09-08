# Capability Catalog

This catalog describes capability *classes*, not hard-coded private tool names. The runtime may expose different names and schemas.

| Capability class | What it enables | Typical use | Preferred over | Key verification |
|---|---|---|---|---|
| Conversation | reasoning, planning, explanation | pure knowledge/writing | none | answer matches request |
| Project context | persistent project instructions/knowledge | scoped work with reusable context | re-uploading context | context is relevant and current |
| Filesystem | read/write local files | source editing, artifacts | GUI file management | file diff/read-back |
| Shell/code | deterministic execution | tests, builds, scripts, servers | GUI interaction | exit status + relevant output |
| MCP/connector | structured external service access | mail, docs, issue systems, APIs | browser recreation | result/read-back |
| Built-in browser | isolated web navigation and interaction | public web, localhost, forms | raw desktop clicking | URL + visible state + interaction result |
| Chrome integration | existing browser state | authenticated/tab-dependent web work | isolated browser | correct account/tab/context |
| Computer use | desktop GUI control | native apps, GUI-only flows | structured tools | observed final screen/state |
| Skill | procedural knowledge | repeatable task workflows | ad-hoc giant prompt | required workflow and evidence followed |
| Plugin | packaged skills/integrations | reusable domain bundles | manually wiring many components | installed components active |
| Scheduling/remote dispatch | delayed/remote orchestration | recurring or off-device tasks | manual repetition | task ran in intended environment |

## Routing principles

### Structured before semantic
Use exact APIs/connectors/filesystem operations when available. They are generally easier to validate than GUI interactions.

### Browser before desktop for web
Use browser semantics for web pages. Escalate to computer use when the browser surface is absent or cannot represent the required behavior.

### Deterministic before visual
Use tests/builds/static checks to catch deterministic failures. Use browser/GUI verification for user-facing behavior.

### Narrowest capability wins
A capability is preferred when it can satisfy the complete requested operation with less ambiguity and lower side-effect risk.

## Capability discovery record

An implementation can normalize a runtime into a record such as:

```yaml
filesystem: available
shell: available
browser: available
chrome: unknown
computer_use: unavailable
mcp:
  github: available
  docs: available
skills: available
plugins: unknown
scheduling: unavailable
```

This is illustrative. Do not emit or depend on these values unless they have been observed from the host.

## Why the catalog exists

Anthropic's own model and runtime combination can make capability selection feel automatic. A custom provider can expose the same underlying tools without reproducing those behavioral priors. The catalog makes the distinctions explicit so the model can reason about them rather than guessing.