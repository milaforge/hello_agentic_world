from pathlib import Path

import pytest

from hello_agentic_world.observations import ObservationStore


@pytest.fixture
def sample_workspace(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    (workspace / "main.py").write_text("print('hello')\n")
    (workspace / "notes.txt").write_text("notes")

    src = workspace / "src"
    src.mkdir()
    (src / "app.py").write_text("x = 1\n")

    return workspace


@pytest.fixture
def sample_store() -> None:
    return ObservationStore()
