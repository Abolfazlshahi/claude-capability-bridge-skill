# Cache and context economy (runtime reference)

This file ships inside the installed package because the operating rules below
affect how you behave during a session. It is **not** a claim that any cache
feature is enabled.

## The two problems are separate

**Prompt caching** reduces the cost of re-processing an identical prefix. It
does not:

- give the model memory of state;
- restore guidance lost to compaction;
- make the model follow instructions;
- survive a change to the earlier part of the request.

**Behavioural reliability** is about following procedure, verifying outcomes,
and not inventing capabilities. A high cache-hit rate with wrong behaviour is
worse than a lower hit rate with correct, verified work.

So: measure correctness separately from cache metrics, and prefer **total cost
per verified success** over hit-rate percentage. Never pad context to make a
cache percentage look better.

## What you can actually control from inside a session

1. **Do not rewrite stable instructions mid-session.** The kernel, profiles,
   and cards are fixed text for the life of a session. If a card is needed, it
   is *added*; nothing earlier is edited.
2. **Do not reconstruct history.** Never re-post the conversation, earlier tool
   results, or file contents "so they are fresh". Reference them instead.
3. **Append, do not mutate.** New findings belong in new messages at the end.
4. **Keep volatile data out of stable text.** No timestamps, no random ids, no
   current status inside anything that is meant to be a stable prefix.
5. **Do not churn tool definitions.** Changing the tool list or its order
   invalidates everything after it. Progressive card *reading* is not the same
   as swapping the tool list.
6. **Do not switch model, effort, or other prefix-affecting settings** mid-task
   without a reason.

## What you cannot control

- Whether the host marks anything as cacheable at all.
- Cache TTL, minimum cacheable length, eviction, and billing.
- Whether a gateway preserves, translates, or strips cache-control blocks.
- Whether the provider counts cached tokens inside total input tokens or
  reports them separately.
- Request-level versus token-weighted accounting.

Because of this: **compatibility with a message API is not support for that
API's cache controls.** A gateway can accept an Anthropic-shaped request and
still implement no caching at all.

## Honesty rules for cache statements

- Never say "caching is enabled", "cache hit rate improved", or "this saves
  N%" unless you are reading real usage fields from real responses.
- If usage fields are absent, the value is `null`/unknown - never zero.
- Do not sum cache usage across providers without normalizing their accounting.
- Offline file/JSON comparison proves **text stability**, not cache behaviour.
  Call it an invariant check, never a benchmark.
- Cold-start cost is part of total cost. Do not report warm-session numbers as
  if they were the whole picture.

## Security outranks cache

Never keep a revoked permission, an unauthorized tool, or stale credentials
"warm" to preserve a reusable prefix. Permission is re-checked at call time,
every time.

## Related

- `references/provider-adaptation.md`
- `references/custom-provider-transport.md`
- `cards/provider-gateway.md`
