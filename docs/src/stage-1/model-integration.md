# Model Integration

## Problem

The deterministic loop proved the host behavior, but Stage 1 still needed the model in the loop.

## Why

The useful teaching point is not that Python can count files. It is that an untrusted model can drive a bounded process while the host preserves evidence, safety, and correctness checks.

## Implementation

`model.py` added an Ollama-backed adapter. The CLI gained model support, and `debug.py` helped inspect model interaction. Later commits added task state as grounding context and support for multiple tool calls in one model response.

## How it works

The model adapter turns an LLM response into host-understood tool calls. The model still does not execute anything directly. Its output remains a proposal that must pass through the dispatcher.

Task state gives the model a compact view of what has already been observed, reducing reliance on unsupported memory.

## Test

`tests/test_model.py` was added for model-response parsing and multi-tool-call behavior. CLI and dispatcher tests were updated around the Ollama integration.

## Observed failure or limitation

The model can produce multiple proposed actions or malformed responses. The host must adapt valid proposals and reject invalid ones without treating either as environmental truth.

## Next step

Add finish verification so the model cannot end the run with an answer that is unsupported by observations.

## Related commits

- [feat(llm): add ollama into the loop](https://github.com/milaforge/hello_agentic_world/commit/84aeffd7c3eee35e5d6b4758387e4ebca310aff0)
- [feat(llm): add state memory as the grounding truth](https://github.com/milaforge/hello_agentic_world/commit/933750072a50623b97c0d47e48c0ae059366d948)
- [feat(llm): support multi tool call](https://github.com/milaforge/hello_agentic_world/commit/a9dbf1cea3020d49308d580c5ba8909bfd7242a3)
