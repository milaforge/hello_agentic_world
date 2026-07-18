# Stage 1.5 Refactor

## Problem

After Stage 1 worked, several maintainability issues remained visible in the implementation.

## Why

The teaching system should stay small, but not brittle. Refactoring after a working checkpoint makes the production lesson explicit: preserve behavior while improving boundaries, diagnostics, and testability.

## Implementation

The `refactor/v1.5-maintainability` branch made six observable changes:

- clearer verification diagnostics;
- scripted actions derived from task state;
- finish verification failures surfaced by the agent;
- runtime dependencies injected into the agent;
- tool specifications centralized in the dispatcher path;
- tool payloads typed in contracts.

## How it works

The refactor keeps the Stage 1 contract intact while making internal responsibilities sharper. The agent loop receives dependencies rather than constructing everything implicitly. Tool schemas move toward a single source of truth. Payload typing makes model and tool boundaries more explicit.

## Test

The refactor updated tests in:

- `tests/test_verification.py`
- `tests/test_agent.py`
- `tests/test_dispatcher.py`

Those tests anchor the behavior that should not change while internals become clearer.

## Observed failure or limitation

The refactor history does not add a new stage capability. It improves the maintainability of Stage 1 and prepares the code for later stages.

## Next step

Future stages can add investigation, repair, persistence, and policy on top of the cleaned Stage 1 shape. Their implementation history is not present in the current refs.

## Related commits

- [fix(verification): clarify size mismatch diagnostic](https://github.com/milaforge/hello_agentic_world/commit/1c3d3f0893443734abdd338e5f13b5d1411d19be)
- [refactor(script): derive filesystem actions from task state](https://github.com/milaforge/hello_agentic_world/commit/cbdd5fb1eb75f0ccca2f37a2764e9d080bc80dc5)
- [refactor(agent): surface finish verification failures](https://github.com/milaforge/hello_agentic_world/commit/452ed9f52130ba583fc0d54aeda85b2ae445f983)
- [refactor(agent): inject runtime dependencies](https://github.com/milaforge/hello_agentic_world/commit/a4f0a055be889658fe7ae3621e3f11eba97041e4)
- [refactor(tools): centralize tool specifications](https://github.com/milaforge/hello_agentic_world/commit/68a5d4af6a034c6e16fcb2da8ba4c2bd1716b5f6)
- [refactor(contracts): type tool payload shapes](https://github.com/milaforge/hello_agentic_world/commit/87f2bda244e91e7b391b1110a6d5ad2e3f2550b3)
