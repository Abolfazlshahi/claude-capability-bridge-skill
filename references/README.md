# Reference Map

These documents are intentionally separated from `SKILL.md` so the agent can load only the procedure required for the current task. The runtime-aware operating model is in `runtime-detection-and-profiles.md`; `claude-desktop-current-map.md` is a Desktop/Cowork capability snapshot, not a universal runtime contract. Provider-specific boundaries are in `custom-provider-transport.md`; CLI behavior is in `claude-code-cli-operating-model.md`; project execution-model recognition is in `project-recognition-and-launch.md`; evidence provenance is kept in `source-notes.md`.

| Reference | Use when |
|---|---|
| `runtime-detection-and-profiles.md` | identify CLI/Desktop/Cowork/cloud/remote host, execution location, provider, and capability profile |
| `claude-code-cli-operating-model.md` | CLI-first routing, shell/Git/process work, browser integration boundaries, provider-aware CLI recovery |
| `claude-code-bootstrap-kit.md` | configure a compact always-on `CLAUDE.md`/SessionStart/plugin bootstrap and evaluate procedural forgetting |
| `capability-remediation.md` | classify missing integrations and repair/re-probe instead of stopping at “not connected” |
| `claude-desktop-current-map.md` | checking the current public Claude Desktop/Cowork capability snapshot |
| `claude-code-native-mechanisms.md` | hooks, CLAUDE.md/rules, slash commands, output styles, rewind, worktrees, teams, SDK/CI, IDE, and Remote Control boundaries |
| `office-and-collaboration-surfaces.md` | native Office, standalone file generation, Slack/Claude Tag, voice, account memory, and surface-specific verification |
| `custom-provider-transport.md` | diagnosing gateways, `ANTHROPIC_BASE_URL`, model/provider feature gaps, and MCP discovery differences |
| `project-recognition-and-launch.md` | identifying static vs server-backed vs full-stack projects and constructing a launch contract |
| `capability-model.md` | separating model, runtime, tool, provider, and environment responsibility |
| `capability-catalog.md` | choosing among capability classes and local/cloud surfaces |
| `capability-handshake.md` | discovering, probing, and freshness-checking capabilities |
| `capability-probing.md` | proving an uncertain capability with the smallest safe probe and invalidating stale observations |
| `runtime-boundary-matrix.md` | comparing cloud/local/browser/Chrome/computer/scheduled execution locations |
| `tool-routing-matrix.md` | selecting the authoritative interface for structured, browser, code, GUI, and artifact tasks |
| `workspace-map.md` | modeling workspace/context/process/browser state and worktree mismatches |
| `runtime-boundaries.md` | crossing local/cloud, browser, authentication, or remote boundaries |
| `activation-and-memory.md` | Skill slash activation and activation lifetime |
| `session-memory.md` | maintaining and invalidating session capability state |
| `tool-schema-literacy.md` | using unfamiliar tools from live schemas |
| `tool-use-patterns.md` | general tool-call, observation, retry, and idempotence discipline |
| `browser-workflows.md` | browser/Chrome navigation, localhost, visual checks, and browser safety |
| `webapp-verification.md` | building/fixing a web app and proving it works end-to-end |
| `artifact-lifecycle.md` | creating, rendering, verifying, saving/versioning, and sharing artifacts |
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

Do not load all references by default. Start with the smallest relevant set and cross the boundary only when the task actually enters another capability family. The runtime-aware detection/profile reference is the first stop; Desktop/Cowork snapshots are supporting context only.