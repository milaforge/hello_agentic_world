# Stage 1: Hello Agent

## Stage goal

Build the smallest useful agentic system:

```text
goal -> propose action -> validate -> execute -> observe -> continue or finish
```

The agent answers:

> How many Python files exist under `workspace/`, excluding `.venv`, and what is their total size?

The model can only propose narrow tools. The host validates tool names and arguments, enforces workspace boundaries, executes tools, records observations, applies budgets, and accepts completion only when evidence supports the answer.

## Starting state

Stage 1 starts from `v0`, a documentation-only foundation. There is no package, CLI, tool dispatcher, observation log, model adapter, evaluator, or tests for executable behavior.

## Concepts introduced

- A model proposal is not an observed fact.
- Filesystem access is confined to `workspace/`.
- Tool execution belongs to the host, not the model.
- Every accepted or rejected action becomes inspectable state.
- Completion is verified against evidence, not trusted because the model says it is done.
- Evaluations run outside the agent and compute ground truth independently.

## Final architecture

Stage 1 ends with:

- `cli.py`: command-line entry point.
- `tools.py`: bounded filesystem tools.
- `dispatcher.py`: tool name and payload validation plus execution.
- `observations.py`: recorded action results.
- `agent.py`: bounded action-observation loop.
- `model.py`: Ollama response adapter.
- `task_state.py`: observed workspace state used for grounding.
- `verification.py`: finish validation.
- `traces.py`: run trace writing.
- `evals/run.py`: repeated scenario evaluation.

## Stage checkpoint

`v1` is the squashed Stage 1 checkpoint. The detailed development history is on `stage/1-hello-agent-world`.

The branch history includes a later local-only evaluation fix, `fix(eval): save runs`, which is documented because it is present in this repository branch.

## Related history

- [v0 foundation](https://github.com/milaforge/hello_agentic_world/commit/841ebf664b60eab2a4ad797d918d73afb2edd76e)
- [v1: bounded observable filesystem agent](https://github.com/milaforge/hello_agentic_world/commit/c8d87cbb9d6b5d33c002c5d9ab122ae7450b62d1)
