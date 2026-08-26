SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


PYTHON_VERSION = 3.9
DOCKER_TAG = obp-next

PORT_BE = 5000
PORT_FE = 3000


#######################################################################
# setup
#######################################################################
.PHONY: setup
setup:
	mkdir -p data/db && mkdir -p data/media
	uv sync --python ${PYTHON_VERSION}
	bun install
	@if [ ! -f .env ]; then \
		echo "adding .env"; \
		cp .env.example .env; \
	fi


#######################################################################
# lint & format
#######################################################################
.PHONY: lint-be
lint-be:
	uv run ruff format --check .
	uv run ruff check --output-format concise .

.PHONY: format-be
format-be:
	uv run ruff format .
	uv run ruff check --fix .
	uv run djhtml --tabwidth 2 core/templates/

.PHONY: lint-fe
lint-fe:
	npx stylelint "./obp_ui/**/*.(scss|js|vue)"
	npx eslint ./obp_ui/ --ext .js --ext .vue

.PHONY: format-fe
format-fe:
	npx stylelint "./obp_ui/**/*.(scss|js|vue)" --fix
	npx eslint ./obp_ui/ --ext .js --ext .vue --fix

.PHONY: lint
lint: lint-be lint-fe

.PHONY: format
format: format-be format-fe


#######################################################################
# test
#######################################################################
.PHONY: test-be
test-be:
	uv run pytest -m "not e2e" -s obp_core/tests/

.PHONY: test
test: test-be


#######################################################################
# build
#######################################################################
.PHONY: build-fe
build-fe:
	bun run build

#######################################################################
# run
#######################################################################
.PHONY: run-be
run-be:
	uv run ./manage.py runserver 0.0.0.0:${PORT_BE}

.PHONY: run-celery
run-celery:
	uv run celery -A config.celery_app worker -B -l info

.PHONY: run-fe
run-fe:
	bun run dev --port ${PORT_FE}

.PHONY: compose-up
compose-up:
	docker compose -f ./devsupport/compose.yml up --build
	docker compose -f ./devsupport/compose.yml down
