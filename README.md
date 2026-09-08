# Claude Capability Bridge Skill

> A deep procedural capability layer for third-party and custom-provider models running inside Claude Desktop-like Agent Skills runtimes.

[![Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20Capability%20Bridge-6f42c1)](./SKILL.md)
[![Validation](https://img.shields.io/badge/validation-offline%20validator-success)](./scripts/validate_skill.py)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## The problem

A capable model can still be a poor desktop agent.

Anthropic's own models may arrive with strong procedural familiarity: they tend to know when to use a connector, when to execute code, when to open a browser, when to escalate to computer use, and when a task is not actually verified yet. A custom provider can expose the same runtime tools while lacking those learned workflows.

This Skill makes that missing procedural knowledge explicit.

### Core invariant

```text
┌────────────────────┐
│ Capability exists  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Capability known   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Task completed     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Task verified      │
└────────────────────┘
```

**Capability available ≠ capability understood ≠ task completed ≠ task verified.**

---

## What this Skill does

```text
                 CLAUDE CAPABILITY BRIDGE
┌───────────────────────────────────────────────────────────┐
│ 1. HOST MODEL                                              │
│    runtime • OS • workspace • project • permissions       │
├───────────────────────────────────────────────────────────┤
│ 2. CAPABILITY DISCOVERY                                    │
│    files • shell • browser • Chrome • computer • MCP      │
├───────────────────────────────────────────────────────────┤
│ 3. TOOL ROUTING                                            │
│    choose the narrowest reliable execution surface        │
├───────────────────────────────────────────────────────────┤
│ 4. PROCEDURAL WORKFLOW                                     │
│    inspect → act → observe → decide                       │
├───────────────────────────────────────────────────────────┤
│ 5. VERIFICATION                                            │
│    acceptance criteria • evidence • browser checks        │
├───────────────────────────────────────────────────────────┤
│ 6. RECOVERY                                                │
│    classify → isolate → repair → re-test                   │
├───────────────────────────────────────────────────────────┤
│ 7. HONEST REPORTING                                        │
│    verified • not verified • residual risk                │
└───────────────────────────────────────────────────────────┘
```

It is intentionally a **knowledge/workflow layer**, not a runtime implementation. It cannot create a browser, computer-use tool, MCP server, filesystem mount, shell, permission, or other capability that the host does not expose.

---

## Activation

When the host exposes installed Skills as slash commands, activate it with:

```text
/claude-capability-bridge
```

The host owns command registration. Installing this repository does not itself create a slash-command UI or grant permissions.

After the host reports activation, the model should establish a session-scoped capability map and apply the Skill's routing/verification policy to the applicable task.

### Activation mental model

```text
INSTALL SKILL
     │
     ▼
HOST REGISTERS SKILL
     │
     ▼
/claude-capability-bridge
     │
     ▼
LOAD CORE POLICY (SKILL.md)
     │
     ▼
DISCOVER CURRENT RUNTIME
     │
     ├── tools
     ├── permissions
     ├── workspace/project
     ├── browser state
     └── process/environment state
     │
     ▼
CREATE SESSION CAPABILITY MAP
     │
     ▼
CONSULT ONLY RELEVANT REFERENCES
     │
     ▼
EXECUTE + VERIFY + RECOVER
```

---

## Capability coverage

The project treats Claude Desktop-like environments as a layered system rather than a single chatbot interface.

| Capability family | Procedural coverage | Main reference |
|---|---:|---|
| Runtime / host awareness | ██████████ 100% | `capability-model.md` |
| Capability discovery | ██████████ 100% | `capability-model.md` |
| Tool selection / routing | ██████████ 100% | `tool-use-patterns.md` |
| Files / Git / workspace | ██████████ 100% | `projects-and-files.md` |
| Shell / code execution | ██████████ 100% | `code-and-shell.md` |
| Browser workflows | ██████████ 100% | `browser-workflows.md` |
| Local web-app verification | ██████████ 100% | `webapp-verification.md` |
| Computer-use escalation | ██████████ 100% | `computer-use.md` |
| MCP / connectors | ██████████ 100% | `mcp-and-connectors.md` |
| MCP deep semantics | █████████░ 90% | `mcp-deep-dive.md` |
| Skills / Plugins | ██████████ 100% | `skills-and-plugins.md` |
| Projects / context separation | ██████████ 100% | `projects-and-files.md` |
| Verification / evidence | ██████████ 100% | `verification.md` |
| Failure recovery | ██████████ 100% | `failure-recovery.md` |
| Security / authorization | ██████████ 100% | `security-and-permissions.md` |
| Custom-provider adaptation | ██████████ 100% | `provider-adaptation.md` |
| Desktop / Cowork workflows | █████████░ 90% | `desktop-workflows.md` |
| Activation / session memory | ██████████ 100% | `activation-and-memory.md` |

> These are **coverage targets for the documentation**, not claims about model performance. Real model capability must be benchmarked.

### Readiness scorecard

```text
Runtime awareness        ██████████ 100%
Tool selection           ██████████ 100%
Workflow knowledge       ██████████ 100%
Browser/web verification ██████████ 100%
Failure recovery        ██████████ 100%
Security boundaries      ██████████ 100%
Desktop UX model         █████████░  90%
Activation semantics     ██████████ 100%
Tool-schema literacy     █████████░  90%
Real-model validation    █████░░░░░  50%
```

The final line is deliberately not presented as solved: the repository contains behavioral scenarios and validation tooling, but model-family benchmarking requires running those scenarios against real providers.

---

## Capability routing ladder

The bridge prefers the narrowest trustworthy surface that can satisfy the acceptance criteria.

```text
┌──────────────────────────────┐
│ Structured API / MCP / Conn. │  ← preferred for structured data/actions
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Filesystem / Git             │  ← source state and repository changes
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Shell / Code Execution       │  ← deterministic work and diagnostics
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Browser                      │  ← user-facing web behavior
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Existing Chrome Context      │  ← user-authenticated browser state
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Computer / Desktop Control   │  ← GUI-only or last-resort workflows
└──────────────────────────────┘
```

This is a heuristic, not a prohibition. A UI acceptance criterion still requires UI/browser evidence even when an API could simulate the same operation.

---

## The web-app verification engine

The flagship workflow is designed for the exact class of tasks where custom-provider agents often stop too early.

```text
┌────────────┐
│ UNDERSTAND │
└─────┬──────┘
      ▼
┌────────────┐
│  INSPECT   │
└─────┬──────┘
      ▼
┌────────────┐
│  BASELINE  │
└─────┬──────┘
      ▼
┌────────────┐
│ IMPLEMENT  │
└─────┬──────┘
      ▼
┌────────────┐
│   LAUNCH   │──────→ actual readiness + actual port/URL
└─────┬──────┘
      ▼
┌────────────┐
│   BROWSER  │──────→ rendered UI + route + visible state
└─────┬──────┘
      ▼
┌────────────┐
│ INTERACT   │──────→ critical user journeys
└─────┬──────┘
      ▼
┌────────────┐
│ DIAGNOSE   │──────→ UI → URL/state → console → network → server
└─────┬──────┘
      ▼
┌────────────┐
│   PATCH    │
└─────┬──────┘
      ▼
┌────────────┐
│ RE-VERIFY  │───────────────┐
└─────┬──────┘               │
      │ PASS                  │ FAIL
      ▼                       │
┌────────────┐                │
│ TEST/LINT  │                │
└─────┬──────┘                │
      ▼                       │
┌────────────┐       ┌────────┴────────┐
│ VISUAL QA  │       │ RECOVER / LOOP  │
└─────┬──────┘       └─────────────────┘
      ▼
┌────────────┐
│   REPORT   │
└────────────┘
```

### Truth states

```text
process running
      ≠
server listening
      ≠
HTTP responds
      ≠
app hydrated
      ≠
page is correct
      ≠
feature works
```

The Skill therefore forbids weak completion claims such as:

```text
"npm run build passed, therefore the app works"
"the page opened, therefore the feature works"
"there are no console errors, therefore the UI is correct"
```

---

## Failure recovery matrix

```text
                    FAILURE
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   TOOL LAYER      ENVIRONMENT      APP LOGIC
        │              │              │
 availability     dependency       runtime/UI
 permission       readiness        network/auth
 schema           process          state mismatch
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                    CLASSIFY
                       ▼
                    ISOLATE
                       ▼
             CHANGE ONE VARIABLE
                       ▼
                 RETRY / ESCALATE
                       ▼
                    VERIFY
```

The bridge explicitly distinguishes tool failure, permission failure, readiness failure, navigation failure, application failure, schema misuse, authentication problems, procedural misunderstanding, and authorization boundaries.

---

## Session capability map

The model should build a lightweight internal map instead of assuming a generic Claude Desktop setup exists.

```text
HOST
├── runtime identity
├── platform / OS
└── current workspace/project

CONTEXT
├── conversation
├── project knowledge
├── live filesystem/worktree
├── Git state
├── browser state
└── connector state

TOOLS
├── filesystem
├── shell/code
├── background process execution
├── browser
├── Chrome
├── screenshots / visual inspection
├── computer use
├── MCP / connectors
├── Git
├── Skills / Plugins
└── scheduling / remote dispatch

STATE
├── cwd
├── PIDs / processes
├── ports / URLs
├── current page
├── auth/session state
├── changed files
└── external side effects

PERMISSIONS
├── writable scope
├── network restrictions
├── approvals
└── sensitive-action boundaries
```

Unknown state remains unknown until evidence upgrades it.

---

## Repository architecture

```text
.
├── SKILL.md
├── README.md
├── LICENSE
│
├── references/
│   ├── activation-and-memory.md
│   ├── browser-workflows.md
│   ├── capability-catalog.md
│   ├── capability-model.md
│   ├── code-and-shell.md
│   ├── computer-use.md
│   ├── desktop-workflows.md
│   ├── failure-recovery.md
│   ├── mcp-and-connectors.md
│   ├── mcp-deep-dive.md
│   ├── projects-and-files.md
│   ├── provider-adaptation.md
│   ├── security-and-permissions.md
│   ├── skills-and-plugins.md
│   ├── task-recipes.md
│   ├── tool-use-patterns.md
│   ├── verification.md
│   ├── webapp-verification.md
│   └── README.md
│
├── scripts/
│   └── validate_skill.py
│
├── tests/
│   └── scenarios.md
│
└── .github/
    └── workflows/
        └── validate.yml
```

### Progressive disclosure

The Skill follows the same principle it teaches models:

```text
metadata
   ↓
SKILL.md
   ↓
relevant reference
   ↓
optional recipe / script
   ↓
execution
   ↓
verification
```

Do not dump every reference into context when only one capability family is relevant.

---

## What it does not do

This boundary is intentional.

```text
SKILL CAN TEACH
───────────────
✓ when to use a capability
✓ how to sequence tools
✓ how to interpret results
✓ how to verify outcomes
✓ how to recover from failures
✓ how to model session state
✓ how to avoid pretending

SKILL CANNOT CREATE
───────────────────
✗ a missing browser runtime
✗ a missing computer-use interface
✗ a missing MCP server
✗ a missing filesystem mount
✗ a missing permission
✗ a missing network path
✗ a host slash-command registry
```

A missing runtime capability is a runtime/integration problem, not a prompt problem.

---

## Validation

Run the offline validator:

```bash
python scripts/validate_skill.py
```

It checks Skill frontmatter, naming, required references, and internal reference consistency. It does **not** prove that a particular Claude Desktop release exposes every capability described by this project.

---

## Benchmarking

The repository includes model-facing behavioral scenarios because documentation coverage alone is not enough.

Recommended evaluation pattern:

```text
MODEL A (native)
       │
       ├── baseline task
       └── task + bridge Skill

MODEL B (custom)
       │
       ├── baseline task
       └── task + bridge Skill

MODEL C (custom)
       │
       ├── baseline task
       └── task + bridge Skill

                 ↓
      compare behavioral evidence
```

Useful metrics include:

```text
tool selection accuracy
first-use success rate
schema argument accuracy
unnecessary tool-call rate
verification completion rate
false-success rate
recovery success rate
critical-path coverage
permission-boundary compliance
```

The benchmark is deliberately separated from the Skill's documentation claims.

---

## Scope and maintenance

This repository models public, reproducible agent workflows. It does not claim to reproduce Anthropic's private system prompts or proprietary internal implementation.

When the host runtime, Claude Desktop capabilities, MCP behavior, browser surfaces, Skill specification, or plugin model changes:

```text
update capability catalog
        ↓
update affected reference
        ↓
update scenarios
        ↓
run validator
        ↓
re-check routing in SKILL.md
```

---

## License

MIT. See [LICENSE](./LICENSE).
