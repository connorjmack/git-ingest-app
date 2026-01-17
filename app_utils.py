"""Small, testable helpers shared across the app."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def default_output_dir(base_file: PathLike, frozen: bool | None = None) -> Path:
    """Return the default output directory based on frozen vs. local execution."""
    is_frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if is_frozen:
        return Path.home() / "Documents" / "GitHub" / "git-ingest-output"
    base_path = Path(base_file).resolve()
    return base_path.parent / "txt_files"


def ensure_directory(path: PathLike) -> Path:
    """Create the directory (and parents) if missing, returning the Path."""
    dest = Path(path)
    dest.mkdir(parents=True, exist_ok=True)
    return dest


__all__ = ["default_output_dir", "ensure_directory"]
