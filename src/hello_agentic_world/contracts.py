from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict


class DirectoryEntryPayload(TypedDict):
    path: str
    kind: Literal["directory", "file"]


class DirectoryListingPayload(TypedDict):
    path: str
    entries: list[DirectoryEntryPayload]


class FileMetadataPayload(TypedDict):
    path: str
    kind: Literal["file"]
    size_bytes: int


class FinishPayload(TypedDict):
    answer: str
    python_file_count: int
    total_size_bytes: int
    evidence: list[str]


class PythonFileMeasurement(TypedDict):
    size_bytes: int
    observation_id: str


class MeasuredPythonFilePayload(PythonFileMeasurement):
    path: str


class TaskStatePayload(TypedDict):
    listed_directories: list[str]
    pending_directories: list[str]
    ignored_directories: list[str]
    pending_python_files: list[str]
    measured_python_files: list[MeasuredPythonFilePayload]
    python_file_count_so_far: int
    total_size_bytes_so_far: int
    evidence_so_far: list[str]
    failed_observations: list[dict[str, Any]]


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
    call: ToolCall
    result: ToolResult


class ToolError(Exception):
    pass
