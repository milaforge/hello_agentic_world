.PHONY: test

test:
	uv run pytest

run:
	uv run hello-agent "How many Python files exist under workspace/" --debug --workspace workspace

eval:
	uv run python evals/run.py --verbose

book:
	mdbook serve docs --hostname 127.0.0.1 --port 3000