from __future__ import annotations

import json
from types import SimpleNamespace

from hello_agentic_world.contracts import ToolCall, ToolResult
from hello_agentic_world.model import (
    build_model_messages,
    ollama_decide,
)
from hello_agentic_world.observations import ObservationStore
from hello_agentic_world.task_state import build_task_state


def _sample_observations():
    store = ObservationStore()

    store.record(
        ToolCall("list_directory", {"path": "."}),
        ToolResult(
            ok=True,
            value={
                "path": ".",
                "entries": [
                    {"path": "old.py", "kind": "file"},
                    {"path": "old.txt", "kind": "file"},
                    {"path": "src", "kind": "directory"},
                    {"path": ".venv", "kind": "directory"},
                ],
            },
        ),
    )
    store.record(
        ToolCall("get_file_metadata", {"path": "old.py"}),
        ToolResult(
            ok=True,
            value={"path": "old.py", "kind": "file", "size_bytes": 7},
        ),
    )
    store.record(
        ToolCall("list_directory", {"path": "src"}),
        ToolResult(
            ok=True,
            value={
                "path": "src",
                "entries": [{"path": "src/app.py", "kind": "file"}],
            },
        ),
    )

    return store.all()


def test_task_state_tracks_verified_work_without_full_transcript() -> None:
    state = build_task_state(_sample_observations()).as_payload()

    assert state["listed_directories"] == [".", "src"]
    assert state["ignored_directories"] == [".venv"]
    assert state["pending_directories"] == []
    assert state["pending_python_files"] == ["src/app.py"]
    assert state["measured_python_files"] == [
        {"path": "old.py", "size_bytes": 7, "observation_id": "obs-2"}
    ]
    assert state["python_file_count_so_far"] == 1
    assert state["total_size_bytes_so_far"] == 7
    assert state["evidence_so_far"] == ["obs-2"]


def test_model_messages_are_bounded_to_state_and_latest_observation() -> None:
    messages = build_model_messages(
        _sample_observations(),
        request="Count Python files.",
        workspace_name="workspace",
    )
    contents = "\n".join(message["content"] for message in messages)

    assert len(messages) == 4
    assert "Host task state" in messages[2]["content"]
    assert '"observation_id": "obs-3"' in messages[3]["content"]

    assert "src/app.py" in contents
    assert "old.py" in contents
    assert "old.txt" not in contents
    assert '"observation_id": "obs-1"' not in contents


def test_debug_model_input_matches_payload_sent_to_chat(capsys, monkeypatch) -> None:
    sent: dict[str, object] = {}

    def fake_chat(**kwargs):
        sent.update(kwargs)
        return SimpleNamespace(
            message=SimpleNamespace(
                tool_calls=[
                    SimpleNamespace(
                        function=SimpleNamespace(
                            name="finish",
                            arguments={
                                "answer": "done",
                                "python_file_count": 1,
                                "total_size_bytes": 7,
                                "evidence": ["obs-2"],
                            },
                        )
                    )
                ]
            )
        )

    monkeypatch.setattr("hello_agentic_world.model.chat", fake_chat)

    actions = ollama_decide(
        _sample_observations(),
        request="Count Python files.",
        workspace_name="workspace",
        debug=True,
    )

    captured = capsys.readouterr()
    debug_input_line = next(
        line
        for line in captured.err.splitlines()
        if line.startswith("DEBUG model_input ")
    )
    debug_payload = json.loads(debug_input_line.removeprefix("DEBUG model_input "))

    assert len(actions) == 1
    assert actions[0].name == "finish"
    assert debug_payload == {
        "model": sent["model"],
        "messages": sent["messages"],
        "tools": sent["tools"],
        "stream": sent["stream"],
    }


def test_model_adapter_preserves_multiple_tool_calls(monkeypatch) -> None:
    def fake_chat(**kwargs):
        return SimpleNamespace(
            message=SimpleNamespace(
                tool_calls=[
                    SimpleNamespace(
                        function=SimpleNamespace(
                            name="get_file_metadata",
                            arguments={"path": "main.py"},
                        )
                    ),
                    SimpleNamespace(
                        function=SimpleNamespace(
                            name="get_file_metadata",
                            arguments={"path": "src/app.py"},
                        )
                    ),
                ]
            )
        )

    monkeypatch.setattr("hello_agentic_world.model.chat", fake_chat)

    actions = ollama_decide(
        _sample_observations(),
        request="Count Python files.",
        workspace_name="workspace",
    )

    assert [action.name for action in actions] == [
        "get_file_metadata",
        "get_file_metadata",
    ]
    assert [action.arguments for action in actions] == [
        {"path": "main.py"},
        {"path": "src/app.py"},
    ]
