"""Frontmatter reading for build-time tooling.

Why this exists: the previous packager searched for `^version:` with a regex and
silently produced `0.0.0` because the real value lives nested under `metadata:`.
A real parser is used when PyYAML is installed; otherwise a conservative,
explicitly-scoped subset parser is used so builds still work offline.

Runtime hooks must NOT import this module. Hook runtime stays dependency-free
and reads only generated JSON.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:  # pragma: no cover - availability depends on the build environment
    import yaml  # type: ignore

    _YAML_BACKEND = "pyyaml"
except ModuleNotFoundError:  # pragma: no cover
    yaml = None  # type: ignore
    _YAML_BACKEND = "builtin-subset"

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)
SEMVER = re.compile(r"\A\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\Z")
SKILL_NAME = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class FrontmatterError(ValueError):
    """Raised for any malformed or incomplete frontmatter."""


def yaml_backend() -> str:
    return _YAML_BACKEND


def split_frontmatter(text: str) -> tuple[str, str]:
    match = _FRONTMATTER.match(text)
    if not match:
        raise FrontmatterError("file must start with a closed '---' YAML frontmatter block")
    return match.group(1), text[match.end() :]


def _strip_scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def _parse_subset(block: str) -> dict[str, Any]:
    """Parse the small YAML subset this repository actually uses.

    Supported: top-level `key: value`, top-level `key:` followed by an indented
    mapping or an indented `- item` list. Anything else raises instead of
    guessing, so a build never proceeds on a misread value.
    """
    data: dict[str, Any] = {}
    current: str | None = None
    for lineno, raw_line in enumerate(block.splitlines(), start=1):
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[:1] in (" ", "\t")
        stripped = line.strip()
        if not indented:
            if ":" not in stripped:
                raise FrontmatterError(f"line {lineno}: expected 'key: value'")
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = _strip_scalar(value)
            data[key] = value if value else {}
            current = key
            continue
        if current is None:
            raise FrontmatterError(f"line {lineno}: indented value without a parent key")
        if stripped.startswith("- "):
            item = _strip_scalar(stripped[2:])
            holder = data.get(current)
            if not isinstance(holder, list):
                if isinstance(holder, dict) and not holder:
                    holder = []
                else:
                    raise FrontmatterError(f"line {lineno}: cannot mix list and mapping")
            holder.append(item)
            data[current] = holder
            continue
        if ":" not in stripped:
            raise FrontmatterError(f"line {lineno}: expected nested 'key: value'")
        key, _, value = stripped.partition(":")
        holder = data.get(current)
        if not isinstance(holder, dict):
            if isinstance(holder, str) and not holder:
                holder = {}
            else:
                raise FrontmatterError(f"line {lineno}: cannot nest inside a scalar")
        holder[key.strip()] = _strip_scalar(value)
        data[current] = holder
    return data


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    block, body = split_frontmatter(text)
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
        except Exception as exc:  # pragma: no cover - depends on input
            raise FrontmatterError(f"invalid YAML frontmatter: {exc}") from exc
    else:  # pragma: no cover - exercised only without PyYAML
        data = _parse_subset(block)
    if not isinstance(data, dict):
        raise FrontmatterError("frontmatter must be a mapping")
    return data, body


def parse_frontmatter_subset(text: str) -> tuple[dict[str, Any], str]:
    """Parse with the builtin subset parser regardless of PyYAML availability."""
    block, body = split_frontmatter(text)
    return _parse_subset(block), body


@dataclass(frozen=True)
class SkillMetadata:
    name: str
    description: str
    version: str
    license: str = ""
    compatibility: str = ""
    body: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


def load_skill_metadata(path: Path) -> SkillMetadata:
    text = path.read_text(encoding="utf-8")
    data, body = parse_frontmatter(text)

    name = str(data.get("name") or "").strip()
    if not name:
        raise FrontmatterError(f"{path.name}: frontmatter 'name' is required")
    if len(name) > 64 or not SKILL_NAME.fullmatch(name):
        raise FrontmatterError(f"{path.name}: invalid Skill name {name!r}")

    description = str(data.get("description") or "").strip()
    if not description:
        raise FrontmatterError(f"{path.name}: frontmatter 'description' is required")
    if len(description) > 1024:
        raise FrontmatterError(
            f"{path.name}: description is {len(description)} characters; limit is 1024"
        )

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        raise FrontmatterError(
            f"{path.name}: frontmatter 'metadata' mapping is required and must hold 'version'"
        )
    version = str(metadata.get("version") or "").strip()
    if not version:
        raise FrontmatterError(
            f"{path.name}: metadata.version is missing; refusing to guess a package version"
        )
    if not SEMVER.fullmatch(version):
        raise FrontmatterError(
            f"{path.name}: metadata.version {version!r} is not a MAJOR.MINOR.PATCH version"
        )

    compatibility = str(data.get("compatibility") or "").strip()
    if len(compatibility) > 500:
        raise FrontmatterError(f"{path.name}: compatibility must be <= 500 characters")

    return SkillMetadata(
        name=name,
        description=description,
        version=version,
        license=str(data.get("license") or "").strip(),
        compatibility=compatibility,
        body=body,
        raw=data,
    )
