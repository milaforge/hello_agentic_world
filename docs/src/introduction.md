# Introduction

This book teaches the basics of agentic software development by reconstructing this repository stage by stage.

The project is intentionally small: a bounded command-line agent answers a filesystem question by proposing actions, waiting for the host to validate and execute them, recording observations, and finishing only when evidence supports the answer.

The core lesson is:

```text
model proposal != environmental fact
```

The model may suggest tool calls. The host program owns validation, execution, budgets, observations, and completion checks. That boundary is what turns an LLM that emits tool-shaped JSON into a debuggable agentic system.

## What this book covers

The current repository history contains:

- `v0`: a documentation-only foundation.
- `stage/1-hello-agent-world`: the complete Stage 1 implementation history.
- `v1`: the squashed Stage 1 checkpoint on `main`.
- `refactor/v1.5-maintainability`: the complete maintainability refactor history.
- `v1.5`: the squashed refactor checkpoint on `main`.

Stage 2 through Stage 5 are described in the existing curriculum, but their implementation branches and tags are not present in the current local or remote Git refs. This book therefore documents their current status without inventing implementation history.

## Local reading

Install and serve the book with:

```bash
cargo install mdbook
mdbook serve docs
```

If port `3000` is already occupied or the browser shows a blank page, run the server on an explicit IPv4 address and alternate port:

```bash
mdbook serve docs --hostname 127.0.0.1 --port 3001 --open
```
