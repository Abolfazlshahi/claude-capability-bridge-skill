# Research Source Notes

The bridge is intentionally based on public documentation and does not attempt to reproduce private prompts or undocumented internals. Re-check these sources when updating the Skill.

## Anthropic first-party sources

- Claude Help Center — What are Skills?
  https://support.claude.com/en/articles/12512176-what-are-skills
- Claude Help Center — Use the built-in browser in Claude Cowork
  https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork
- Claude Help Center — Let Claude use your computer in Cowork
  https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- Claude Help Center — What are Projects?
  https://support.claude.com/en/articles/9517075-what-are-projects
- Claude Help Center — Use plugins in Claude
  https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- Claude Help Center — Assign tasks from anywhere in Claude Cowork
  https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork
- Claude Platform Docs — Using Agent Skills with the API
  https://platform.claude.com/docs/en/build-with-claude/skills-guide
- Anthropic Skills repository
  https://github.com/anthropics/skills
- Agent Skills specification
  https://agentskills.io/specification

## Source interpretation rules

1. Prefer first-party documentation over community summaries.
2. Treat current help-center availability and plan/OS details as time-sensitive.
3. Do not turn one implementation example into a universal runtime guarantee.
4. Separate public behavior from inferred internal architecture.
5. When a feature is in beta/gradual rollout, treat availability as environment-dependent.
6. Never encode a private or undocumented tool name into the workflow contract merely because it appeared in an external example.
