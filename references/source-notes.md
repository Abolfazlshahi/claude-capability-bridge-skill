# Research Source Notes

_Last reviewed: 2026-09-08._

This project models public, reproducible behavior. It does not claim to reproduce private system prompts, weights, internal classifiers, undocumented orchestration, or private tool names.

## Primary sources checked

### Claude Desktop / Cowork
- Claude — **The Claude Cowork product guide** — 2026-06-05
  https://claude.com/blog/the-claude-cowork-product-guide
- Claude — **Get Claude's own browser in Cowork** — 2026-08-26
  https://claude.com/blog/cowork-built-in-browser
- Claude Help Center — **Use the built-in browser in Claude Cowork**
  https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork
- Claude Help Center — **Let Claude use your computer in Cowork**
  https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- Claude — **Put Claude to work on your computer** — 2026-03-23
  https://claude.com/blog/dispatch-and-computer-use
- Claude Help Center — **Use Claude Cowork on web, desktop, and mobile**
  https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- Claude Help Center — **Schedule recurring tasks in Claude Cowork**
  https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork

### Browser / safety
- Claude Help Center — **Get started with Claude in Chrome**
  https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome
- Claude Help Center — **Use Claude in Chrome safely**
  https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely
- Claude Help Center — **Claude in Chrome permissions guide**
  https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide
- Claude Help Center — **Claude in Chrome troubleshooting**
  https://support.claude.com/en/articles/12902405-claude-in-chrome-troubleshooting
- Claude Help Center — **Set up browser use in Claude Cowork for Team and Enterprise plans**
  https://support.claude.com/en/articles/16635803-set-up-browser-use-in-claude-cowork-for-team-and-enterprise-plans

### MCP / connectors / local extensions
- Claude Help Center — **Get started with custom connectors using remote MCP**
  https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- Claude Help Center — **Getting Started with Local MCP Servers on Claude Desktop** — 2026-06-30
  https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- Claude Help Center — **When to use desktop and web connectors** — 2026-08-06
  https://support.claude.com/en/articles/11725091-use-desktop-and-web-connectors
- Claude Help Center — **Deploying enterprise-grade MCP servers with desktop extensions** — 2026-08-05
  https://support.claude.com/en/articles/12702546-deploying-enterprise-grade-mcp-servers-with-desktop-extensions
- Claude Help Center — **Use interactive connectors in Claude**
  https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude

### Artifacts / plugins / agent workflows
- Claude Help Center — **Use artifacts in Claude Cowork**
  https://support.claude.com/en/articles/14729249-use-artifacts-in-claude-cowork
- Claude — **Customize Cowork with plugins** — 2026-01-30
  https://claude.com/blog/cowork-plugins
- Claude — **Skills explained: How Skills compares to prompts, Projects, MCP, and subagents** — 2026-03-05
  https://claude.com/blog/skills-explained
- Claude — **Common workflow patterns for AI agents—and when to use them** — 2026-03-05
  https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them
- Claude — **Building Agents with Skills: Equipping Agents for Specialized Work** — 2026-01-22
  https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work

### Skills standard / implementation references
- Agent Skills — **Specification**
  https://agentskills.io/specification
- Anthropic — **Public Agent Skills repository**
  https://github.com/anthropics/skills
- Anthropic — **skill-creator SKILL.md**
  https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

## Interpretation rules

1. Prefer first-party documentation over community summaries.
2. Treat plan, OS, admin, beta, rollout, and availability details as time-sensitive.
3. Distinguish public product behavior from inference about internal implementation.
4. A model-facing Skill can supply procedural knowledge, but cannot manufacture a missing runtime capability.
5. Do not use a single product example as proof that every host, provider, model, or release behaves identically.
6. Re-check this source list and the current capability map after significant Claude Desktop/Cowork releases.
