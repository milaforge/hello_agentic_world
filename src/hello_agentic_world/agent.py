from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from hello_agentic_world.dispatcher import execute_tool_call
from hello_agentic_world.observations import Observation, ObservationStore


@dataclass(frozen=True)
class Action:
    name: str
    arguments: dict[str, Any]


DecisionMaker = Callable[[tuple[Observation, ...]], Action]


@dataclass(frozen=True)
class AgentRun:
    completed: bool
    observations: tuple[Observation, ...]
    final_value: dict[str, Any] | None = None
    error: str | None = None


def run_agent(
    decide: DecisionMaker,
    *,
    max_steps: int = 15,
) -> AgentRun:
    """
    The Loop
    """
    store = ObservationStore()

    for _ in range(max_steps):
        action = decide(store.all())

        observation = execute_tool_call(
            store,
            action.name,
            action.arguments,
        )

        if action.name == "finish" and observation.result.ok:
            return AgentRun(
                completed=True,
                observations=store.all(),
                final_value=observation.result.value,
            )
    return AgentRun(
        completed=False, observations=store.all(), error="step_budget_exhausted"
    )
