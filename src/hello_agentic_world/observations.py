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
        # to make it immutable and prevent:
        # store.all().append(...)
        return tuple(self._observations)

    def get(self, observation_id: str) -> Observation | None:
        for observation in self._observations:
            if observation.id == observation_id:
                return observation
        return None
