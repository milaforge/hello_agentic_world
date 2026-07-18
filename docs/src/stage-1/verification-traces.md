# Finish Verification and Traces

## Problem

The model needed a way to finish, but accepting a finish call blindly would reintroduce unsupported claims.

## Why

The stage asks for a count and total size. Those numbers are only trustworthy if they are supported by observed file metadata. Completion has to be a checked operation, not a polite convention.

## Implementation

`verification.py` added finish validation. The agent loop was updated to use it. The CLI gained model selection, and `traces.py` added preliminary run output for replay and inspection.

## How it works

The finish action is accepted only when the recorded evidence supports the structured answer. If the evidence is incomplete or inconsistent, the host rejects completion and the loop continues until the budget is exhausted or a supported answer appears.

Traces make the run auditable after the fact. They are useful for seeing not only the final answer, but also which actions were tried and which observations were recorded.

## Test

`tests/test_verification.py` introduced direct tests for completion checks. `tests/trace_test.py` covered trace output, and CLI tests were updated for model selection and trace behavior.

## Observed failure or limitation

The verifier can only validate against observations the host recorded. If the agent failed to inspect a file, completion should fail instead of filling the gap with inference.

## Next step

Evaluate the full behavior repeatedly across scenarios, using an evaluator that computes ground truth outside the agent.

## Related commits

- [feat(safety): verify finish function](https://github.com/milaforge/hello_agentic_world/commit/d1b3a2eab9d1fe0391497810fb1b00518dba7ef6)
- [feat(cli): accept model](https://github.com/milaforge/hello_agentic_world/commit/145ef8e78dd08c825a7358499af56453e481086e)
- [feat(traces): preliminary output for replay](https://github.com/milaforge/hello_agentic_world/commit/e9df63a344f53fb74c68d150c9b2e461dafb073a)
