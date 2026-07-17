from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_eval_runner():
    path = Path(__file__).parents[1] / "evals" / "run.py"
    spec = importlib.util.spec_from_file_location("evals_run", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_eval_runner_defaults_to_qwen_model(capsys, monkeypatch) -> None:
    run = load_eval_runner()
    seen_models = []

    def fake_evaluate_scenario(scenario, *, workspace, model):
        seen_models.append(model)
        return {"scenario": scenario.name, "passed": True}

    monkeypatch.setattr(run, "evaluate_scenario", fake_evaluate_scenario)

    exit_code = run.main([])

    assert exit_code == 0
    assert seen_models == ["qwen3:8b"] * len(run.SCENARIOS)
    assert '"passed": true' in capsys.readouterr().out


def test_eval_runner_accepts_model_argument(monkeypatch) -> None:
    run = load_eval_runner()
    seen_models = []

    def fake_evaluate_scenario(scenario, *, workspace, model):
        seen_models.append(model)
        return {"scenario": scenario.name, "passed": True}

    monkeypatch.setattr(run, "evaluate_scenario", fake_evaluate_scenario)

    exit_code = run.main(["--model", "llama3.2:latest"])

    assert exit_code == 0
    assert seen_models == ["llama3.2:latest"] * len(run.SCENARIOS)


def test_eval_runner_verbose_prints_scenario_progress(capsys, monkeypatch) -> None:
    run = load_eval_runner()

    def fake_evaluate_scenario(scenario, *, workspace, model):
        return {"scenario": scenario.name, "passed": True, "steps": 3}

    monkeypatch.setattr(run, "evaluate_scenario", fake_evaluate_scenario)

    exit_code = run.main(["--verbose"])

    out = capsys.readouterr().out

    assert exit_code == 0
    assert "[1/3] Evaluating basic (2 scenarios left)" in out
    assert "[2/3] Evaluating empty (1 scenario left)" in out
    assert "[3/3] Evaluating ignore_venv (0 scenarios left)" in out
    assert "0:00" in out


def test_format_elapsed_uses_minutes_and_zero_padded_seconds() -> None:
    run = load_eval_runner()

    assert run.format_elapsed(0) == "0:00"
    assert run.format_elapsed(1.9) == "0:01"
    assert run.format_elapsed(70) == "1:10"
