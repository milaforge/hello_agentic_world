from __future__ import annotations

from pathlib import Path

from .contracts import (
    DirectoryListingPayload,
    FileMetadataPayload,
    FinishPayload,
    ToolError,
)


def resolve_workspace_path(workspace_root: Path, path: str) -> Path:
    """Resolve user-supplied paths without escaping the workspace."""

    if not isinstance(path, str):
        raise ToolError("invalid_argument_types")

    workspace_root = workspace_root.resolve()
    requested = Path(path)

    if requested.is_absolute():
        raise ToolError("absolute_paths_are_not_allowed")

    resolved = (workspace_root / requested).resolve()

    try:
        resolved.relative_to(workspace_root)
    except ValueError as exc:
        raise ToolError("path_outside_workspace") from exc

    if not resolved.exists():
        raise ToolError("path_does_not_exist")

    return resolved


def display_path(workspace_root: Path, path: Path) -> str:
    """Return stable POSIX-style paths for observations and tests."""

    relative = path.relative_to(workspace_root)

    if relative == Path("."):
        return "."

    return relative.as_posix()


def list_directory(workspace_root: Path, path: str) -> DirectoryListingPayload:
    """Describe immediate children without exposing host-only paths."""

    resolved = resolve_workspace_path(workspace_root, path)

    if not resolved.is_dir():
        raise ToolError("path_is_not_a_directory")

    entries = [
        {
            "path": display_path(workspace_root, entry),
            "kind": "directory" if entry.is_dir() else "file",
        }
        for entry in sorted(resolved.iterdir(), key=lambda item: item.name)
    ]

    return {
        "path": display_path(workspace_root, resolved),
        "entries": entries,
    }


def get_file_metadata(workspace_root: Path, path: str) -> FileMetadataPayload:
    """Return the small metadata set needed by the learning exercise."""

    workspace_root = workspace_root.resolve()
    resolved = resolve_workspace_path(workspace_root, path)

    if not resolved.is_file():
        raise ToolError("path_is_not_a_file")

    return {
        "path": display_path(workspace_root, resolved),
        "kind": "file",
        "size_bytes": resolved.stat().st_size,
    }


def finish(
    answer: str,
    python_file_count: int,
    total_size_bytes: int,
    evidence: list[str],
) -> FinishPayload:
    """Accept the agent's final answer after basic sanity checks."""

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
