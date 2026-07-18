# Safe Filesystem Tools

## Problem

The agent needed to inspect files without receiving broad filesystem authority.

## Why

The stage is about safe tool use. Direct shell access or recursive host-side globbing would bypass the lesson. The model should be forced to gather evidence through narrow, observable operations.

## Implementation

`tools.py` and `contracts.py` introduced bounded tool contracts and filesystem operations. Tests covered basic file inspection behavior.

A later fix changed boundary handling so authorization checks happen before other path behavior. Test fixtures were then shared through `tests/conftest.py`.

The observable correction in this stage is path handling: workspace inputs are relative to `workspace_root`, and the root is addressed as `"."`.

## How it works

The tool layer exposes limited operations:

```text
list_directory(path)
get_file_metadata(path)
```

The host resolves each requested path under the configured workspace root and rejects paths that escape the boundary or violate the stage rules.

## Test

`tests/test_tools.py` checks successful reads and rejection behavior. Fixture reuse moved shared setup into `tests/conftest.py`, reducing duplicated test scaffolding.

## Observed failure or limitation

The commit history shows a path-boundary correction. The important lesson is that path normalization and authorization order are security-sensitive; checking the boundary after other path handling can make tests pass for the wrong reason.

## Next step

Add a dispatcher so model-proposed tool names and payloads can be validated before execution.

## Related commits

- [feat: tools](https://github.com/milaforge/hello_agentic_world/commit/8873e8014fdcb76675a627fe01581cda44ddeaa5)
- [refactor: remove unused](https://github.com/milaforge/hello_agentic_world/commit/b04d568b806358a03f9b3568ce219ab1b6b9c8be)
- [fix(tools): check for boundary first](https://github.com/milaforge/hello_agentic_world/commit/ef251a51cd227212b9af27e980973daa8fc70b84)
- [refactor(test): reuse fixture](https://github.com/milaforge/hello_agentic_world/commit/751f134c917cf31d4b45c6fe301e116ca08b048e)
