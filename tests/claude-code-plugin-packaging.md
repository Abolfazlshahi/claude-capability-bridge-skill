# Regression test: Claude Code plugin packaging

## Scenario
Build the bridge as a Claude Code plugin so the Skill and its optional SessionStart bootstrap can be distributed together.

## Required behavior

1. Generate a plugin with a valid `.claude-plugin/plugin.json` manifest.
2. Bundle the current `SKILL.md` without silently changing its procedural content.
3. Bundle a `hooks/hooks.json` SessionStart hook and its script.
4. Use `${CLAUDE_PLUGIN_ROOT}` for plugin-local scripts rather than project-root assumptions.
5. Keep the bootstrap advisory/contextual; it must not claim to grant tools or bypass permissions.
6. Keep plugin generation reproducible from the repository source files.

## Failure signatures

Fail the test if:

- the generated plugin contains a stale copy of the Skill that differs from the source;
- hook configuration points at an absolute machine-specific path;
- the hook is presented as universal deterministic enforcement;
- plugin generation requires manual copying of the Skill;
- the generated manifest or hooks JSON is invalid.
