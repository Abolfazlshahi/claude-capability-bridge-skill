# Trace fixtures (synthetic)

Every file in this directory is hand-written. Nothing here was captured from a
real provider and none of the numbers are measurements. They exist only to
exercise the offline analyser (`scripts/analyze_trace.py`) without network
access, credentials, or paid calls.

| Fixture | What it demonstrates |
| --- | --- |
| `trace-stable-prefix.json` | `tools` and `system` stay byte-identical while `messages` grow. One record reports `cache_read_input_tokens: 0`; another omits the cache fields entirely, so the analyser must print `unknown` instead of `0`. |
| `trace-rewritten-prefix.json` | The anti-pattern: a timestamp and a turn counter live inside the system block, so it is rewritten every turn, and the tool list is reordered. The analyser must locate the first rewritten region. |

## Capturing a real trace

Store the request bodies your host actually sent, in order, as a JSON array, a
JSONL file, or an object with a `records` array. Each record may be a bare
request or `{"label": ..., "request": {...}, "usage": {...}}`.

For a gateway, capture the request **after** translation. Only the outgoing
request reaches the provider, and a gateway may add, drop, or reorder cache
blocks without telling the client.

## What a green run does not mean

A stable-prefix verdict says the text did not change. It is not evidence about
provider cache behaviour, tokenizer boundaries, TTL, eviction, or billing. Those
can only be read from live usage fields such as `cache_read_input_tokens` and
`cache_creation_input_tokens`, and they are not simulated here.
