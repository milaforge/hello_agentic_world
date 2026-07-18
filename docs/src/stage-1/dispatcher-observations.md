# Dispatcher and Observations

## Problem

Tool functions existed, but the host still needed a central place to accept or reject model proposals and record what happened.

## Why

An agent loop is only debuggable if actions and outcomes are explicit. Unknown tools, malformed arguments, authorization failures, and successful results should all become inspectable records.

## Implementation

`dispatcher.py` added tool dispatch. `observations.py` added structured observations and IDs. Tests expanded around accepted calls, rejected calls, and recorded outcomes.

## How it works

The dispatcher receives an untrusted tool call, validates the tool name and arguments, runs the matching host function only if valid, and returns an observation.

That keeps this boundary clear:

```text
model output -> host validation -> host execution -> observation
```

## Test

`tests/test_dispatcher.py` was introduced and then expanded when observations became first-class records.

## Observed failure or limitation

Initial dispatch handled execution, but the later observation layer made failures and rejections part of the trace instead of incidental control flow.

## Next step

Use the dispatcher inside a bounded loop that repeatedly asks for an action until the task finishes or the budget is exhausted.

## Related commits

- [feat(tools): dispatch](https://github.com/milaforge/hello_agentic_world/commit/036fd8afd7066f79c7783a250c4c9b26a29ecab1)
- [feat(observation): init](https://github.com/milaforge/hello_agentic_world/commit/9e554409211b090139b9eb1eb1e5a742df3e85f1)
