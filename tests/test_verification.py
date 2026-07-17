from hello_agentic_world.observations import (
    Observation,
    ToolCall,
    ToolResult,
)

from hello_agentic_world.verification import verify_finish


def make_observations():
    return (
        Observation(
            id="obs-1",
            step=1,
            call=ToolCall(
                "get_file_metadata",
                {"path": "main.py"},
            ),
            result=ToolResult(
                ok=True,
                value={
                    "path": "main.py",
                    "size_bytes": 10,
                },
            ),
        ),
        Observation(
            id="obs-2",
            step=2,
            call=ToolCall(
                "get_file_metadata",
                {"path": "app.py"},
            ),
            result=ToolResult(
                ok=True,
                value={
                    "path": "app.py",
                    "size_bytes": 20,
                },
            ),
        ),
    )


def test_accepts_correct_finish():
    ok, error = verify_finish(
        make_observations(),
        python_file_count=2,
        total_size_bytes=30,
        evidence=["obs-1", "obs-2"],
    )

    assert ok is True
    assert error is None


def test_rejects_fake_count():
    ok, error = verify_finish(
        make_observations(),
        python_file_count=100,
        total_size_bytes=30,
        evidence=["obs-1", "obs-2"],
    )

    assert ok is False
    assert "count_mismatch" in error


def test_rejects_fake_evidence():
    ok, error = verify_finish(
        make_observations(),
        python_file_count=2,
        total_size_bytes=30,
        evidence=["obs-2", "obs-3"],
    )

    assert ok is False
    assert "unknown_evidence" in error


def test_rejects_fake_size_with_clear_diagnostic():
    ok, error = verify_finish(
        make_observations(),
        python_file_count=2,
        total_size_bytes=999,
        evidence=["obs-1", "obs-2"],
    )

    assert ok is False
    assert error == "size_mismatch:expected=30,got=999"
