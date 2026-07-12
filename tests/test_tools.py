from pathlib import Path

import pytest

from hello_agentic_world.tools import (
    ToolError,
    finish,
    get_file_metadata,
    list_directory,
)

def test_list_directory(sample_workspace: Path) -> None:
    result = list_directory(workspace_root=sample_workspace, path=".")

    assert result["path"] == "."
    assert result["entries"] == [
        {"path": "main.py", "kind": "file"},
        {"path": "notes.txt", "kind": "file"},
        {"path": "src", "kind": "directory"},
    ]


def test_get_file_metadata(sample_workspace: Path) -> None:
    result = get_file_metadata(workspace_root=sample_workspace, path="main.py")

    assert result["path"] == "main.py"
    assert result["kind"] == "file"
    assert result["size_bytes"] == len("print('hello')\n")


@pytest.mark.parametrize(
    "path",
    [
        "/etc/passwd",
        "../secret.txt",
        "workspace/../secret.txt",
    ],
)
def test_reject_paths_outside_workspace(sample_workspace: Path, path: str) -> None:
    with pytest.raises(ToolError):
        list_directory(sample_workspace, path)


def test_list_directory_rejects_files(sample_workspace: Path) -> None:
    with pytest.raises(ToolError, match="path_is_not_a_directory"):
        list_directory(sample_workspace, "main.py")


def test_get_metadata_rejects_directory(sample_workspace: Path) -> None:
    with pytest.raises(ToolError, match="path_is_not_a_file"):
        get_file_metadata(sample_workspace, "src")


def test_finish_returns_structured_result() -> None:
    result = finish(
        answer="Two Python files.",
        python_file_count=2,
        total_size_bytes=21,
        evidence=["obs-0001", "obs-0002"],
    )

    assert result["python_file_count"] == 2
    assert result["total_size_bytes"] == 21


def test_finish_requires_evidence() -> None:
    with pytest.raises(ToolError, match="evidence_is_required"):
        finish(
            answer="Two Python files.",
            python_file_count=2,
            total_size_bytes=21,
            evidence=[],
        )
