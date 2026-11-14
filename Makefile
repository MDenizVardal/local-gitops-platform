.PHONY: test lint fmt

test:
	cd app && uv run pytest

lint:
	cd app && uv run ruff check . && uv run ruff format --check .

fmt:
	cd app && uv run ruff format . && uv run ruff check --fix .
