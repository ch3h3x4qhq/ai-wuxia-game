.PHONY: dev test fmt lint typecheck

dev:
uvicorn app.main:app --reload

test:
pytest

fmt:
ruff check --fix .
black .

lint:
ruff check .

typecheck:
mypy app
