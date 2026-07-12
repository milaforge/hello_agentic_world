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

    )
