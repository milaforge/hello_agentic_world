# Repository structure

The repository keeps the same conceptual shape across all branches. Modules appear only when their stage introduces the corresponding responsibility.

## Final structure on `main`

```text
.
├── README.md
├── STAGE.md
├── pyproject.toml
├── src/
│   └── hello_agentic_world/
│       ├── __init__.py
│       ├── __main__.py
│       ├── agent_loop.py
│       ├── protocol.py
│       ├── state.py
│       ├── llm/
│       │   └── ollama.py
│       ├── tools/
│       │   ├── registry.py
│       │   ├── filesystem.py
│       │   ├── editing.py
│       │   └── testing.py
│       ├── safety/
│       │   ├── paths.py
│       │   ├── policy.py
│       │   └── approvals.py
│       ├── evidence/
│       │   ├── observations.py
│       │   └── verifier.py
│       └── persistence/
│           ├── events.py
│           ├── checkpoints.py
│           └── retrieval.py
├── tests/
│   ├── unit/
│   └── integration/
├── evals/
│   ├── __init__.py
│   ├── run.py
│   ├── ground_truth.py
│   ├── scorers.py
│   ├── cases/
│   │   ├── stage_1/
│   │   ├── stage_2/
│   │   ├── stage_3/
│   │   ├── stage_4/
│   │   └── stage_5/
│   └── fixtures/
├── docs/
│   ├── CURRICULUM.md
│   ├── REPOSITORY_STRUCTURE.md
│   ├── BRANCH_WORKFLOW.md
│   ├── EVALUATION.md
│   ├── contracts/
│   │   ├── agent-loop.md
│   │   ├── tool-protocol.md
│   │   └── completion.md
│   └── stages/
│       ├── 01-hello-agent.md
│       ├── 02-file-detective.md
│       ├── 03-self-correcting.md
│       ├── 04-persistent.md
│       └── 05-governed.md
├── workspace/
│   └── .gitkeep
├── runs/
│   └── .gitkeep
└── .gitignore
```

## Responsibility boundaries

### `src/hello_agentic_world/`

Production behavior only. It must not contain evaluator shortcuts or direct access to scenario answers.

### `tools/`

Small, typed capabilities. Tools perform operations; they do not decide which operation should happen next.

### `safety/`

Host-enforced authorization and argument validation. Prompts may explain policy, but prompts are not a security boundary.

### `evidence/`

Immutable observations and completion verification. A model statement is not evidence until the host associates it with an executed result.

### `persistence/`

Durable event history, checkpoints, and retrieval. Persist facts and provenance, not hidden reasoning.

### `evals/`

Independent scenario setup, ground truth, scoring, and trace assertions. The agent must not import from this package.

### `workspace/`

The only filesystem area exposed to the agent. Evaluation fixtures are copied here before a run.

### `runs/`

Generated traces, model responses, metrics, and reports. Keep it out of Git except for `.gitkeep`.

## Naming rules

- Python package: `hello_agentic_world`
- CLI command/module: `python -m hello_agentic_world`
- Branches: `stage/<number>-<name>`
- Immutable checkpoints: `v0` through `v5`
- Student branches: `work/<number>-<name>`
- Observation IDs: `obs-0001`, `obs-0002`, …
- Evaluation case IDs: `s<stage>-<purpose>-<number>`

## Structure rule

Do not create a module merely because a future stage may need it. Introduce it in the first stage that gives it a real responsibility and test.
