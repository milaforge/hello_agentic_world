# Stage 3 — Self-Correcting Agent

## Task

Repair a small Python project with failing tests.

New capabilities may include:

```text
apply_patch(patch)
run_tests(target)
```

## Capability added

The agent uses environmental feedback to revise its plan. A failed test run is evidence that must affect the next action.

## Required behavior

- inspect the failure before editing;
- apply bounded, reviewable patches;
- classify test failures and tool errors;
- stop unchanged retry loops;
- verify the final state through an executed test result;
- preserve unrelated behavior.

## Evaluation focus

- first patch fails but exposes useful feedback;
- stale assumptions after code changes;
- broad rewrites where a local fix is sufficient;
- tests that pass while the requested behavior remains wrong;
- false claims of success without a post-change test run.
