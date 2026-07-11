from pathlib import Path

from hello_agentic_world.dispatcher import execute_tool_call, ObservationStore


def test_execute_known_tools(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": ".",
        },
    )

    assert observation.id == "obs-1"
    assert observation.result.ok is True

    assert observation.result.value["entries"][0] == {
        "path": "workspace/main.py",
        "kind": "file",
    }


def test_rejects_unknown_tool(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "delete_file",
        {
            "workspace_root": sample_workspace,
            "path": ".",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "unknown_tool"


def test_rejects_invalid_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "list_directory",
        {
            "path": ".",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_rejects_missing_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "list_directory",
        {},
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_rejects_extra_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": ".",
            "recursive": True,
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_converts_tool_error_to_result(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    observation = execute_tool_call(
        sample_store,
        "list_directory",
        {
            "workspace_root": sample_workspace,
            "path": "../secret",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "path_outside_workspace"


def test_rejects_invalid_argument_type(sample_store: ObservationStore) -> None:
    observation = execute_tool_call(
        sample_store,
        "get_file_metadata",
        {"path": 123},
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"
