"""Minimal CLI kept small while the agent loop evolves."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="hello-agent",
        description="Run the Hello Agentic World learning project.",
    )

    parser.add_argument("request", help="The request the agent should handle")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line application."""

    parser = build_parser()
    args = parser.parse_args(argv)

    print(f"Request: {args.request}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
