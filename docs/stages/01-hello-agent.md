# Stage 1 — Hello Agent

## Task

Build a command-line agent that can answer:

> How many Python files exist under `workspace/`, excluding `.venv`, and what is their total size?

Available capabilities:

```text
list_directory(path)
get_file_metadata(path)
finish(result, evidence)
```

`list_directory` returns one level only. The model decides where to inspect next and when enough evidence exists.

## Do not bypass the lesson

The application workflow must not directly call recursive globbing or compute the answer for the model. Direct traversal is allowed only inside the independent evaluator.

## Required behavior

- inspect only paths under `workspace/`;
- never follow symlinks;
- record every tool result as an observation;
- reject unknown tools and invalid arguments;
- count rejected proposals against the action budget;
- accept completion only when its evidence supports the structured answer;
- terminate within the scenario budget.

## Pass criteria

- exact count and total bytes;
- complete evidence for every counted file;
- zero accepted fabricated observations;
- zero execution outside `workspace/`;
- successful termination in all deterministic fixtures;
- required repeated-run pass rate.
