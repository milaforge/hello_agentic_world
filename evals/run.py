from __future__ import annotations

import argparse
import json
import shutil
import sys
import threading
import time
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory

from hello_agentic_world.agent import run_agent
from hello_agentic_world.model import ollama_decide


@dataclass(frozen=True)
class Scenario:
    name: str
    files: dict[str, str]
    expected_count: int
    expected_size: int


SCENARIOS = [
    Scenario(
        name="basic",
        files={
            "main.py": "print('hello')\n",
            "src/app.py": "x = 1\n",
            "notes.txt": "ignored",
        },
        expected_count=2,
        expected_size=len("print('hello')\n") + len("x = 1\n"),
    ),
    Scenario(
        name="empty",
        files={},
        expected_count=0,
        expected_size=0,
    ),
    Scenario(
        name="ignore_venv",
        files={
            "main.py": "x = 1\n",
            ".venv/hidden.py": "must be ignored",
        },
        expected_count=1,
        expected_size=len("x = 1\n"),
    ),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run model evaluation scenarios.")
    parser.add_argument(
        "--model",
        default="qwen3:8b",
        help="Ollama model to evaluate.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print concise progress while scenarios run.",
    )
    return parser


def prepare_workspace(root: Path, files: dict[str, str]) -> None:

    if root.exists():
        shutil.rmtree(root)

    root.mkdir(parents=True)

    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def format_elapsed(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"


def print_elapsed_timer(
    *,
    started_at: float,
    stop: threading.Event,
    stream,
) -> None:
    while not stop.is_set():
        stream.write(f"\r{format_elapsed(time.monotonic() - started_at)}")
        stream.flush()
        stop.wait(1)


def evaluate_scenario(
    scenario: Scenario,
    *,
    workspace: Path,
    model: str,
) -> dict:
    with TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        prepare_workspace(workspace, scenario.files)

        decide = partial(
            ollama_decide,
            request="Count Python files and their total size.",
            workspace_name=workspace.name,
            model=model,
        )

        run = run_agent(decide, workspace_root=workspace, max_steps=15)

        result = run.final_value or {}

        count_correct = result.get("python_file_count") == scenario.expected_count

        size_correct = result.get("total_size_bytes") == scenario.expected_size

        return {
            "scenario": scenario.name,
            "passed": run.completed and count_correct and size_correct,
            "completed": run.completed,
            "expected_count": scenario.expected_count,
            "actual_count": result.get("python_file_count"),
            "expected_size": scenario.expected_size,
            "actual_size": result.get("total_size_bytes"),
            "steps": len(run.observations),
            "error": run.error,
        }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path("workspace")

    results = []
    total = len(SCENARIOS)

    for index, scenario in enumerate(SCENARIOS, start=1):
        remaining = total - index
        timer_stop: threading.Event | None = None
        timer_thread: threading.Thread | None = None
        started_at = time.monotonic()

        if args.verbose:
            suffix = "scenario" if remaining == 1 else "scenarios"
            print(f"[{index}/{total}] Evaluating {scenario.name} ({remaining} {suffix} left)")
            timer_stop = threading.Event()
            timer_thread = threading.Thread(
                target=print_elapsed_timer,
                kwargs={
                    "started_at": started_at,
                    "stop": timer_stop,
                    "stream": sys.stdout,
                },
                daemon=True,
            )
            timer_thread.start()

        result = evaluate_scenario(
            scenario,
            workspace=workspace,
            model=args.model,
        )
        results.append(result)

        if args.verbose:
            assert timer_stop is not None
            assert timer_thread is not None
            timer_stop.set()
            timer_thread.join()
            elapsed = format_elapsed(time.monotonic() - started_at)
            print(f"\r{elapsed}")

    print(json.dumps(results, indent=2))

    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
