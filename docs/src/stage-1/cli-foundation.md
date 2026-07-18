# CLI Foundation

## Problem

The repository needed a runnable surface before agent behavior could be tested.

## Why

A command-line entry point gives the stage a narrow interface: accept a user goal, run the host program, and print the result. Keeping this small made later changes testable without committing to a broader framework.

## Implementation

The package skeleton, `pyproject.toml`, lockfile, `cli.py`, and CLI tests were added.

The important design choice was to start with a host-controlled executable path rather than giving the model direct access to the environment.

## How it works

The CLI parses input and invokes repository code. It is the outer boundary for local usage, not the source of agent intelligence.

## Test

`tests/test_cli.py` was introduced to lock the command behavior.

## Observed failure or limitation

The CLI alone could not inspect `workspace/`, validate tools, or prove completion. It only established the runnable package.

## Next step

Add bounded filesystem tools and tests for their safety properties.

## Related commits

- [feat 1 : the cli foundation](https://github.com/milaforge/hello_agentic_world/commit/f248fe1f607f1bb63723d6b1096c2512aebe2fea)
