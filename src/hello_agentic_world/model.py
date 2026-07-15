from __future__ import annotations

import json
from typing import Any

from ollama import chat, ResponseError

from hello_agentic_world.agent import Action
from hello_agentic_world.debug import print_model_input, print_model_output
from hello_agentic_world.observations import Observation


class ModelError(Exception):
    pass


SYSTEM_PROMPT_TEMPLATE = """
You are a bounded filesystem investigation agent.

Goal:
Count all Python files under {workspace_name}/, excluding every .venv directory, and calculate their total size in bytes.

Rules:
- Use only the provided tools.
- Inspect directories one level at a time.
- Never access paths outside {workspace_name}/.
- Tool paths are relative to {workspace_name}/.
- Use "." to inspect the {workspace_name}/ root.
- Do not include the leading "{workspace_name}/" prefix in tool path arguments.
- Do not inspect .venv directories.
- Do not invent files, sizes or observations.
- Call finish only when every relevant directory and Python file has been inspected.
- Evidence must contain observation IDs supporting the answer.
"""


def build_tool_schemas(workspace_name: str) -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": (
                    "List the immediate entries of a directory. Paths are relative "
                    f'to {workspace_name}/; use "." for the root.'
                ),
                "parameters": {
                    "type": "object",
                    "required": ["path"],
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                f"A relative path under {workspace_name}/, without "
                                f'the leading "{workspace_name}/" prefix.'
                            ),
                        }
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_file_metadata",
                "description": "Return metadata including byte size for one file.",
                "parameters": {
                    "type": "object",
                    "required": ["path"],
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                f"A relative file path under {workspace_name}/, without "
                                f'the leading "{workspace_name}/" prefix.'
                            ),
                        }
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "finish",
                "description": "Submit the final answer with supporting evidence.",
                "parameters": {
                    "type": "object",
                    "required": [
                        "answer",
                        "python_file_count",
                        "total_size_bytes",
                        "evidence",
                    ],
                    "properties": {
                        "answer": {
                            "type": "string",
                        },
                        "python_file_count": {
                            "type": "string",
                        },
                        "total_size_bytes": {
                            "type": "string",
                        },
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
    ]


def ollama_decide(
    observations: tuple[Observation, ...],
    *,
    request: str,
    workspace_name: str,
    model: str = "qwen3:8b",
    debug: bool = False,
) -> Action:
    tool_schemas = build_tool_schemas(workspace_name)
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

    messages.extend(observation_messages(obs) for obs in observations)

    if debug:
        print_model_input(
            model=model,
            messages=messages[-1:] if observations else messages,
            tool_schemas=tool_schemas,
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

    if len(tool_calls) != 1:
        if debug:
            print_model_output({"tool_call_count": len(tool_calls), "action": None})
        return Action(name="invalid_model_response", arguments={})

    call = tool_calls[0].function

    action = Action(name=call.name, arguments=dict(call.arguments))

    if debug:
        print_model_output(
            {"action": {"name": action.name, "arguments": action.arguments}}
        )

    return action


##TODO make it more precise
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
