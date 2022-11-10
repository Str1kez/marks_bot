env:
	cp .env.example .env

run:
	poetry run python3 -m app

format:
	poetry run black .
	poetry run isort .
