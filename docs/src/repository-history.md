# Repository History

This repository separates clean learning checkpoints from detailed implementation history.

`main` contains clean milestone commits. In the current checkout, `main` points at `v1.5`, which contains the Stage 1 implementation plus a maintainability refactor as squashed milestone commits.

Tags identify stable snapshots:

- `v0`: foundation before Stage 1.
- `v1`: bounded observable filesystem agent.
- `v1.5`: Stage 1 maintainability refactor.

The `stage/*` and `refactor/*` branches retain the complete development history where that history exists:

- `stage/1-hello-agent-world`: Stage 1 implementation commits.
- `refactor/v1.5-maintainability`: Stage 1.5 refactor commits.

No `stage/2-*`, `stage/3-*`, `stage/4-*`, `stage/5-*`, `v2`, `v3`, `v4`, or `v5` refs are present in the current local or upstream repository. The Stage 2-5 pages in this book are placeholders until those implementation histories exist.

## How to inspect changes

Each discussed commit is linked to its GitHub commit page:

```text
https://github.com/milaforge/hello_agentic_world/commit/<sha>
```

That page includes the commit diff. Use it to inspect the exact evolution of code, tests, and documentation.

Useful local commands:

```bash
git log --reverse --oneline v0..stage/1-hello-agent-world
git log --reverse --oneline v1..refactor/v1.5-maintainability
git show <sha>
```

The intended teaching workflow is:

1. Read a stage goal.
2. Inspect the branch history chronologically.
3. Study the grouped implementation chapters.
4. Open the linked commit diffs for exact code changes.
5. Compare the branch to the stable tag for the checkpoint.
