SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


PYTHON_VERSION = 3.9
DOCKER_TAG = obp-next

# runtime runs in docker (devsupport/, single entry point: http://obp-next.local:5000);
# lint, format, tests and lockfiles run on the host
COMPOSE = cd devsupport && docker compose -f compose.yml -f compose.override.yml


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
	uv run djhtml --check --tabwidth 2 obp_core/templates/

.PHONY: format-be
format-be:
	uv run ruff format .
	uv run ruff check --fix .
	uv run djhtml --tabwidth 2 obp_core/templates/

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

.PHONY: test-be-fast
test-be-fast:
	uv run pytest --nomigrations -m "not e2e" obp_core/tests/

.PHONY: test
test: test-be


#######################################################################
# build
#######################################################################
.PHONY: build-fe
build-fe:
	bun run build

#######################################################################
# run (docker compose - see devsupport/README.md)
#######################################################################
.PHONY: up
up:
	$(COMPOSE) up -d --build

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: logs
logs:
	$(COMPOSE) logs -f

.PHONY: ps
ps:
	$(COMPOSE) ps

# usage: make cli ARGS="search_index --create"
ARGS ?=

.PHONY: cli
cli:
	$(COMPOSE) exec core ./cli $(ARGS)
