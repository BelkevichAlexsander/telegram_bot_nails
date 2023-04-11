generate:
	alembic revision --m="Initial migrate" --autogenerate

migrate:
	alembic upgrade head

