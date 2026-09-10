---
id: delegation-context
title: Delegation, subagents, and context boundaries
summary: Delegated and resumed runs have their own context; files, credentials, processes, and browser state do not transfer implicitly.
task_families:
  - delegation
  - context-lifecycle
signals:
  - subagent
  - agent
  - delegate
  - parallel
  - remote
  - resume
  - compact
  - continue
  - handoff
  - scheduled
  - trigger
conceptual_capabilities:
  - spawn subagent
  - delegate task
  - background run
  - resume session
related_references:
  - references/async-subagents-and-remote.md
  - references/session-memory.md
  - references/runtime-boundaries.md
essentials:
  - A delegated run starts with its own context; it does not see your conversation, files, or logins unless they are passed explicitly.
  - After compact, clear, fork, or resume, treat earlier observations as STALE until re-observed.
  - Pass instructions and inputs by value; never assume shared localhost, shared browser session, or shared credentials.
---

# Delegation, subagents, and context boundaries

## Purpose

Split work across runs, or continue after a context change, without silently
losing the state that made the earlier work valid.

## Use when

- The host offers subagents, background runs, or scheduled/triggered runs and
  the task genuinely benefits from separation.
- Work must continue after compaction, clearing, forking, or resuming.
- A long task needs to be handed to another run with clear inputs.

## Do not use when

- The task is short and local. Delegation adds coordination cost and a fresh
  context that knows nothing.
- No delegation capability is exposed. Do not describe a subagent you cannot
  create.
- The work needs your live processes or authenticated browser session, which do
  not transfer.

## Required evidence

1. A delegation capability is exposed, with its own schema.
2. What the delegated run inherits - usually much less than assumed. Check
   filesystem, credentials, network, and tool access separately.
3. Whether the delegated run can report back, and how you receive its result.
4. Whether a human is present to answer questions. Scheduled runs usually have
   nobody.

## Live tool-contract source

The delegation tool's schema plus whatever the host documents about the child
run's environment. Treat "same machine" as unproven unless stated. If the
contract is silent, assume nothing is inherited.

## Minimal workflow

1. Decide whether separation actually helps. If not, do the work here.
2. Write the delegated instruction to be self-contained: objective, inputs,
   constraints, definition of done, and what to report.
3. Pass data by value or by a path the child can genuinely reach.
4. Start the run, then treat its output as a report you must validate, not as
   verified truth.
5. Verify the claimed effects yourself in your own context before telling the
   user it happened.

**Anti-pattern:** telling a subagent to "continue where I left off" or to "use
the server I started". It has neither your history nor your process.

## Context-change handling

- **compact** - the transcript was summarized. Restore the minimum operating
  rules and re-verify anything you are about to rely on. Do not re-inject the
  whole library.
- **clear** - new context. Nothing carries over.
- **fork** - a sibling context. Processes, browser sessions, and auth state are
  not shared.
- **resume** - decide from host evidence. When unclear, rehydrate
  conservatively and re-observe rather than trusting a stale note.

## Verification

Done means:

- the delegated run's claims were checked against real evidence in your
  context;
- inputs actually reached the child (no missing file, no unreachable path);
- after a context change, every fact you rely on was either re-observed or is
  explicitly labelled `STALE`/`UNKNOWN`.

## Common failures

- Child run has no access to the file or repository you referenced.
- Child run lacks credentials or connector scopes you have.
- `localhost` in the child points at a different machine or nothing at all.
- Two runs writing the same file, and the later write wins silently.
- After compaction, acting on an identifier or plan that no longer exists.
- Reporting a delegated claim as verified fact.

## Recovery

- Child failed on access: pass the content inline, or do the step yourself.
- Missing credentials in the child: do not forward secrets. Re-scope the task
  so the authenticated part stays where the credentials legitimately live.
- Post-compaction confusion: re-read the current state of the target, then
  continue from evidence rather than from memory.
- No human available in an automated run: stop at the decision point and report
  it instead of assuming consent.

## Related deep references

- `references/async-subagents-and-remote.md`
- `references/session-memory.md`
- `references/runtime-boundaries.md`
- `references/activation-and-memory.md`
