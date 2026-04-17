SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

DOCKER_TAG = obp-next

PORT_BE = 5000
PORT_FE = 3000

.PHONY: lint
lint:
	npx stylelint "./obp_ui/**/*.(scss|js|vue)"
	npx eslint ./obp_ui/ --ext .js --ext .vue

.PHONY: fix
fix:
	npx stylelint "./obp_ui/**/*.(scss|js|vue)" --fix
	npx eslint ./obp_ui/ --ext .js --ext .vue --fix


.PHONY: run-be
run-be:
	uv run ./manage.py runserver 0.0.0.0:${PORT_BE}

.PHONY: run-fe
run-fe:
	bun run dev --port ${PORT_FE}

.PHONY: run-celery
run-celery:
	uv run ./manage.py celery worker -l info

.PHONY: compose-up
compose-up:
	docker compose -f ./devsupport/docker-compose.yml up --build
	docker compose -f ./devsupport/docker-compose.yml down
