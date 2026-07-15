from pathlib import Path

from hello_agentic_world.dispatcher import (
    execute_tool_call,
    ObservationStore,
    build_tools,
)


def test_execute_known_tools(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {
            "path": ".",
        },
    )

    assert observation.id == "obs-1"
    assert observation.result.ok is True

    assert observation.result.value["entries"][0] == {
        "path": "main.py",
        "kind": "file",
    }


def test_execute_rejects_workspace_prefixed_path(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {
            "path": "workspace/",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "path_does_not_exist"


def test_rejects_unknown_tool(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "delete_file",
        {
            "path": ".",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "unknown_tool"


def test_rejects_invalid_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {
            "invalid": 123,
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_rejects_missing_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {},
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_rejects_extra_arguments(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {
            "path": ".",
            "recursive": True,
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_arguments"


def test_converts_tool_error_to_result(
    sample_workspace: Path, sample_store: ObservationStore
) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "list_directory",
        {
            "path": "../secret",
        },
    )

    assert observation.result.ok is False
    assert observation.result.error == "path_outside_workspace"


def test_rejects_invalid_argument_type(sample_workspace: Path, sample_store: ObservationStore) -> None:
    tools = build_tools(sample_workspace)

    observation = execute_tool_call(
        sample_store,
        tools,
        "get_file_metadata",
        {"path": 123},
    )

    assert observation.result.ok is False
    assert observation.result.error == "invalid_argument_types"


def test_runtime_type_errors_are_failed_observations(
    sample_store: ObservationStore,
) -> None:
    def broken_tool() -> dict[str, object]:
        raise TypeError("boom")

    observation = execute_tool_call(
        sample_store,
        {"broken_tool": broken_tool},
        "broken_tool",
        {},
    )

    assert observation.result.ok is False
    assert observation.result.value is None
    assert observation.result.error == "TypeError: boom"
