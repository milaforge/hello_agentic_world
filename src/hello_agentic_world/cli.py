"""Minimal CLI kept small while the agent loop evolves."""

from __future__ import annotations

from functools import partial
import argparse
from collections.abc import Sequence
from pathlib import Path

from .model import ollama_decide
from .model import ModelError
from .agent import run_agent


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="hello-agent",
        description="Run the Hello Agentic World learning project.",
    )

    parser.add_argument(
        "--workspace",
        required=True,
        help="Workspace directory the agent may inspect.",
    )
    parser.add_argument("request", help="The request the agent should handle")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print model input and output payloads to stderr.",
    )
    parser.add_argument(
        "--model",
        default="qwen3:8b",
        help="Ollama model to use for decisions.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line application."""

    parser = build_parser()
    args = parser.parse_args(argv)

    print(f"Request: {args.request}", flush=True)
    workspace_root = Path(args.workspace)
    workspace_name = workspace_root.name

    decide = partial(
        ollama_decide,
        request=args.request,
        workspace_name=workspace_name,
        model=args.model,
        debug=args.debug,
    )

    try:
        result = run_agent(decide, workspace_root=workspace_root, max_steps=15)
    except ModelError as exc:
        print(str(exc))
        return 1

    print(result.final_value if result.completed else result.error)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
