from __future__ import annotations

from hello_agentic_world.observations import Observation


def verify_finish(
    observations: tuple[Observation, ...],
    *,
    python_file_count: int,
    total_size_bytes: int,
    evidence: list[str],
) -> tuple[bool, str | None]:

    # 1. Evidence IDs must exist

    indexed = {observation.id: observation for observation in observations}

    for evidence_id in evidence:
        if evidence_id not in indexed:
            return False, f"unknown_evidence:{evidence_id}"

    # 2. Evidence must come from successful metadata calls

    metadata_observations = []

    for evidence_id in evidence:
        observation = indexed[evidence_id]

        if observation.call.name != "get_file_metadata":
            continue

        if not observation.result.ok:
            continue

        metadata_observations.append(observation)

    # 3. Recalculate facts from evidence

    actual_count = len(metadata_observations)

    actual_size = sum(
        observation.result.value["size_bytes"]
        for observation in metadata_observations
        if observation.result.value is not None
    )

    if actual_count != python_file_count:
        return (
            False,
            f"count_mismatch:expected={actual_count},got={python_file_count}",
        )

    if actual_size != total_size_bytes:
        return (False, f"size_mismatch:expected={actual_size},got={total_size_bytes}")

    return True, None
