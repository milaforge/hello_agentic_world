"""Deterministic decision makers used by tests and early stages."""

from __future__ import annotations

from hello_agentic_world.agent import Action
from hello_agentic_world.observations import Observation
from hello_agentic_world.task_state import build_task_state


def simple_script(
    observations: tuple[Observation, ...],
) -> Action:
    """Finish after proving one tool call can round-trip."""

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
    """Exercise the agent's step budget failure path."""

    return Action(name="list_directory", arguments={"path": "."})


def unsafe_script(
    observations: tuple[Observation, ...],
) -> Action:
    """Exercise rejection of tools outside the allowlist."""

    return Action(
        name="delete_file",
        arguments={"path": "a.txt"},
    )


def filesystem_script(
    observations: tuple[Observation, ...],
) -> Action:
    """Explore the workspace, measure Python files, then finish with evidence."""

    state = build_task_state(observations)

    if state.pending_directories:
        return Action(
            name="list_directory",
            arguments={"path": sorted(state.pending_directories)[0]},
        )

    if state.pending_python_files:
        return Action(
            name="get_file_metadata",
            arguments={"path": sorted(state.pending_python_files)[0]},
        )

    return Action(
        name="finish",
        arguments={
            "answer": (
                "Found "
                f"{state.python_file_count} Python files with a total size of "
                f"{state.total_size_bytes} bytes."
            ),
            "python_file_count": state.python_file_count,
            "total_size_bytes": state.total_size_bytes,
            "evidence": state.evidence,
        },
    )
