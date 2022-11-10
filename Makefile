env:
	cp .env.example .env

run:
	poetry run python3 -m app

build:
	docker build . -t str1kez/marks_bot:latest

up:
	docker run --name marks_bot  --env-file=.env -d --rm str1kez/marks_bot

down:
	docker container rm -f marks_bot

format:
	poetry run black .
	poetry run isort .
