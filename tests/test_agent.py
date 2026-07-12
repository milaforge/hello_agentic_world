
from hello_agentic_world.agent import run_agent
from hello_agentic_world.scripted import simple_script, never_finish, unsafe_script, filesystem_script


def test_agent_executes_until_finish() -> None:
    result = run_agent(simple_script)

    assert result.completed is True
    assert result.final_value is not None
    assert len(result.observations) == 2

    assert result.observations[0].call.name == "list_directory"
    assert result.observations[1].call.name == "finish"


def test_agent_stops_at_step_budget() -> None:
    result = run_agent(never_finish, max_steps=3)

    assert result.completed is False
    assert result.error == "step_budget_exhausted"
    assert len(result.observations) == 3


def test_invalid_actions_consume_budget() -> None:
    result = run_agent(unsafe_script, max_steps=2)

    assert result.completed is False
    assert len(result.observations) == 2

    for obs in result.observations:
        assert obs.result.ok is False
        assert obs.result.error == "unknown_tool"

def test_script_counts_python_files() -> None:
    result = run_agent(
        filesystem_script,
        max_steps=15,
    )

    assert result.completed is True
    assert result.final_value is not None
    assert result.final_value["python_file_count"] == 3
    assert result.final_value["total_size_bytes"] == 37