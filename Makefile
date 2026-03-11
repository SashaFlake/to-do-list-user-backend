.PHONY: dev lint test migrate

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check . && mypy src

test:
	pytest tests/ -v

migrate:
	alembic upgrade head

migrate-auto:
	alembic revision --autogenerate -m "$(msg)"
