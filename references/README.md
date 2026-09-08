# Reference Map

These documents are deliberately separated from `SKILL.md` so an agent can load only the procedures needed for the current task.

| Reference | Use when |
|---|---|
| `capability-model.md` | diagnosing whether a problem is runtime, routing, schema-use, workflow, or verification |
| `browser-workflows.md` | navigating websites, using browser surfaces, or testing localhost apps |
| `webapp-verification.md` | building/fixing a web app and proving it works end-to-end |
| `computer-use.md` | controlling native GUI applications or escalating from structured tools |
| `code-and-shell.md` | running builds, tests, scripts, servers, and deterministic checks |
| `mcp-and-connectors.md` | choosing MCP/connectors and validating structured tool calls |
| `skills-and-plugins.md` | understanding procedural Skills and packaged Plugins |
| `projects-and-files.md` | reconciling project knowledge with live filesystem/worktree state |
| `verification.md` | defining evidence and reporting exact verification status |
| `failure-recovery.md` | diagnosing and recovering from failed or ambiguous tool workflows |
| `security-and-permissions.md` | sensitive data, approvals, local extensions, and prompt-injection defense |
| `desktop-workflows.md` | mapping Claude Desktop/Cowork-style workflows to available capabilities |

## Loading rule

Do not load all references by default. Select the smallest set that directly supports the current task. Cross-reference only when another capability boundary is entered.