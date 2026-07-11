from pathlib import Path

from hello_agentic_world.dispatcher import execute_tool_call


def test_execute_known_tools(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": ".",
        },
    )

    assert result["ok"] is True
    assert result["value"]["entries"][0] == {
        "path": "workspace/main.py",
        "kind": "file",
    }


def test_rejects_unknown_tool(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "delete_file",
        {
            "workspace_root": sample_workspace,
            "path": ".",
        },
    )

    assert result["ok"] is False
    assert result["error"] == "unknown_tool"


def test_rejects_invalid_arguments(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "list_directory",
        {
            "path": ".",
        },
    )

    assert result["ok"] is False
    assert result["error"] == "invalid_arguments"


def test_rejects_missing_arguments(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "list_directory",
        {},
    )

    assert result["ok"] is False
    assert result["error"] == "invalid_arguments"


def test_rejects_extra_arguments(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": ".",
            "recursive": True,
        },
    )

    assert result["ok"] is False
    assert result["error"] == "invalid_arguments"


def test_converts_tool_error_to_result(sample_workspace: Path) -> None:
    result = execute_tool_call(
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": "../secret",
        },
    )

    assert result["ok"] is False
    assert result["error"] == "path_outside_workspace"


def test_rejects_invalid_argument_type() -> None:
    result = execute_tool_call(
        "get_file_metadata",
        {"path": 123},
    )

    assert result["ok"] is False
    assert result["error"] == "invalid_arguments"
