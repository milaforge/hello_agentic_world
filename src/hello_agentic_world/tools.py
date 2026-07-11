from __future__ import annotations

from pathlib import Path
from typing import Any

from .contracts import ToolError

WORKSPACE_ROOT = Path("workspace").resolve()


def resolve_workspace_path(path: str) -> Path:
    requested = Path(path)

    if requested.is_absolute():
        raise ToolError("absolute_paths_are_not_allowed")

    resolved = requested.resolve()

    try:
        resolved.relative_to(WORKSPACE_ROOT)
    except Exception as exc:
        raise ToolError("path_outside_workspace") from exc

    return resolved


def display_path(relative_path: Path) -> str:
    return (
        "workspace"
        if relative_path == Path(".")
        else str(Path("workspace") / relative_path)
    )


def list_directory(workspace_root: Path, path: str) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    resolved = (workspace_root / path).resolve()

    try:
        relative_path = resolved.relative_to(workspace_root)
    except ValueError as exc:
        raise ToolError("path_outside_workspace") from exc

    if not resolved.exists():
        raise ToolError("path_does_not_exist")

    if not resolved.is_dir():
        raise ToolError("path_is_not_a_directory")

    entries = []

    for entry in sorted(resolved.iterdir(), key=lambda item: item.name):
        relative_entry = entry.relative_to(workspace_root)

        entries.append(
            {
                "path": str(Path("workspace") / relative_entry),
                "kind": "directory" if entry.is_dir() else "file",
            }
        )

    return {
        "path": display_path(relative_path),
        "entries": entries,
    }


def get_file_metadata(workspace_root: Path, path: str) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    resolved = (workspace_root / path).resolve()

    # validate boundary
    try:
        relative_path = resolved.relative_to(workspace_root)
    except ValueError as exc:
        raise ToolError("path_outside_workspace") from exc

    if not resolved.exists():
        raise ToolError("path_does_not_exist")

    if not resolved.is_file():
        raise ToolError("path_is_not_a_file")

    return {
        "path": str(Path("workspace") / relative_path),
        "kind": "file",
        "size_bytes": resolved.stat().st_size,
    }


def finish(
    answer: str,
    python_file_count: int,
    total_size_bytes: int,
    evidence: list[str],
) -> dict[str, Any]:
    if python_file_count < 0:
        raise ToolError("invalid_file_count")

    if total_size_bytes < 0:
        raise ToolError("invalid_total_size")

    if not evidence:
        raise ToolError("evidence_is_required")

    return {
        "answer": answer,
        "python_file_count": python_file_count,
        "total_size_bytes": total_size_bytes,
        "evidence": evidence,
    }
