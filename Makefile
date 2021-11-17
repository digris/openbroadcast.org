SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

DOCKER_TAG = openbroadcast.org
PORT = 8080

run:
	poetry run ./manage.py runserver 0.0.0.0:$(PORT)

shell:
	poetry run ./manage.py shell

lint:
	npx stylelint "./static/**/*.(scss|js|vue)"
	npx eslint ./static/ --ext .js --ext .vue
	#black ./website/ --check
	#poetry run prospector -p ./website/

fix:
	npx stylelint "./static/**/*.(scss|js|vue)" --fix
	npx eslint ./static/ --ext .js --ext .vue --fix

test:
	pytest --ds app.settings.test --cov=app

compose-up:
	docker-compose -f ./docker/docker-compose.yml up --build
	docker-compose -f ./docker/docker-compose.yml down

build:
	poetry export -f requirements.txt -o requirements.txt
	yarn dist
