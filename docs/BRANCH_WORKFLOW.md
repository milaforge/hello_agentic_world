# Branch workflow

## Reference model

```text
v0
 └─ stage/1-hello-agent       ── tag v1
     └─ stage/2-file-detective ── tag v2
         └─ stage/3-self-correcting ── tag v3
             └─ stage/4-persistent ── tag v4
                 └─ stage/5-governed ── tag v5 ── main
```

Each stage branch is cumulative and contains a completed reference implementation. `main` points to the latest complete stage.

Branches can receive corrections. Published tags do not move.

## Build the instructor reference stages

### Stage 1

```bash
git switch -c stage/1-hello-agent v0
# Implement Stage 1 in small reviewed commits.
git tag -a v1 -m "Stage 1: bounded tool-use agent"
```

### Stage 2

```bash
git switch -c stage/2-file-detective v1
# Add only Stage 2 capabilities.
git tag -a v2 -m "Stage 2: evidence-based investigation"
```

Repeat the pattern through `v5`.

After Stage 5:

```bash
git switch main
git merge --ff-only stage/5-governed
git push origin main --follow-tags
git push origin 'stage/*'
```

## Student workflow

Start without the solution:

```bash
git switch --detach v0
git switch -c work/1-hello-agent
```

Implement and evaluate. Then compare:

```bash
git diff --stat v1
git diff v1 -- src tests evals
git log --oneline v0..v1
```

Begin Stage 2 from the official Stage 1 checkpoint:

```bash
git switch -c work/2-file-detective v1
```

This keeps each exercise focused. A student can also continue from their own previous branch to experience accumulated design consequences.

## Updating published stages

Do not force-push stage branches after students may have based work on them.

For a correction:

1. Commit the fix to the affected stage branch.
2. Cherry-pick or merge the fix into every later stage.
3. Create a new patch tag such as `v2.1`; do not move `v2`.
4. Record the correction in the changelog.

## Pull requests

A stage pull request should state:

- capability added;
- invariant preserved;
- new tools or permissions;
- new failure scenarios;
- evaluation result before and after the change.

A stage is incomplete if only the happy-path implementation changes.
