from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ollama import chat, ResponseError

from hello_agentic_world.agent import Action, ActionBatch
from hello_agentic_world.debug import print_model_input, print_model_output
from hello_agentic_world.dispatcher import build_tool_schemas
from hello_agentic_world.observations import Observation
from hello_agentic_world.task_state import task_state_message


class ModelError(Exception):
    pass


SYSTEM_PROMPT_TEMPLATE = """
You are a bounded filesystem investigation agent.

Goal:
Count all Python files under {workspace_name}/, excluding every .venv directory, and calculate their total size in bytes.

Rules:
- Use only the provided tools.
- You may call multiple independent tools in one turn when their inputs do not
  depend on each other's observations.
- The host records batched tool observations in the same order you request them.
- Inspect directories one level at a time.
- Never access paths outside {workspace_name}/.
- Tool paths are relative to {workspace_name}/.
- Use "." to inspect the {workspace_name}/ root.
- Do not include the leading "{workspace_name}/" prefix in tool path arguments.
- Do not inspect .venv directories.
- Do not invent files, sizes or observations.
- Treat the host task state as verified fact.
- Use the latest host observation only to update your next action.
- Call finish only when every relevant directory and Python file has been inspected.
- Evidence must contain observation IDs supporting the answer.
"""


def ollama_decide(
    observations: tuple[Observation, ...],
    *,
    request: str,
    workspace_name: str,
    model: str = "qwen3:8b",
    debug: bool = False,
) -> Action | ActionBatch:
    tool_schemas = build_tool_schemas(Path(workspace_name), workspace_name)
    messages = build_model_messages(
        observations,
        request=request,
        workspace_name=workspace_name,
    )

    if debug:
        print_model_input(
            model=model,
            messages=messages,
            tool_schemas=tool_schemas,
            stream=False,
        )

    try:
        response = chat(
            model=model,
            messages=messages,
            tools=tool_schemas,
            stream=False,
        )
    except ResponseError as exc:
        raise ModelError(
            f"Ollama request failed with status {exc.status_code}"
        ) from exc

    tool_calls = response.message.tool_calls or []

    if not tool_calls:
        if debug:
            print_model_output({"tool_call_count": len(tool_calls), "action": None})
        return Action(name="invalid_model_response", arguments={})

    actions = tuple(
        Action(
            name=tool_call.function.name,
            arguments=dict(tool_call.function.arguments),
        )
        for tool_call in tool_calls
    )

    if debug:
        print_model_output(
            {
                "actions": [
                    {"name": action.name, "arguments": action.arguments}
                    for action in actions
                ]
            }
        )

    return actions


def build_model_messages(
    observations: tuple[Observation, ...],
    *,
    request: str,
    workspace_name: str,
) -> list[dict[str, str]]:
    """Build the bounded model payload from full host-owned observations."""

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT_TEMPLATE.format(workspace_name=workspace_name),
        },
        {
            "role": "user",
            "content": request,
        },
    ]

    if not observations:
        return messages

    messages.append(task_state_message(observations))
    messages.append(observation_messages(observations[-1]))
    return messages


def observation_messages(observation: Observation) -> dict[str, str]:
    payload = {
        "observation_id": observation.id,
        "tool": observation.call.name,
        "ok": observation.result.ok,
        "value": observation.result.value,
        "error": observation.result.error,
    }

    return {
        "role": "user",
        "content": ("Host observation:\n" + json.dumps(payload, sort_keys=True)),
    }
