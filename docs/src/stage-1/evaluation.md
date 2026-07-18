# Evaluation Loop

## Problem

Passing unit tests does not prove that the model-driven loop succeeds reliably.

## Why

Agentic systems fail through behavior over time: repeated unsupported finishes, path mistakes, budget exhaustion, or plausible but incomplete answers. Stage 1 needs repeated-run evaluation, not only deterministic unit tests.

## Implementation

`evals/run.py` added automatic evaluation. It creates scenarios, runs the agent, computes ground truth independently, and reports pass or failure details. A later fix saved run outputs.

## How it works

The evaluator is outside the agent. It can inspect the fixture directly because it is measuring the agent, not participating in the agent loop.

That separation keeps the lesson intact:

```text
agent: must gather evidence through tools
evaluator: computes ground truth independently
```

## Test

`tests/test_evals_run.py` was added. Agent tests were updated around evaluation behavior.

## Observed failure or limitation

The `fix(eval): save runs` commit shows that evaluation is more useful when failures leave artifacts. Without saved runs, debugging repeated behavior is harder.

## Next step

Squash the completed stage to a clean `v1` checkpoint, then refactor maintainability without changing the teaching contract.

## Related commits

- [feat(eval): automatic evaluation](https://github.com/milaforge/hello_agentic_world/commit/c86910a0ef46f6325125e7044a07422d8b493791)
- [fix(eval): save runs](https://github.com/milaforge/hello_agentic_world/commit/eb865dc1cbf2923cd11da3208f1001da5c2c56ce)
