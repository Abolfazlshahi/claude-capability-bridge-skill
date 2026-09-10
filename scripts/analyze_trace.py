#!/usr/bin/env python3
"""Offline prefix-stability checker for request traces you captured yourself.

SCOPE - read this before quoting any output from this tool:

It compares request JSON. It can show whether the text this project sends stays
stable, and it can echo usage numbers a provider already reported. It cannot
prove tokenizer behaviour, routing, TTL, eviction, billing, or backend cache
state. It is NOT a provider cache simulator. For a gateway, capture the request
AFTER translation: only the outgoing request reaches the provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCOPE = (
    "SCOPE: offline comparison of captured request JSON. It cannot prove provider "
    "cache behaviour, tokenizer behaviour, TTL, routing, or billing. It is not a "
    "provider cache simulator. For a gateway, capture the request AFTER "
    "translation, because only the outgoing request reaches the provider."
)

SECTIONS = ("tools", "system", "messages")
USAGE_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)
HOOK_MARKERS = ("CAPABILITY BRIDGE", "Capability card:", "TOOL FAILURE CLASS:")


class TraceError(Exception):
    """The trace could not be read as a request trace."""


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()[:16]


def as_blocks(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    return [value]


def iter_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


# ----------------------------------------------------------------------- loading


def normalise_record(index: int, raw) -> dict:
    if not isinstance(raw, dict):
        raise TraceError(f"record {index} is not a JSON object")
    request = raw.get("request") if isinstance(raw.get("request"), dict) else raw
    usage = None
    if isinstance(raw.get("usage"), dict):
        usage = raw["usage"]
    elif isinstance(raw.get("response"), dict) and isinstance(
        raw["response"].get("usage"), dict
    ):
        usage = raw["response"]["usage"]
    label = raw.get("label") or raw.get("name") or f"request[{index}]"
    return {
        "label": str(label),
        "request": request,
        "usage": usage,
        "synthetic": bool(raw.get("synthetic")),
    }


def load_records(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise TraceError(f"cannot read {path}: {error}") from error
    try:
        data = json.loads(text)
    except ValueError:
        data = []
        for number, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except ValueError as error:
                raise TraceError(
                    f"{path.name}: line {number} is not valid JSON or JSONL"
                ) from error
        if not data:
            raise TraceError(f"{path.name} is not valid JSON or JSONL")
    synthetic = False
    if isinstance(data, dict):
        synthetic = bool(data.get("synthetic"))
        for key in ("records", "requests", "trace"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            data = [data]
    if not isinstance(data, list) or not data:
        raise TraceError(f"{path.name} contains no request records")
    records = [normalise_record(index, raw) for index, raw in enumerate(data)]
    if synthetic:
        for record in records:
            record["synthetic"] = True
    return records


# ------------------------------------------------------------------- comparison


def fingerprint(request: dict) -> dict:
    out = {}
    for section in SECTIONS:
        present = section in request and request[section] is not None
        blocks = as_blocks(request.get(section))
        out[section] = {
            "present": present,
            "blocks": len(blocks) if present else None,
            "chars": len(canonical(request[section])) if present else None,
            "whole": digest(request.get(section)) if present else None,
            "digests": [digest(block) for block in blocks],
        }
    return out


def preview(value) -> str:
    text = canonical(value)
    return text[:120] + ("..." if len(text) > 120 else "")


def compare(first: dict, second: dict):
    """Return the first divergent region, walking the request in prefix order."""
    for section in SECTIONS:
        left = as_blocks(first["request"].get(section))
        right = as_blocks(second["request"].get(section))
        for index in range(min(len(left), len(right))):
            if digest(left[index]) != digest(right[index]):
                return {
                    "section": section,
                    "index": index,
                    "kind": "rewritten",
                    "left_preview": preview(left[index]),
                    "right_preview": preview(right[index]),
                }
        if len(right) > len(left):
            return {
                "section": section,
                "index": len(left),
                "kind": "appended",
                "left_preview": None,
                "right_preview": preview(right[len(left)]),
            }
        if len(left) > len(right):
            return {
                "section": section,
                "index": len(right),
                "kind": "removed",
                "left_preview": preview(left[len(right)]),
                "right_preview": None,
            }
    return None


def hook_texts(request: dict) -> list:
    found = []
    for section in ("system", "messages"):
        for block in as_blocks(request.get(section)):
            for text in iter_strings(block):
                if any(marker in text for marker in HOOK_MARKERS):
                    found.append(text.strip())
    return found


def usage_values(record: dict) -> dict:
    usage = record["usage"] or {}
    values = {}
    for field in USAGE_FIELDS:
        raw = usage.get(field)
        # Absent stays None. A reported 0 is kept, because "the provider said
        # zero" and "we do not know" are different facts.
        values[field] = raw if isinstance(raw, (int, float)) else None
    return values


def analyse(records: list, sources: list) -> dict:
    fingerprints = [
        {"label": record["label"], "sections": fingerprint(record["request"])}
        for record in records
    ]
    comparisons = []
    for index in range(len(records) - 1):
        divergence = compare(records[index], records[index + 1])
        comparisons.append(
            {
                "from": records[index]["label"],
                "to": records[index + 1]["label"],
                "divergence": divergence,
                "prefix_preserved": divergence is None
                or divergence["kind"] == "appended",
            }
        )
    variants = []
    for record in records:
        for text in hook_texts(record["request"]):
            if text not in variants:
                variants.append(text)
    return {
        "scope": SCOPE,
        "sources": sources,
        "synthetic": any(record["synthetic"] for record in records),
        "records": fingerprints,
        "comparisons": comparisons,
        "hook_text": {
            "variants": len(variants),
            "stable": len(variants) <= 1,
            "samples": [text[:100] for text in variants[:4]],
        },
        "usage": [
            {"label": record["label"], "values": usage_values(record)}
            for record in records
        ],
        "verdict": {
            "compared_pairs": len(comparisons),
            "prefix_preserved": all(item["prefix_preserved"] for item in comparisons),
            "comparable": len(records) > 1,
        },
    }


# ---------------------------------------------------------------------- output


def render_json(report: dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)


def render_text(report: dict) -> str:
    lines = ["CAPABILITY BRIDGE - offline trace analysis", report["scope"], ""]
    if report["synthetic"]:
        lines.append("INPUT IS A SYNTHETIC FIXTURE: the numbers below are invented.")
        lines.append("")
    lines.append(f"sources: {', '.join(report['sources'])}")
    lines.append(f"records: {len(report['records'])}")
    lines.append("")
    lines.append("requests")
    for index, record in enumerate(report["records"]):
        parts = []
        for section in SECTIONS:
            data = record["sections"][section]
            if not data["present"]:
                parts.append(f"{section}=absent")
            else:
                parts.append(f"{section}={data['blocks']} blocks/{data['chars']} chars")
        lines.append(f"  [{index}] {record['label']}: " + "  ".join(parts))
    lines.append("")
    lines.append("comparisons")
    if not report["comparisons"]:
        lines.append("  only one request in the trace: nothing to compare")
    for index, item in enumerate(report["comparisons"]):
        divergence = item["divergence"]
        if divergence is None:
            lines.append(f"  [{index}] identical requests")
            continue
        where = f"{divergence['section']}[{divergence['index']}]"
        if divergence["kind"] == "appended":
            lines.append(f"  [{index}] prefix preserved: content appended at {where}")
        else:
            lines.append(f"  [{index}] PREFIX {divergence['kind'].upper()} at {where}")
            lines.append(f"        before: {divergence['left_preview']}")
            lines.append(f"        after : {divergence['right_preview']}")
    lines.append("")
    hook = report["hook_text"]
    state = "stable" if hook["stable"] else "UNSTABLE across requests"
    lines.append(f"bridge/hook text variants: {hook['variants']} ({state})")
    lines.append("")
    lines.append("usage as reported in the trace")
    lines.append("  unknown means the field was absent. unknown is not zero.")
    for index, row in enumerate(report["usage"]):
        rendered = " ".join(
            f"{field}="
            + ("unknown" if row["values"][field] is None else str(row["values"][field]))
            for field in USAGE_FIELDS
        )
        lines.append(f"  [{index}] {rendered}")
    lines.append("")
    lines.append("verdict")
    if not report["verdict"]["comparable"]:
        lines.append("  not comparable: capture at least two requests")
    lines.append(
        "  prefix preserved across compared requests: "
        + ("yes" if report["verdict"]["prefix_preserved"] else "no")
    )
    lines.append(
        "  this says nothing about whether the provider actually served a cache "
        "read; only live usage fields can show that."
    )
    return "\n".join(lines)


# -------------------------------------------------------------------- selftest


def selftest() -> int:
    fixtures = Path(__file__).resolve().parents[1] / "benchmarks" / "fixtures"
    stable = analyse(load_records(fixtures / "trace-stable-prefix.json"), ["stable"])
    assert stable["verdict"]["prefix_preserved"], "stable fixture must preserve prefix"
    assert stable["hook_text"]["variants"] == 1, stable["hook_text"]
    assert any(
        row["values"]["cache_read_input_tokens"] is None for row in stable["usage"]
    ), "fixture must exercise a missing usage field"
    assert any(
        row["values"]["cache_read_input_tokens"] == 0 for row in stable["usage"]
    ), "fixture must exercise a reported zero"
    rewritten = analyse(
        load_records(fixtures / "trace-rewritten-prefix.json"), ["rewritten"]
    )
    assert not rewritten["verdict"]["prefix_preserved"]
    sections = [
        item["divergence"]["section"]
        for item in rewritten["comparisons"]
        if item["divergence"]
    ]
    assert "system" in sections and "tools" in sections, sections
    assert rewritten["hook_text"]["variants"] > 1
    print("OK: offline trace analysis selftest passed (synthetic fixtures only).")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Offline prefix-stability checker for captured request traces.",
        epilog=SCOPE,
    )
    parser.add_argument("traces", nargs="*", type=Path, help="trace files (JSON/JSONL)")
    parser.add_argument("--json", dest="as_json", action="store_true")
    parser.add_argument(
        "--fail-on-rewrite",
        action="store_true",
        help="exit 1 when a compared request rewrote an earlier region",
    )
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.traces:
        print("ERROR: give at least one trace file, or --selftest", file=sys.stderr)
        return 2
    records = []
    try:
        for path in args.traces:
            records.extend(load_records(path))
    except TraceError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    report = analyse(records, [str(path) for path in args.traces])
    print(render_json(report) if args.as_json else render_text(report))
    if args.fail_on_rewrite and not report["verdict"]["prefix_preserved"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
