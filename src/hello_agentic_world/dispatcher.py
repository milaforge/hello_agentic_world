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

from hello_agentic_world.tools import (
    ToolError,
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
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    tool = TOOLS.get(name)

    if tool is None:
        return {
            "ok": False,
            "error": "unknown_tool",
        }

    # Catch structural mistakes before execution
    try:
        inspect.signature(tool).bind(**arguments)
    except TypeError:
        return {
            "ok": False,
            "error": "invalid_arguments",
        }

    try:
        value = tool(**arguments)
    except ToolError as exc:
        return {
            "ok": False,
            "error": str(exc),
        }
    except TypeError:
        return {
            "ok": False,
            "error": "invalid_argument_types",
        }

    return {"ok": True, "value": value}
