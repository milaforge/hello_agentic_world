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


def build_tools(workspace_root: Path) -> dict[str, ToolFunction]:
    return {
        "list_directory": partial(list_directory, workspace_root),
        "get_file_metadata": partial(get_file_metadata, workspace_root),
        "finish": finish,
    }


def execute_tool_call(
    store: ObservationStore,
    tools: dict[str, ToolFunction],
    name: str,
    arguments: dict[str, Any],
) -> Observation:
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

    value = None

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
