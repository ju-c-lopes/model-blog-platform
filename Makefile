build:
	docker compose \
	--env-file .env.dev \
	-f docker-compose.yml \
	-f docker-compose.dev.yml \
	build

up:
	docker compose \
	--env-file .env.dev \
	-f docker-compose.yml \
	-f docker-compose.dev.yml \
	up

run-dev:
	docker compose exec python-app poetry run python manage.py runserver 0.0.0.0:8000

down:
	docker compose \
	--env-file .env.dev \
	-f docker-compose.yml \
	-f docker-compose.dev.yml \
	down

prod-build:
	docker compose \
	--env-file .env.prod \
	-f docker-compose.yml \
	-f docker-compose.prod.yml \
	build --no-cache

prod-down:
	docker compose \
	--env-file .env.prod \
	-f docker-compose.yml \
	-f docker-compose.prod.yml \
	down --remove-orphans

prod:
	docker compose \
	--env-file .env.prod \
	-f docker-compose.yml \
	-f docker-compose.prod.yml \
	up -d --force-recreate

status:
	docker compose ps

logs:
	docker compose logs -f

shell:
	docker compose exec python-app bash

migrate:
	docker compose exec python-app poetry run python manage.py migrate

collectstatic:
	docker compose exec python-app poetry run python manage.py collectstatic

django-shell:
	docker compose exec python-app poetry run python manage.py shell

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build         Build the development environment"
	@echo "  up            Start the development environment"
	@echo "  down          Stop containers"
	@echo "  prod          Build the production environment"
	@echo "  prod-build    Build the production environment"
	@echo "  status        Show status of the services"
	@echo "  logs          Show logs of the services"
	@echo "  shell         Open a shell in the python-app container"
	@echo "  migrate       Run Django migrations"
	@echo "  collectstatic Run Django collectstatic"
	@echo "  django-shell  Open a Django shell in the python-app container"
	@echo "  run-dev       Run Django development server"
