# Cache contract: who controls what

This document exists so nobody - human or model - can read this repository and
conclude that installing it "enables prompt caching" or "improves cache hit
rate". It cannot do either. It can only keep its own text stable.

Design statement used everywhere in this project:

> Designed to be compatible with prefix caching. Requires verification on a
> real deployment.

Not: "guaranteed cache-hit improvement".

## Layer 1 - what the Skill controls

The Skill is Markdown. Its only cache-relevant power is **text stability**.

| Rule | Mechanism |
| --- | --- |
| The kernel does not change during a session | `SKILL.md` contains no state, timestamps, or ids; enforced by `tests/python/test_cache_invariants.py` |
| Cards are additive | A card is read/appended; the kernel is never rewritten |
| Generated files are deterministic | `cards/index.json` is byte-stable and rebuilt only by `scripts/build_card_index.py`; verified by `--check` |
| No build metadata in shipped content | No build timestamp, no random id, no host name in packaged files |
| Dynamic facts live in new messages | Kernel instructs append-only reporting |

What the Skill **cannot** do: mark a block as cacheable, set a TTL, choose a
breakpoint, or affect billing.

## Layer 2 - what the Plugin controls

The optional Claude Code plugin adds hooks. Hooks add text at the **end** of a
context, which is prefix-preserving by construction, and they can decide *when*
not to add anything at all.

| Rule | Mechanism |
| --- | --- |
| No unconditional per-turn injection | `adaptive` mode is silent on a normal turn (`bootstrap/bridge_hook.py`) |
| Card guidance is emitted at most once per epoch | Card lifecycle state in the session state file |
| Repeated failures do not explode context | Escalation cap, then silence |
| Output size is bounded | Character budget, `CLAUDE_CAPABILITY_BRIDGE_MAX_CONTEXT_CHARS` |
| Emitted text is deterministic | Same input plus same state gives byte-identical output |
| Baseline is reproducible | `legacy-every-turn` restores the old unconditional reminder |

What the Plugin **cannot** do: place content anywhere other than where the host
puts hook output, confirm that its output reached the model, or observe cache
usage. Hook stdout is best-effort: the host may time out, reject, or reorder it.
This project therefore reports card delivery as `emitted`, never as `confirmed`,
unless the host provides real evidence.

### Why per-turn injection is a cost problem, not automatically a cache problem

Appending the same reminder every turn does **not** by itself invalidate an
earlier prefix. What it does do:

- adds input tokens on every single turn;
- grows context, so compaction arrives sooner;
- keeps guidance in the conversation that may not match the current task.

So the honest claim is: `legacy-every-turn` wastes tokens and context.
Whether it changes cache hit behaviour depends on the host and gateway, and
that requires a live trace to establish - including the request **after**
gateway translation, not just the request the host sent in.

## Layer 3 - what only the Host, Gateway, or Provider controls

- whether cache control is requested at all, and where breakpoints go;
- TTL, minimum cacheable prefix length, and eviction;
- whether tool definitions and system content participate;
- whether a gateway preserves, translates, or silently strips cache blocks;
- whether cached tokens are counted inside `input_tokens` or reported
  separately (for example `cache_read_input_tokens` /
  `cache_creation_input_tokens`);
- pricing for cache writes and cache reads;
- routing and tokenizer differences between models.

Consequence: **Anthropic Messages API compatibility is not Anthropic cache
support.** A gateway can accept the request shape and implement no caching.

## Deferred / optional transport features

Recommend an optional feature (for example deferred or searchable tool
definitions) only when all three hold:

1. the installed host version supports it;
2. the gateway preserves or correctly translates the required blocks;
3. the backend model actually supports the resulting request.

Do not set an environment flag for every custom endpoint because the endpoint
"looks compatible". An unsupported block can be stripped or rejected, and a
rewritten prefix costs more than it saves.

## Metrics discipline

- Separate **behavioural success** from **cache metrics**. Report both.
- Prefer **total cost per verified success** to hit-rate percentage.
- Report cold-start and warm-session numbers separately; never drop cold start.
- Missing usage fields are `null`/unknown, never `0`.
- Do not sum cache usage across providers without normalizing accounting.
- Request-level hit rate is not token-weighted hit rate.
- If cache hits went down but total cost and time improved, say so.
- If cache hits went up but task success dropped, that is not an improvement.

## Tooling in this repository

- `scripts/analyze_trace.py` - offline prefix-stability checker. It fingerprints
  `tools`, `system`, and `messages`, finds the first divergent region between
  two requests, and extracts real usage fields when they exist. It is **not** a
  provider cache simulator: file comparison cannot prove tokenizer behaviour,
  routing, TTL, or backend cache state.
- `tests/python/test_cache_invariants.py` - invariant tests, not benchmarks.
- `benchmarks/` - definitions and a runner guide for live A/B/C/D comparison.
  Nothing in this repository executes a paid run on its own.

## Related

- `references/cache-and-context-economy.md` (ships inside the package)
- `cards/provider-gateway.md`
- `docs/baseline-audit.md`
