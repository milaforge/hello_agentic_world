# Stage 1 — Hello Agent

Build the smallest useful agentic system:

> goal → choose one action → validate → execute → observe → continue or finish

## Goal

Answer:

> How many Python files exist under `workspace/`, excluding `.venv`, and what is their total size?

The model can only propose:

- `list_directory(path)`
- `get_file_metadata(path)`
- `finish(answer, python_file_count, total_size_bytes, evidence)`

## Trust boundary

The model is untrusted. The host owns:

- path authorization;
- tool execution;
- immutable observations;
- the 15-action budget;
- completion verification.

The evaluator independently computes ground truth. It may use direct traversal because it is not part of the agent.

## Build order

1. `paths.py`: confine all access to `workspace/` and reject symlinks.
2. `tools.py`: expose narrow, deterministic filesystem operations.
3. `observations.py`: assign IDs to successful and rejected actions.
4. `completion.py`: prove exploration and numerical claims from the trace.
5. `model.py`: adapt Ollama responses into untrusted `ToolCall` values.
6. `engine.py`: run the bounded action-observation loop.
7. `tests/`: test invariants and failure behavior.
8. `evals/`: measure the actual model across repeated scenarios.

Read the files in that order.

## Run locally

```bash
uv sync
ollama pull qwen3:8b
uv run pytest
uv run hello-agent
```

Add a fixture before running the agent:

```bash
mkdir -p workspace/src workspace/.venv
printf 'print("root")\n' > workspace/main.py
printf 'print("nested")\n' > workspace/src/nested.py
printf 'ignored\n' > workspace/.venv/dependency.py
```

Inspect the generated trace in `runs/` after each run.

## Evaluate the model

```bash
uv run python -m evals.run_stage1 --model qwen3:8b --repeats 5
```

A useful first comparison is:

```bash
uv run python -m evals.run_stage1 --model llama3.2:latest --repeats 5
```

Do not evaluate only correctness. Also inspect:

- action count;
- forbidden path attempts;
- rejected finish attempts;
- budget exhaustion;
- failure traces.

## Stage completion criteria

- Deterministic tests pass.
- Every evaluation scenario can complete within 15 actions.
- No out-of-workspace or symlink access is executed.
- No completion is accepted without complete evidence.
- The selected controller reaches the pass-rate threshold you record in the Stage 1 report.

Then commit the implementation and create tag `v1`.
