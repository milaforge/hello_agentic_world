from __future__ import annotations

from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from hello_agentic_world.dispatcher import ToolFunction, execute_tool_call, build_tools
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
FinishVerifier = Callable[
    [tuple[Observation, ...]],
    tuple[bool, str | None],
]


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
    store: ObservationStore | None = None,
    tools: dict[str, ToolFunction] | None = None,
    finish_verifier: FinishVerifier | None = None,
) -> AgentRun:
    """Run model decisions through host-controlled tools until completion."""

    store = store or ObservationStore()
    tools = tools or build_tools(workspace_root.resolve())
    finish_verifier = finish_verifier or _verify_finish_observation

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
                ok, error = finish_verifier(store.all())

                if ok:
                    return AgentRun(
                        completed=True,
                        observations=store.all(),
                        final_value=observation.result.value,
                    )

                return AgentRun(
                    completed=False,
                    observations=store.all(),
                    error=f"verification_failed:{error}",
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


def _verify_finish_observation(
    observations: tuple[Observation, ...],
) -> tuple[bool, str | None]:
    observation = observations[-1]
    value = observation.result.value

    if value is None:
        return False, "missing_finish_value"

    return verify_finish(
        observations,
        python_file_count=value["python_file_count"],
        total_size_bytes=value["total_size_bytes"],
        evidence=value["evidence"],
    )
