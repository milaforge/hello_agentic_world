from __future__ import annotations

import subprocess
import sys

from hello_agentic_world.cli import (
    build_parser,
    main,
)


def test_main_prints_requests(capsys) -> None:
    exit_code = main(["How many Python files exist?"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Request: How many Python files exist?\n"


def test_module_rejects_missing_requests() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hello_agentic_world.cli",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "usage:" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()
