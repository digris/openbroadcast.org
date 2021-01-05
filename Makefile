GCP_PROJECT = org-openbroadcast
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
