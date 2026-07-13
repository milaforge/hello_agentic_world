from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hello_agentic_world.contracts import (
    ToolCall,
    ToolResult,
    ToolError,
    Observation,
)


class ObservationStore:
    """Append-only trace of what the host accepted or rejected."""

    def __init__(self) -> None:
        self._observations: list[Observation] = []

    def record(
        self,
        call: ToolCall,
        result: ToolResult,
    ) -> Observation:
        step = len(self._observations) + 1

        observation = Observation(
            id=f"obs-{step}",
            step=step,
            call=call,
            result=result,
        )

        self._observations.append(observation)
        return observation

    def all(self) -> tuple[Observation, ...]:
        # Give callers a snapshot they cannot mutate in place.
        return tuple(self._observations)

    def get(self, observation_id: str) -> Observation | None:
        for observation in self._observations:
            if observation.id == observation_id:
                return observation
        return None
