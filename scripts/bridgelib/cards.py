"""Capability-card index generation.

The card catalog is generated at build time from card frontmatter and committed
as plain JSON. Two consequences that matter:

* the hook runtime needs no YAML parser and no model call to route a task;
* routing signals are reviewable in a diff instead of being re-invented per turn.

The index is NOT a registry of tools that exist. It maps task families to
procedural guidance. Whether a tool exists and is permitted is always decided
from live host evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .frontmatter import FrontmatterError, parse_frontmatter

INDEX_NAME = "index.json"
INDEX_VERSION = 1
REQUIRED_KEYS = ("id", "title", "summary")
REQUIRED_SECTIONS = (
    "## Purpose",
    "## Use when",
    "## Do not use when",
    "## Required evidence",
    "## Live tool-contract source",
    "## Minimal workflow",
    "## Verification",
    "## Common failures",
    "## Recovery",
    "## Related deep references",
)


def card_files(cards_dir: Path) -> list[Path]:
    return sorted(p for p in cards_dir.glob("*.md") if p.is_file())


def _as_list(value: Any, path: Path, key: str) -> list[str]:
    if value in (None, "", {}, []):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    raise FrontmatterError(f"{path.name}: '{key}' must be a string or list")


def load_card(path: Path) -> dict[str, Any]:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    for key in REQUIRED_KEYS:
        if not str(data.get(key) or "").strip():
            raise FrontmatterError(f"{path.name}: card frontmatter '{key}' is required")
    card_id = str(data["id"]).strip()
    if card_id != path.stem:
        raise FrontmatterError(
            f"{path.name}: card id {card_id!r} must match the file name {path.stem!r}"
        )
    missing = [section for section in REQUIRED_SECTIONS if section not in body]
    if missing:
        raise FrontmatterError(f"{path.name}: missing required sections: {missing}")
    return {
        "id": card_id,
        "title": str(data["title"]).strip(),
        "summary": str(data["summary"]).strip(),
        "path": f"cards/{path.name}",
        "task_families": sorted(set(_as_list(data.get("task_families"), path, "task_families"))),
        "signals": sorted(set(s.lower() for s in _as_list(data.get("signals"), path, "signals"))),
        "conceptual_capabilities": sorted(
            set(_as_list(data.get("conceptual_capabilities"), path, "conceptual_capabilities"))
        ),
        "related_references": sorted(
            set(_as_list(data.get("related_references"), path, "related_references"))
        ),
        "essentials": _as_list(data.get("essentials"), path, "essentials"),
    }


def build_index(cards_dir: Path) -> dict[str, Any]:
    cards = [load_card(path) for path in card_files(cards_dir)]
    ids = [card["id"] for card in cards]
    duplicates = sorted({cid for cid in ids if ids.count(cid) > 1})
    if duplicates:
        raise FrontmatterError(f"duplicate card ids: {duplicates}")
    return {
        "index_version": INDEX_VERSION,
        "generated_by": "scripts/build_card_index.py",
        "note": (
            "Task-family routing table. Conceptual capability names are not callable "
            "tool names, and nothing here proves a tool exists or is permitted."
        ),
        "cards": cards,
    }


def render_index(index: dict[str, Any]) -> str:
    return json.dumps(index, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def verify_index(cards_dir: Path) -> dict[str, Any]:
    """Rebuild the index and confirm the committed file matches byte for byte."""
    index_path = cards_dir / INDEX_NAME
    expected = render_index(build_index(cards_dir))
    if not index_path.is_file():
        raise FrontmatterError(
            f"{index_path} is missing; run scripts/build_card_index.py"
        )
    actual = index_path.read_text(encoding="utf-8")
    if actual != expected:
        raise FrontmatterError(
            "cards/index.json is out of date; run scripts/build_card_index.py"
        )
    return json.loads(actual)
