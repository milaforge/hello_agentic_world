from pathlib import Path
import json
from hello_agentic_world.agent import AgentRun
from hello_agentic_world.observations import Observation, ToolCall, ToolResult
from hello_agentic_world.traces import save_run
from pprint import pprint
from dataclasses import asdict


def test_saves_completed_run_as_json(tmp_path: Path) -> None:
    run = AgentRun(
        completed=True,
        observations=(
            Observation(
                id="obs-1",
                step=1,
                call=ToolCall(
                    name="list_directory",
                    arguments={"path": "."},
                ),
                result=ToolResult(ok=True, value={"path": ".", "entries": []}),
            ),
        ),
        final_value={
            "answer": "No Python files found.",
            "python_file_count": 0,
            "total_size_bytes": 0,
            "evidence": [],
        },
    )

    pprint(asdict(run))

    path = save_run(
        run,
        request="Count Python files",
        model="qwen3:8b",
        output_dir=tmp_path,
    )

    payload = json.loads(path.read_text())

    assert path.suffix == ".json"
    assert payload["schema_version"] == 1
    assert payload["status"] == "completed"
    assert payload["request"] == "Count Python files"
    assert payload["model"] == "qwen3:8b"
    assert payload["observations"][0]["id"] == "obs-1"
    assert payload["final_result"]["python_file_count"] == 0


def test_saves_failed_run(tmp_path: Path) -> None:
    run = AgentRun(
        completed=False,
        observations=(),
        error="step_budget_exhausted",
    )

    path = save_run(
        run,
        request="Count Python files",
        model="qwen3:8b",
        output_dir=tmp_path,
    )
    payload = json.loads(path.read_text())

    assert payload["status"] == "failed"
    assert payload["error"] == "step_budget_exhausted"
    assert payload["final_result"] is None
