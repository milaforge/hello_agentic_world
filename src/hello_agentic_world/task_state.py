from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any

from hello_agentic_world.observations import Observation


@dataclass
class TaskState:
    """Compact, host-derived state for the filesystem counting task."""

    listed_directories: set[str] = field(default_factory=set)
    pending_directories: set[str] = field(default_factory=lambda: {"."})
    ignored_directories: set[str] = field(default_factory=set)
    pending_python_files: set[str] = field(default_factory=set)
    measured_python_files: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed_observations: list[dict[str, Any]] = field(default_factory=list)

    @property
    def python_file_count(self) -> int:
        return len(self.measured_python_files)

    @property
    def total_size_bytes(self) -> int:
        return sum(
            metadata["size_bytes"] for metadata in self.measured_python_files.values()
        )

    @property
    def evidence(self) -> list[str]:
        return [
            metadata["observation_id"]
            for _, metadata in sorted(self.measured_python_files.items())
        ]

    def as_payload(self) -> dict[str, Any]:
        return {
            "listed_directories": sorted(self.listed_directories),
            "pending_directories": sorted(self.pending_directories),
            "ignored_directories": sorted(self.ignored_directories),
            "pending_python_files": sorted(self.pending_python_files),
            "measured_python_files": [
                {
                    "path": path,
                    "size_bytes": metadata["size_bytes"],
                    "observation_id": metadata["observation_id"],
                }
                for path, metadata in sorted(self.measured_python_files.items())
            ],
            "python_file_count_so_far": self.python_file_count,
            "total_size_bytes_so_far": self.total_size_bytes,
            "evidence_so_far": self.evidence,
            "failed_observations": self.failed_observations,
        }


def task_state_message(observations: tuple[Observation, ...]) -> dict[str, str]:
    payload = build_task_state(observations).as_payload()
    return {
        "role": "user",
        "content": (
            "Host task state, derived from all verified observations:\n"
            + json.dumps(payload, sort_keys=True)
        ),
    }


def build_task_state(observations: tuple[Observation, ...]) -> TaskState:
    state = TaskState()

    for observation in observations:
        if not observation.result.ok:
            _apply_failed_observation(state, observation)
        elif observation.result.value is not None:
            _apply_successful_observation(state, observation)

    return state


def _apply_failed_observation(state: TaskState, observation: Observation) -> None:
    state.failed_observations.append(
        {
            "observation_id": observation.id,
            "tool": observation.call.name,
            "arguments": observation.call.arguments,
            "error": observation.result.error,
        }
    )


def _apply_successful_observation(state: TaskState, observation: Observation) -> None:
    if observation.call.name == "list_directory":
        _apply_directory_observation(state, observation)
    elif observation.call.name == "get_file_metadata":
        _apply_metadata_observation(state, observation)


def _apply_directory_observation(state: TaskState, observation: Observation) -> None:
    value = observation.result.value
    if value is None:
        return

    listed_path = value["path"]
    state.listed_directories.add(listed_path)
    state.pending_directories.discard(listed_path)

    for entry in value["entries"]:
        path = entry["path"]

        if entry["kind"] == "directory":
            _track_directory(state, path)
        elif path.endswith(".py") and path not in state.measured_python_files:
            state.pending_python_files.add(path)


def _track_directory(state: TaskState, path: str) -> None:
    if PurePosixPath(path).name == ".venv":
        state.ignored_directories.add(path)
    elif path not in state.listed_directories:
        state.pending_directories.add(path)


def _apply_metadata_observation(state: TaskState, observation: Observation) -> None:
    value = observation.result.value
    if value is None:
        return

    path = value["path"]
    if not path.endswith(".py"):
        return

    state.pending_python_files.discard(path)
    state.measured_python_files[path] = {
        "size_bytes": value["size_bytes"],
        "observation_id": observation.id,
    }
