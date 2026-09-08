# Reference Map

These documents are intentionally separated from `SKILL.md` so the agent can load only the procedure required for the current task. The canonical current-capability snapshot is `claude-desktop-current-map.md`; provider-specific boundaries are in `custom-provider-transport.md`; evidence provenance is kept in `source-notes.md`.

| Reference | Use when |
|---|---|
| `claude-desktop-current-map.md` | checking the current public Claude Desktop/Cowork/Claude Code capability surface |
| `custom-provider-transport.md` | diagnosing gateways, `ANTHROPIC_BASE_URL`, model/provider feature gaps, and MCP discovery differences |
| `capability-model.md` | separating model, runtime, tool, provider, and environment responsibility |
| `capability-catalog.md` | choosing among capability classes and local/cloud surfaces |
| `capability-handshake.md` | discovering, probing, and freshness-checking capabilities |
| `workspace-map.md` | modeling Desktop workspace/context/process/browser state |
| `runtime-boundaries.md` | crossing local/cloud, browser, authentication, or remote boundaries |
| `activation-and-memory.md` | Skill slash activation and activation lifetime |
| `session-memory.md` | maintaining and invalidating session capability state |
| `tool-schema-literacy.md` | using unfamiliar tools from live schemas |
| `tool-use-patterns.md` | general tool-call, observation, retry, and idempotence discipline |
| `browser-workflows.md` | browser/Chrome navigation, localhost, visual checks, and browser safety |
| `webapp-verification.md` | building/fixing a web app and proving it works end-to-end |
| `interactive-surfaces.md` | interactive connectors/apps and Artifacts |
| `computer-use.md` | GUI escalation and screen-control workflows |
| `code-and-shell.md` | deterministic execution, servers, tests, and process management |
| `mcp-and-connectors.md` | MCP/connectors, structured operations, and read-back |
| `mcp-deep-dive.md` | MCP tools, resources, prompts, elicitation, and trust boundaries |
| `desktop-extensions.md` | local MCP/Desktop Extensions and their security boundary |
| `skills-and-plugins.md` | Skills, Plugins, triggering, and progressive disclosure |
| `async-subagents-and-remote.md` | subagents, long-running work, scheduled and remote sessions |
| `projects-and-files.md` | projects vs live files vs Git/artifact state |
| `provider-adaptation.md` | deciding whether a custom-provider problem is Skill-solvable |
| `evaluation-and-attribution.md` | controlled before/after evaluation and causal attribution |
| `task-recipes.md` | compact reusable task procedures |
| `verification.md` | acceptance criteria and evidence levels |
| `failure-recovery.md` | failure classification and repair loops |
| `security-and-permissions.md` | authorization, sensitive data, and prompt injection |
| `desktop-workflows.md` | Desktop/Cowork routing patterns |
| `source-notes.md` | primary-source provenance and maintenance rules |

## Loading rule

Do not load all references by default. Start with the smallest relevant set and cross the boundary only when the task actually enters another capability family. The current capability map is a maintained public snapshot, not a universal runtime contract.