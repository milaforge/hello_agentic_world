from __future__ import annotations

import subprocess
import sys

from hello_agentic_world.agent import AgentRun
from hello_agentic_world.cli import main
from hello_agentic_world.model import ModelError


def test_main_prints_request_and_result(capsys, monkeypatch) -> None:
    def fake_run_agent(decide, *, workspace_root, max_steps):
        assert workspace_root.as_posix() == "workspace"
        return AgentRun(completed=True, observations=(), final_value={"answer": "3"})

    monkeypatch.setattr("hello_agentic_world.cli.run_agent", fake_run_agent)

    exit_code = main(["--workspace", "workspace", "How many Python files exist?"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Request: How many Python files exist?\n{'answer': '3'}\n"
    assert captured.err == ""


def test_debug_flag_is_passed_to_model_adapter(capsys, monkeypatch) -> None:
    def fake_ollama_decide(observations, *, request, workspace_name, model, debug):
        raise AssertionError("run_agent should not call decide in this test")

    def fake_run_agent(decide, *, workspace_root, max_steps):
        assert workspace_root.as_posix() == "workspace"
        assert decide.keywords["debug"] is True
        assert decide.keywords["model"] == "qwen3:8b"
        assert decide.keywords["request"] == "How many Python files exist?"
        assert decide.keywords["workspace_name"] == "workspace"
        return AgentRun(completed=False, observations=(), error="step_budget_exhausted")

    monkeypatch.setattr("hello_agentic_world.cli.ollama_decide", fake_ollama_decide)
    monkeypatch.setattr("hello_agentic_world.cli.run_agent", fake_run_agent)

    exit_code = main(
        ["--workspace", "workspace", "--debug", "How many Python files exist?"]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.startswith(
        "Request: How many Python files exist?\n"
        "DEBUG run_saved runs/"
    )
    assert captured.out.endswith("step_budget_exhausted\n")
    assert captured.err == ""


def test_model_flag_is_passed_to_model_adapter_and_trace(
    capsys, monkeypatch
) -> None:
    def fake_ollama_decide(observations, *, request, workspace_name, model, debug):
        raise AssertionError("run_agent should not call decide in this test")

    def fake_run_agent(decide, *, workspace_root, max_steps):
        assert decide.keywords["model"] == "llama3.2:latest"
        return AgentRun(completed=True, observations=(), final_value={"answer": "3"})

    def fake_save_run(result, *, request, model, output_dir):
        assert request == "How many Python files exist?"
        assert model == "llama3.2:latest"
        return output_dir / "fake-run.json"

    monkeypatch.setattr("hello_agentic_world.cli.ollama_decide", fake_ollama_decide)
    monkeypatch.setattr("hello_agentic_world.cli.run_agent", fake_run_agent)
    monkeypatch.setattr("hello_agentic_world.cli.save_run", fake_save_run)

    exit_code = main(
        [
            "--workspace",
            "workspace",
            "--model",
            "llama3.2:latest",
            "How many Python files exist?",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Request: How many Python files exist?\n{'answer': '3'}\n"
    assert captured.err == ""


def test_model_errors_are_printed_without_traceback(capsys, monkeypatch) -> None:
    def fake_run_agent(decide, *, workspace_root, max_steps):
        raise ModelError("Ollama request failed with status 503")

    monkeypatch.setattr("hello_agentic_world.cli.run_agent", fake_run_agent)

    exit_code = main(["--workspace", "workspace", "How many Python files exist?"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == (
        "Request: How many Python files exist?\n"
        "Ollama request failed with status 503\n"
    )
    assert captured.err == ""


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
