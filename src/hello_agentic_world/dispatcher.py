"""
The AI Model should never call Python functions directly.

Instead, it proposes a tool call, for example:

{
    "name": "list_directory",
    "arguments": {
        "path": "workspace",
    }
}

The host is responsible for:

1. Verifying the requested tool exists.
2. Validating the supplied arguments.
3. Executing the tool.
4. Returning a structured result instead of crashing.

---

model proposal
    ↓
dispatcher
    ↓
validated tool execution
    ↓
structured result

"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from collections.abc import Callable
from typing import Any

from hello_agentic_world.observations import (
    Observation,
    ObservationStore,
    ToolCall,
    ToolResult,
    ToolError,
)
from hello_agentic_world.tools import (
    finish,
    get_file_metadata,
    list_directory,
)

ToolFunction = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    """Host-side callable and model-facing schema for one allowed tool."""

    name: str
    function: ToolFunction
    schema: dict[str, Any]


def build_tools(workspace_root: Path) -> dict[str, ToolFunction]:
    """Expose only the tools this run is allowed to use."""

    return {spec.name: spec.function for spec in build_tool_specs(workspace_root, ".")}


def build_tool_schemas(workspace_root: Path, workspace_name: str) -> list[dict[str, Any]]:
    """Return model-facing schemas for the same tools exposed to the dispatcher."""

    return [
        spec.schema for spec in build_tool_specs(workspace_root, workspace_name)
    ]


def build_tool_specs(workspace_root: Path, workspace_name: str) -> tuple[ToolSpec, ...]:
    """Expose allowed tools with one source for callables and schemas."""

    return (
        ToolSpec(
            name="list_directory",
            function=partial(list_directory, workspace_root),
            schema={
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
        ),
        ToolSpec(
            name="get_file_metadata",
            function=partial(get_file_metadata, workspace_root),
            schema={
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
        ),
        ToolSpec(
            name="finish",
            function=finish,
            schema={
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
                                "type": "integer",
                            },
                            "total_size_bytes": {
                                "type": "integer",
                            },
                            "evidence": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
        ),
    )


def build_tool_schema_names(
    workspace_root: Path,
    workspace_name: str,
) -> list[str]:
    """Return schema names for tests that assert registry/schema alignment."""

    return [
        spec.schema["function"]["name"]
        for spec in build_tool_specs(workspace_root, workspace_name)
    ]


def execute_tool_call(
    store: ObservationStore,
    tools: dict[str, ToolFunction],
    name: str,
    arguments: dict[str, Any],
) -> Observation:
    """Validate, execute, and record one untrusted tool request."""

    call = ToolCall(name=name, arguments=arguments)
    tool = tools.get(call.name)

    if tool is None:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error="unknown_tool",
            ),
        )

    # Reject malformed calls before any tool code runs.
    try:
        inspect.signature(tool).bind(**call.arguments)
    except TypeError:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error="invalid_arguments",
            ),
        )

    try:
        value = tool(**call.arguments)
    except ToolError as exc:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error=str(exc),
            ),
        )
    except (TypeError, AttributeError) as exc:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error=f"{type(exc).__name__}: {exc}",
            ),
        )

    result = ToolResult(ok=True, value=value)

    return store.record(call, result)
