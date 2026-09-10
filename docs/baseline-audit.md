# Baseline audit (pre-refactor)

Recorded before any behavioural change, so the refactor can be compared against
real observations instead of assumptions.

## Environment actually used

| Item | Value |
| --- | --- |
| OS | Amazon Linux 2023 sandbox (Linux) |
| Python | 3.13.14 |
| PyYAML | 6.0.3 (available in the audit sandbox) |
| git | 2.49.0 |
| Claude Code | **not installed** - no live host run was performed |
| Model / gateway / provider | **none exercised** - no live inference, no cache measurement |

Everything below is a static/offline observation of this repository. None of it
is evidence about how a third-party model behaves in a real Claude Code session.

## Side-effect review before executing scripts

`scripts/` and `bootstrap/` were scanned for destructive or networked calls
before anything was run:

* `shutil.rmtree` appears in `scripts/package_skill.py`, `scripts/package_claude_code_plugin.py`
  and `scripts/validate_skill.py`, in all cases scoped to `dist/`.
* `subprocess.run` in `scripts/validate_skill.py` is used for `bash -n` syntax
  checks and for invoking the packagers.
* No network access, no `pip install`, no `eval`, and no writes outside the repo
  were found.

Conclusion: safe to execute locally.

## Reproduced findings

### Bug A - references missing from the plugin package (confirmed)

`scripts/package_claude_code_plugin.py` copies `SKILL.md` and the three hook
scripts only. The built plugin contained exactly six files:

```text
.claude-plugin/plugin.json
SKILL.md
hooks/hooks.json
scripts/post-tool-use-failure.sh
scripts/session-start.sh
scripts/user-prompt-submit.sh
```

`SKILL.md` links to 10 local `references/*.md` files; **10 of 10 were missing**
from the built plugin, so every progressive-disclosure link is dangling once the
plugin is installed away from the source checkout.

### Bug B - wrong plugin version (confirmed)

`SKILL.md` frontmatter carries the version nested under `metadata:`:

```yaml
metadata:
  project: claude-capability-bridge
  version: "0.8.0"
```

The packager searched for `^version:` at line start, missed the indented key,
and fell back to its default. Observed result:

```text
source metadata.version = 0.8.0
built plugin.version    = 0.0.0
```

A wrong manifest version breaks plugin update detection, and the silent default
hid the problem.

### Bug C - validator reported PASS anyway (confirmed)

With A and B both true, `python3 scripts/validate_skill.py` exited `0` and
printed `PASS: ... plugin packaging ... passed`. The validator checked the
*source tree*, not the *built artifact*, so it could not see either defect.

### Bug D - hooks ignore their input (confirmed, with a caveat)

`bootstrap/user-prompt-submit.sh` and `bootstrap/post-tool-use-failure.sh` are
fixed `cat <<'JSON'` heredocs. They never read stdin, so an unrelated prompt and
a tool-schema failure receive byte-identical guidance.

Caveat, recorded deliberately: this is a **relevance and context-growth**
problem, not proof of cache invalidation. Hook output is appended as new
conversation context, so it does not rewrite an already-cached prefix. The real
costs are wasted input tokens every turn, earlier compaction, and guidance that
does not match the actual failure. Any cache claim needs a live trace.

## Explicitly *not* a bug

`SKILL.md` at the plugin root is valid for a single-skill plugin in current
Claude Code (no `skills/` directory and no `skills` manifest field). This was
left as-is and must not be "fixed".

## What was already correct and must not regress

* `scripts/package_skill.py` already shipped `references/` and `LICENSE`.
* Hook JSON already used the documented
  `hookSpecificOutput.hookEventName` / `additionalContext` shape.
* `SessionStart` already matched `startup|resume|clear|compact|fork`.
* Plugin hook commands already used `${CLAUDE_PLUGIN_ROOT}`.
* The Skill name `claude-capability-bridge` is a public contract.

## Exit criteria for phase 1

* Bugs A, B, C, D reproduced on this checkout: **done**.
* Packaging regression tests written before the fix and observed failing:
  see `tests/python/test_packaging.py`.
* Pre-existing correct behaviour catalogued above so the refactor does not
  silently drop it.
