.PHONY: test

test:
	uv run pytest

run:
	uv run hello-agent "How many Python files exist under workspace/" --debug --workspace workspace
