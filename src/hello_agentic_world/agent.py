from __future__ import annotations

from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from hello_agentic_world.dispatcher import execute_tool_call, build_tools
from hello_agentic_world.observations import Observation, ObservationStore


@dataclass(frozen=True)
class Action:
    """The model's next requested host action."""

    name: str
    arguments: dict[str, Any]


DecisionMaker = Callable[[tuple[Observation, ...]], Action]


@dataclass(frozen=True)
class AgentRun:
    """Complete trace and terminal state for one bounded loop."""

    completed: bool
    observations: tuple[Observation, ...]
    final_value: dict[str, Any] | None = None
    error: str | None = None


def run_agent(
    decide: DecisionMaker,
    *,
    workspace_root: Path = Path("workspace"),
    max_steps: int = 15,
) -> AgentRun:
    """Run model decisions through host-controlled tools until completion."""

    store = ObservationStore()
    tools = build_tools(workspace_root.resolve())

    for _ in range(max_steps):
        action = decide(store.all())

        observation = execute_tool_call(
            store,
            tools,
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
