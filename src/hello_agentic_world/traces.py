from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from hello_agentic_world.agent import AgentRun


def save_run(
    run: AgentRun,
    *,
    request: str,
    model: str,
    output_dir: Path = Path("runs"),
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC)
    run_id = timestamp.strftime("%Y%m%dT%H%M%S.%fZ")

    payload: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "created_at": timestamp.isoformat(),
        "request": request,
        "model": model,
        "status": "completed" if run.completed else "failed",
        "error": run.error,
        "observations": [asdict(observation) for observation in run.observations],
        "final_result": run.final_value,
    }

    path = output_dir / f"{run_id}.json"

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    return path
