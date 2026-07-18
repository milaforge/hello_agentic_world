# What

Hello, Agentic world!

This is a bounded system, an agent whose actions, evidence, permissions, and failures can be inspected and evaluated.

> receive a goal → choose an action → use a tool → observe the result → update its state → stop with evidence

# How

This repository builds that system in five stages. Each stage extends the same agent loop and adds one capability, one failure mode, and one evaluation layer.

## One agent, five stages

| Stage | Git branch                | Capability added               | Failure addressed               |
| ----- | ------------------------- | ------------------------------ | ------------------------------- |
| 1     | `stage/1-hello-agent`     | Bounded tool-use loop          | Invented actions and results    |
| 2     | `stage/2-file-detective`  | Investigation and evidence     | Unsupported conclusions         |
| 3     | `stage/3-self-correcting` | Feedback-driven repair         | Repeating a failed approach     |
| 4     | `stage/4-persistent`      | Checkpoints and retrieval      | Lost context after interruption |
| 5     | `stage/5-governed`        | Policy, approval, verification | Unsafe or dishonest autonomy    |

Every stage is cumulative. `main` contains the completed Stage 5 implementation.

## Learn by doing

Start Stage 1 from the empty foundation:

```bash
git switch --detach v0
git switch -c work/1-hello-agent
```

Read `STAGE.md`, implement the requirements, and run the tests and evaluations. Compare your result only after finishing:

```bash
git diff v1 -- src tests evals
```

For the next stage, start from the previous completed checkpoint:

```bash
git switch -c work/2-file-detective v1
```

Branches are browsable solutions. Tags `v0` through `v5` are immutable learning checkpoints.

## Run locally

Requirements:

- Python 3.12+
- `uv`
- Ollama
- `qwen3:8b` as the default controller model

```bash
uv sync
ollama pull qwen3:8b
uv run pytest
uv run python -m hello_agentic_world "your task"
uv run python -m evals.run --stage 1
```

## Non-negotiable boundary

The model may propose actions. It may not execute them directly.

The host program must:

- validate tool names and arguments;
- enforce workspace and authorization boundaries;
- execute tools and record observations;
- enforce action, time, and retry budgets;
- reject completion claims not supported by evidence.

The evaluator is independent from the agent and computes ground truth directly.

## Repository map

```text
src/          agent implementation
tests/        deterministic unit and integration tests
evals/        scenario fixtures, scorers, and repeated-run evaluation
docs/         curriculum, contracts, architecture, and workflow
workspace/    the only filesystem area available to the agent
runs/         generated traces and reports; not committed
```

See:

- [`docs/CURRICULUM.md`](docs/CURRICULUM.md)
- [`docs/REPOSITORY_STRUCTURE.md`](docs/REPOSITORY_STRUCTURE.md)
- [`docs/BRANCH_WORKFLOW.md`](docs/BRANCH_WORKFLOW.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)

## Documentation

The mdBook in [`docs/`](docs/) teaches the project from the branch history: `main` keeps clean squashed milestones, tags mark stable snapshots, and `stage/*` plus `refactor/*` branches preserve the detailed implementation commits.

Run it locally:

```bash
cargo install mdbook
mdbook serve docs
```

If `http://localhost:3000/` is blank or the port is already occupied, bind explicitly to IPv4 on another port:

```bash
mdbook serve docs --hostname 127.0.0.1 --port 3001 --open
```

## What this work is not

No agent framework, multi-agent role play, open shell, browser control, production credentials, or autonomous network access. Those increase surface area before the core loop is understood.

The outcome is not “an LLM that calls tools.” It is an agent whose actions, evidence, permissions, and failure modes can be inspected and evaluated.


## Repository history

`main` contains one squashed milestone commit per completed stage.

The complete implementation history, including intermediate decisions, failures, and refactors, remains available in each `stage/*` branch.

The mdBook documentation reconstructs every stage from its branch history and links directly to the relevant commit diffs.
