from __future__ import annotations

import json
import sys
from typing import Any


def print_model_input(
    *,
    model: str,
    messages: list[dict[str, str]],
    tool_schemas: list[dict[str, Any]],
    stream: bool,
) -> None:
    print(
        "DEBUG model_input "
        + json.dumps(
            {
                "model": model,
                "messages": messages,
                "tools": tool_schemas,
                "stream": stream,
            },
            sort_keys=True,
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )


def print_model_output(payload: dict[str, Any]) -> None:
    print(
        "DEBUG model_output "
        + json.dumps(payload, sort_keys=True, ensure_ascii=False),
        file=sys.stderr,
    )
