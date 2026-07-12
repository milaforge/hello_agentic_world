"""
Some hardcoded decision making system to help prove the loop works.
"""

from __future__ import annotations

from pathlib import PurePosixPath

from hello_agentic_world.agent import Action
from hello_agentic_world.observations import Observation


def simple_script(
    observations: tuple[Observation, ...],
) -> Action:
    step = len(observations)

    if step == 0:
        return Action(
            "list_directory",
            arguments={"path": "."},
        )

    return Action(
        name="finish",
        arguments={
            "answer": "workspace inspected.",
            "python_file_count": 0,
            "total_size_bytes": 0,
            "evidence": ["obs-1"],
        },
    )


def never_finish(
    observations: tuple[Observation, ...],
) -> Action:
    return Action(name="list_directory", arguments={"path": "."})


def unsafe_script(
    observations: tuple[Observation, ...],
) -> Action:
    return Action(
        name="delete_file",
        arguments={"path": "a.txt"},
    )


def filesystem_script(
    observations: tuple[Observation, ...],
) -> Action:
    listed_directories: set[str] = set()
    measured_files: set[str] = set()
    discovered_directories: list[str] = ["."]
    discovered_python_files: list[str] = []

    for observation in observations:
        if not observation.result.ok or observation.result.value is None:
            continue

        if observation.call.name == "list_directory":
            listed_path = observation.result.value["path"]
            listed_directories.add(listed_path)

            for entry in observation.result.value["entries"]:
                path = entry["path"]

                if entry["kind"] == "directory":
                    if PurePosixPath(path).name != ".venv":
                        discovered_directories.append(path)

                elif path.endswith(".py"):
                    discovered_python_files.append(path)

        elif observation.call.name == "get_file_metadata":
            measured_files.add(observation.result.value["path"])

    for directory in discovered_directories:
        if directory not in listed_directories:
            return Action(
                name="list_directory",
                arguments={"path": directory},
            )

    for path in discovered_python_files:
        if path not in measured_files:
            return Action(
                name="get_file_metadata",
                arguments={"path": path},
            )

    metadata_observations = [
        observation
        for observation in observations
        if observation.call.name == "get_file_metadata"
        and observation.result.ok
        and observation.result.value is not None
    ]

    count = len(metadata_observations)
    total_size = sum(
        observation.result.value["size_bytes"] for observation in metadata_observations
    )

    evidence = [
        observation.id
        for observation in observations
        if observation.result.ok
        and observation.call.name
        in {
            "list_directory",
            "get_file_metadata",
        }
    ]

    return Action(
        name="finish",
        arguments={
            "answer": (
                f"Found {count} Python files with a total size of {total_size} bytes."
            ),
            "python_file_count": count,
            "total_size_bytes": total_size,
            "evidence": evidence,
        },
    )
