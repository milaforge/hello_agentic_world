.PHONY: test

test:
	uv run pytest

run:
	uv run hello-agent "How many Python files exist under workspace/" --debug --workspace workspace

eval:
	uv run python evals/run.py --verbose

book:
	mdbook serve docs 