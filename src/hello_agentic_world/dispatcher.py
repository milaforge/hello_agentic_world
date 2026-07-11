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

TOOLS: dict[str, ToolFunction] = {
    "list_directory": list_directory,
    "get_file_metadata": get_file_metadata,
    "finish": finish,
}


def execute_tool_call(
    store: ObservationStore,
    name: str,
    arguments: dict[str, Any],
) -> Observation:
    call = ToolCall(name=name, arguments=arguments)
    tool = TOOLS.get(call.name)

    if tool is None:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error="unknown_tool",
            ),
        )

    # Catch structural mistakes before execution
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
    except TypeError:
        return store.record(
            call,
            ToolResult(
                ok=False,
                error="invalid_argument_types",
            ),
        )

    result = ToolResult(ok=True, value=value)

    return store.record(call, result)
