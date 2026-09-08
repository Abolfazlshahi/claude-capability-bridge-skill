# Research Source Notes

_Last reviewed: 2026-09-08._

This project models public, reproducible behavior. It does not claim to reproduce private system prompts, weights, internal classifiers, undocumented orchestration, or private tool names.

## Primary sources checked

### Claude Desktop / Cowork
- Claude — The Claude Cowork product guide — 2026-06-05
  https://claude.com/blog/the-claude-cowork-product-guide
- Claude — Get Claude's own browser in Cowork — 2026-08-26
  https://claude.com/blog/cowork-built-in-browser
- Claude Help Center — Use the built-in browser in Claude Cowork
  https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork
- Claude Help Center — Let Claude use your computer in Cowork
  https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- Claude — Put Claude to work on your computer — 2026-03-23
  https://claude.com/blog/dispatch-and-computer-use
- Claude Help Center — Use Claude Cowork on web, desktop, and mobile
  https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- Claude Help Center — Schedule recurring tasks in Claude Cowork
  https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- Claude Help Center — Claude Cowork architecture overview
  https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- Claude — Customize Cowork with plugins — 2026-01-30
  https://claude.com/blog/cowork-plugins

### Claude Code architecture and tool behavior
- Claude Code Docs — How Claude Code works
  https://code.claude.com/docs/en/how-claude-code-works
- Claude Code Docs — Tools reference
  https://code.claude.com/docs/en/tools-reference
- Claude Code Docs — Get started with the desktop app
  https://code.claude.com/docs/en/desktop-quickstart
- Claude Code Docs — Platforms and integrations
  https://code.claude.com/docs/en/platforms
- Claude Code Docs — Model configuration
  https://code.claude.com/docs/en/model-config
- Claude Code Docs — Environment variables
  https://code.claude.com/docs/en/env-vars
- Claude Code Docs — LLM gateway configuration
  https://code.claude.com/docs/en/llm-gateway
- Claude Code Docs — Connect Claude Code to tools via MCP
  https://code.claude.com/docs/en/mcp
- Claude Code Docs — Give Claude custom tools
  https://code.claude.com/docs/en/agent-sdk/custom-tools
- Claude Code Docs — Claude Code on the web
  https://code.claude.com/docs/en/web-quickstart
- Claude Code Docs — Automate work with routines
  https://code.claude.com/docs/en/routines

### Provider and policy boundaries
- Claude Code Docs — Configure server-managed settings
  https://code.claude.com/docs/en/server-managed-settings
- Claude Code Docs — Enterprise deployment overview / third-party integrations
  https://code.claude.com/docs/en/third-party-integrations

### MCP / connectors / local extensions
- Claude Help Center — Get started with custom connectors using remote MCP
  https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- Claude Help Center — Getting Started with Local MCP Servers on Claude Desktop
  https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- Claude Help Center — When to use desktop and web connectors
  https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors
- Claude Help Center — Deploying enterprise-grade MCP servers with desktop extensions
  https://support.claude.com/en/articles/12702546-deploying-enterprise-grade-mcp-servers-with-desktop-extensions
- Claude Help Center — Use interactive connectors in Claude
  https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude

### Browser / safety
- Claude Help Center — Get started with Claude in Chrome
  https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome
- Claude Help Center — Use Claude in Chrome safely
  https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely
- Claude Help Center — Claude in Chrome permissions guide
  https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide
- Claude Help Center — Claude in Chrome troubleshooting
  https://support.claude.com/en/articles/12902405-claude-in-chrome-troubleshooting
- Claude Help Center — Set up browser use in Claude Cowork for Team and Enterprise plans
  https://support.claude.com/en/articles/16635803-set-up-browser-use-in-claude-cowork-for-team-and-enterprise-plans

### Skills / plugins / agent workflows
- Claude Help Center — What are Skills?
  https://support.claude.com/en/articles/12512176-what-are-skills
- Claude — Skills explained: How Skills compares to prompts, Projects, MCP, and subagents — 2026-03-05
  https://claude.com/blog/skills-explained
- Claude — Common workflow patterns for AI agents—and when to use them — 2026-03-05
  https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them
- Claude — Building Agents with Skills: Equipping Agents for Specialized Work — 2026-01-22
  https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work
- Anthropic — Public Agent Skills repository
  https://github.com/anthropics/skills
- Anthropic — skill-creator SKILL.md
  https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
- Agent Skills — Specification
  https://agentskills.io/specification
- Agent Skills — skills-ref reference validator
  https://github.com/agentskills/agentskills/tree/main/skills-ref

## Interpretation rules

1. Prefer first-party documentation over community summaries.
2. Treat plan, OS, admin, beta, rollout, endpoint, and availability details as time-sensitive.
3. Distinguish public product behavior from inference about internal implementation.
4. A model-facing Skill can supply procedural knowledge, but cannot manufacture a missing runtime capability.
5. A gateway can be protocol-compatible while the underlying model remains behaviorally different.
6. When `ANTHROPIC_BASE_URL` or another provider routing mode changes runtime behavior, classify that as a transport/provider boundary before blaming the Skill.
7. Never encode a private or undocumented tool name into the workflow contract merely because it appeared in an external example.
8. Re-check this source list and the capability map after significant Claude Desktop/Cowork/Claude Code releases.
