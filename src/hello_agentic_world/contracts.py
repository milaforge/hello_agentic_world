from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    """An untrusted action proposed by the model."""

    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ToolResult:
    """The result returned after host-controlled execution."""

    ok: bool
    value: dict[str, Any] | None = None
    error: str | None = None


@dataclass(frozen=True)
class Observation:
    """An immutable record of an executed or rejected action."""

    id: str
    step: int
    tool_call: ToolCall
    result: ToolResult


class ToolError(Exception):
    pass
