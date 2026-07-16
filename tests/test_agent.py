
from hello_agentic_world.agent import Action, run_agent
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


def test_agent_executes_batched_actions_in_one_decision() -> None:
    def batched_script(observations):
        if not observations:
            return (
                Action("list_directory", {"path": "."}),
                Action("get_file_metadata", {"path": "main.py"}),
                Action(
                    "finish",
                    {
                        "answer": "done",
                        "python_file_count": 1,
                        "total_size_bytes": 15,
                        "evidence": ["obs-2"],
                    },
                ),
            )

        raise AssertionError("this test batch should finish in the first decision")

    result = run_agent(batched_script)

    assert result.completed is True
    assert [observation.call.name for observation in result.observations] == [
        "list_directory",
        "get_file_metadata",
        "finish",
    ]


def test_batched_observations_preserve_request_order() -> None:
    def batched_script(observations):
        if not observations:
            return (
                Action("get_file_metadata", {"path": "main.py"}),
                Action("get_file_metadata", {"path": "notes.txt"}),
            )

        return Action(
            "finish",
            {
                "answer": "done",
                "python_file_count": 2,
                "total_size_bytes": 20,
                "evidence": ["obs-1", "obs-2"],
            },
        )

    result = run_agent(batched_script)

    assert result.completed is True
    assert [
        (observation.id, observation.call.arguments["path"])
        for observation in result.observations[:2]
    ] == [
        ("obs-1", "main.py"),
        ("obs-2", "notes.txt"),
    ]


def test_batched_actions_stop_at_step_budget() -> None:
    def batched_script(observations):
        return (
            Action("list_directory", {"path": "."}),
            Action("get_file_metadata", {"path": "main.py"}),
        )

    result = run_agent(batched_script, max_steps=1)

    assert result.completed is False
    assert result.error == "step_budget_exhausted"
    assert len(result.observations) == 1


def test_empty_action_batches_consume_budget() -> None:
    def empty_batch(observations):
        return ()

    result = run_agent(empty_batch, max_steps=1)

    assert result.completed is False
    assert result.error == "step_budget_exhausted"
    assert len(result.observations) == 1
    assert result.observations[0].call.name == "invalid_model_response"


def test_script_counts_python_files() -> None:
    result = run_agent(
        filesystem_script,
        max_steps=15,
    )

    assert result.completed is True
    assert result.final_value is not None
    assert result.final_value["python_file_count"] == 3
    assert result.final_value["total_size_bytes"] == 37
