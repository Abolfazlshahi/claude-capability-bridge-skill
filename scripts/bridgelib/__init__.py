"""Build-time helpers shared by the packagers, the validator, and the tests.

This package is development/build tooling. It is never shipped inside an
installable package and the hook runtime never imports it.
"""

from __future__ import annotations

from . import cards, payload, refs
from .frontmatter import (
    FrontmatterError,
    SkillMetadata,
    load_skill_metadata,
    parse_frontmatter,
    parse_frontmatter_subset,
    yaml_backend,
)
from .payload import BuildError, BuildResult, build_plugin_package, build_skill_package

__all__ = [
    "BuildError",
    "BuildResult",
    "FrontmatterError",
    "SkillMetadata",
    "build_plugin_package",
    "build_skill_package",
    "cards",
    "load_skill_metadata",
    "parse_frontmatter",
    "parse_frontmatter_subset",
    "payload",
    "refs",
    "yaml_backend",
]
