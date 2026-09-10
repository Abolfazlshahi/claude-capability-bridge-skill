---
id: provider-gateway
title: Provider, gateway, and model-transport boundaries
summary: Diagnose failures that come from the model transport rather than the task, without inventing provider features or claiming cache behaviour.
task_families:
  - provider
  - transport
signals:
  - gateway
  - provider
  - proxy
  - base url
  - api key
  - model name
  - streaming
  - token limit
  - context window
  - prompt cache
  - caching
  - anthropic-compatible
  - openai-compatible
  - rate limit
conceptual_capabilities:
  - model transport
  - tool-call translation
  - prompt caching
  - usage accounting
related_references:
  - references/provider-adaptation.md
  - references/custom-provider-transport.md
  - references/runtime-boundary-matrix.md
essentials:
  - Message-format compatibility does not imply identical tool, streaming, or cache semantics.
  - Cache behaviour, TTL, minimum length, and billing belong to the provider and gateway - never to this Skill.
  - Never report a cache hit rate or an enabled cache feature without real usage numbers from the response.
---

# Provider, gateway, and model-transport boundaries

## Purpose

Separate "the task is hard" from "the transport between host and model is
lossy", so failures are attributed to the right layer and no provider feature
is assumed.

## Use when

- Tool calls are dropped, malformed, or silently reshaped.
- Behaviour differs between hosts with the same instructions.
- The user asks about caching, token accounting, context limits, or costs.
- A custom base URL, proxy, or compatibility layer is in play.

## Do not use when

- The failure has a local explanation (bad path, missing dependency, denied
  permission). Exhaust those first.
- The user wants task work. Do not turn a normal request into a transport
  investigation.

## Required evidence

1. Which host is running, and whether a non-default endpoint is configured.
2. Observable symptoms: what was sent, what came back, which fields were lost.
3. Real usage numbers from responses, if the host surfaces them at all.
4. Whether the same input behaves differently on a known-good path.

If the host exposes none of this, the honest status is `UNOBSERVABLE`.

## Live tool-contract source

The host's own configuration and whatever the response actually returns. Not
the provider's marketing page, and not this repository. A gateway may accept a
request shape while translating away tool blocks, cache controls, or streaming
semantics.

## Minimal workflow

1. Rule out local causes first.
2. Identify the transport: default vendor path, custom endpoint, or a
   compatibility gateway.
3. Characterize the symptom precisely: tool block dropped, arguments mangled,
   truncated output, refused parameter, inconsistent streaming.
4. Reduce to the smallest reproducible case.
5. Attribute to a layer only with evidence. Otherwise report competing
   hypotheses and what would distinguish them.
6. Report the boundary and what the user would have to change. Do not enable
   provider flags speculatively.

**Anti-pattern:** setting an optional transport or caching feature flag "because
the endpoint looks Anthropic-compatible". Unsupported blocks can be stripped or
rejected, and a rewritten prefix costs more than it saves.

## Cache-specific rules

- This Skill can only keep its **own** text stable and append-only. It cannot
  turn caching on, cannot set TTL, and cannot guarantee a cache hit.
- Compatibility with a message API is not support for that API's cache
  controls.
- Never state a cache hit rate, cache savings, or "caching enabled" unless real
  usage fields from the actual responses are in hand.
- Providers differ in whether cached tokens are counted inside total input
  tokens or reported separately. Do not sum across providers without
  normalizing.
- Request-level hit rate and token-weighted hit rate are different metrics.
- See `docs/cache-contract.md` for the ownership split and
  `scripts/analyze_trace.py` for offline prefix-stability checks (an
  invariant checker, not a cache simulator).

## Verification

Done means:

- the symptom is described in terms of observed request/response evidence;
- the attribution names a layer and the evidence for it, or explicitly says
  UNKNOWN;
- any numbers reported come from real usage fields, never from estimation.

## Common failures

- Tool-use blocks dropped in translation, so the model appears to ignore tools.
- Parameter accepted by the gateway but ignored downstream.
- Context window smaller than assumed, causing silent truncation.
- Model alias pointing at a different model than the name suggests.
- Rate limits reported as generic failures.
- Usage fields absent, then treated as zero instead of unknown.

## Recovery

- Dropped tool calls: report the transport boundary; do not compensate by
  restating instructions every turn.
- Rejected parameter: remove it rather than retrying variants blindly.
- Truncation: shorten deliberately and say what was omitted.
- Missing usage data: report `null`/unknown. Never fabricate zeros.
- Unclear layer: state both hypotheses and the smallest test that would
  separate them.

## Related deep references

- `references/provider-adaptation.md`
- `references/custom-provider-transport.md`
- `references/runtime-boundary-matrix.md`
- `references/evaluation-and-attribution.md`
