# Agent Loop and Scripted Strategy

## Problem

The system needed to run more than one tool call and decide when enough evidence had been collected.

## Why

Agentic behavior is iterative. A single function call is not enough to teach budgets, state, retries, evidence accumulation, or stop conditions.

## Implementation

`agent.py` introduced the bounded host loop. `scripted.py` provided a deterministic action source so the loop could be tested before relying on an LLM.

The path correction commit changed the system to use workspace-relative paths consistently. The counting strategy was then updated to perform the real investigation instead of a placeholder behavior.

## How it works

The host loop repeatedly:

1. asks the action source for the next proposed tool call;
2. dispatches the call through host validation and execution;
3. records the observation;
4. checks whether the finish action is valid;
5. stops when complete or when the action budget is exhausted.

The scripted strategy made this deterministic enough to test exact behavior.

## Test

`tests/test_agent.py` covered loop execution. Dispatcher and tool tests changed with the workspace-relative path correction.

## Observed failure or limitation

The history shows that path shape mattered. Using paths with a `workspace/` prefix did not match the eventual contract. The corrected contract uses `"."` for the workspace root and relative paths for files beneath it.

## Next step

Replace the deterministic action source with an LLM adapter while preserving the same host-owned tool boundary.

## Related commits

- [feat(host): loop or run the actions](https://github.com/milaforge/hello_agentic_world/commit/daf96fbb49a48259d32b9c61c2948f8ad4e8f949)
- [fix(path): use relative path](https://github.com/milaforge/hello_agentic_world/commit/e3ecd00bcab2d2eefd7f91d944e00966d61d7db7)
- [feat(script): the real counting strategy](https://github.com/milaforge/hello_agentic_world/commit/b36f956672b4ae50f10b04706a3ed08d37319f5c)
- [refactor(comments): elaborate](https://github.com/milaforge/hello_agentic_world/commit/15a59f05c31328377381600d3dcf5244d247519a)
