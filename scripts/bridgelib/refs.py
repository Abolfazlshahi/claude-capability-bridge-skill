"""Local reference extraction and closure checks.

Progressive disclosure only works if every link that ships inside a package can
be opened from inside that same package. Bug A happened because nothing checked
that property on the built artifact.
"""

from __future__ import annotations

import re
from pathlib import Path

# Directories whose files must always travel with an installable package.
PACKAGED_PREFIXES = ("references/", "cards/", "profiles/")

_MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
_INLINE_CODE = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|json|ya?ml|sh|ps1|py))`")
_BARE_CONTENT = re.compile(
    r"(?<![\w./$-])((?:references|cards|profiles)/[A-Za-z0-9_./-]+\.(?:md|json))"
)


def extract_references(text: str) -> set[str]:
    """Return relative local paths referenced by Markdown-ish text."""
    found: set[str] = set()
    for match in _MD_LINK.finditer(text):
        target = match.group(1).strip()
        if not target or "://" in target or target.startswith(("#", "mailto:", "/")):
            continue
        if "${" in target or "$(" in target:
            continue
        found.add(target.split("#", 1)[0])
    for match in _INLINE_CODE.finditer(text):
        found.add(match.group(1))
    for match in _BARE_CONTENT.finditer(text):
        found.add(match.group(1))
    return {ref for ref in found if ref and not ref.startswith(("http", "/"))}


def packaged_references(text: str) -> set[str]:
    return {ref for ref in extract_references(text) if ref.startswith(PACKAGED_PREFIXES)}


def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def missing_references(root: Path) -> list[str]:
    """Report `file -> reference` pairs whose target does not exist under root."""
    problems: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for ref in sorted(packaged_references(text)):
            if not (root / ref).exists():
                problems.append(f"{path.relative_to(root).as_posix()} -> {ref}")
    return problems


def reference_closure(root: Path, seeds: list[str]) -> set[str]:
    """Transitively follow packaged references starting from seed files."""
    seen: set[str] = set()
    queue = list(seeds)
    while queue:
        rel = queue.pop()
        if rel in seen:
            continue
        seen.add(rel)
        path = root / rel
        if not path.is_file() or path.suffix != ".md":
            continue
        for ref in packaged_references(path.read_text(encoding="utf-8")):
            if ref not in seen:
                queue.append(ref)
    return seen
