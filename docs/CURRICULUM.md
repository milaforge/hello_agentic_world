# Curriculum

The curriculum grows one implementation. A new stage may extend the agent loop, tools, state, policy, persistence, or evaluator, but it must not replace the previous architecture with an unrelated work.

## Learning sequence

| Work on | Start from | Compare against |
|---|---|---|
| Stage 1 | `v0` | `v1` |
| Stage 2 | `v1` | `v2` |
| Stage 3 | `v2` | `v3` |
| Stage 4 | `v3` | `v4` |
| Stage 5 | `v4` | `v5` |

For each stage:

1. Read its specification in `docs/stages/`.
2. Predict likely failures before coding.
3. Implement deterministic host behavior first.
4. Add the model-controlled behavior.
5. Add adversarial and repeated-run evaluations.
6. Inspect traces, not only final answers.
7. Compare with the reference stage after completing your attempt.

## Stage 1 — Hello Agent

**Goal:** implement one bounded model–tool loop.

The agent investigates `workspace/` through narrow filesystem tools and answers with observed evidence.

Adds:

- system prompt and tool schemas;
- action validation and execution;
- observation history;
- step budget and stop condition;
- independent deterministic ground truth.

Central question:

> Can the system distinguish a proposed action from an observed fact?

Specification: [`stages/01-hello-agent.md`](stages/01-hello-agent.md)

## Stage 2 — File Detective

**Goal:** investigate a non-trivial repository question before reaching a conclusion.

Adds:

- explicit investigation state;
- search and bounded file-reading tools;
- evidence ledger;
- completion verification for coverage and support;
- evaluation of incomplete but plausible answers.

Central question:

> Does the agent know what it still needs to inspect?

Specification: [`stages/02-file-detective.md`](stages/02-file-detective.md)

## Stage 3 — Self-Correcting Agent

**Goal:** repair a small project by using environmental feedback.

Adds:

- patch application;
- test execution;
- failure classification;
- retry budgets;
- comparison between attempted and verified completion.

Central question:

> Does failure change the next action, or only produce another confident guess?

Specification: [`stages/03-self-correcting.md`](stages/03-self-correcting.md)

## Stage 4 — Persistent Agent

**Goal:** preserve and recover useful state across interruption.

Adds:

- append-only event log;
- checkpoints and resume;
- retrieval from prior observations and documents;
- provenance for retrieved context;
- stale-state and confirmation-bias evaluations.

Central question:

> Can the agent resume without pretending that remembered context is current truth?

Specification: [`stages/04-persistent.md`](stages/04-persistent.md)

## Stage 5 — Governed Agent

**Goal:** complete an issue-to-patch workflow under explicit policy.

Adds:

- capability and path policy;
- approval gates for risky actions;
- preconditions and postconditions;
- independent completion verifier;
- audit trace and denial-path evaluations.

Central question:

> Can the agent remain useful when it is not authorized to do everything required?

Specification: [`stages/05-governed.md`](stages/05-governed.md)
