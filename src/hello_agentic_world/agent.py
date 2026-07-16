from __future__ import annotations

from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from hello_agentic_world.dispatcher import execute_tool_call, build_tools
from hello_agentic_world.observations import Observation, ObservationStore
from hello_agentic_world.verification import verify_finish


@dataclass(frozen=True)
class Action:
    """The model's next requested host action."""

    name: str
    arguments: dict[str, Any]


ActionBatch = tuple[Action, ...]
Decision = Action | ActionBatch
DecisionMaker = Callable[[tuple[Observation, ...]], Decision]


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

    while len(store.all()) < max_steps:
        actions = _as_action_batch(decide(store.all()))

        for action in actions:
            if len(store.all()) >= max_steps:
                break

            observation = execute_tool_call(
                store,
                tools,
                action.name,
                action.arguments,
            )

            if action.name == "finish" and observation.result.ok:
                value = observation.result.value

                ok, error = verify_finish(
                    store.all(),
                    python_file_count=value["python_file_count"],
                    total_size_bytes=value["total_size_bytes"],
                    evidence=value["evidence"],
                )

                if ok:
                    return AgentRun(
                        completed=True,
                        observations=store.all(),
                        final_value=observation.result.value,
                    )
    return AgentRun(
        completed=False, observations=store.all(), error="step_budget_exhausted"
    )


def _as_action_batch(decision: Decision) -> ActionBatch:
    if isinstance(decision, Action):
        return (decision,)

    if decision:
        return decision

    return (Action(name="invalid_model_response", arguments={}),)
