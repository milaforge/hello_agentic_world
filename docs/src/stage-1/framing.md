# Framing the Lesson

## Problem

The project needed a concrete teaching target before code existed.

## Why

Agentic systems become hard to reason about when the lesson starts with a full framework. Stage 1 narrows the problem to one loop, three tool shapes, one workspace boundary, and one verifiable answer.

## Implementation

The first commits created the stage documentation and specified the task:

```text
list_directory(path)
get_file_metadata(path)
finish(result, evidence)
```

The docs also defined the trust boundary: the model proposes actions, while the host owns authorization, execution, observations, budgets, and completion checks.

## How it works

The stage specification makes unsupported claims visible. A tool call is only a request. A fact exists only after the host validates the call, executes it, and records an observation.

## Test

No executable tests existed yet. The testable requirements were introduced as acceptance criteria in `STAGE.md` and `docs/stages/01-hello-agent.md`.

## Observed failure or limitation

At this point, the repository taught the goal but had no runnable implementation.

## Next step

Create the package and command-line entry point so the stage can be exercised.

## Related commits

- [docs: init](https://github.com/milaforge/hello_agentic_world/commit/f4b87c1f5126447176fddc0c960166b6a85b56e9)
- [add the goal](https://github.com/milaforge/hello_agentic_world/commit/88de25e1112634ba3ebc705c9ba20127f28b110a)
