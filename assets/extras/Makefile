start-dev:
	docker-compose -f docker-compose.local.yaml up --build
prod:
	docker-compose -f docker-compose.test.yaml up --build

get-env:
	# fetch env file from github secrets... or maybe gcloud..?

push-env:
	# push env file to github secrets... or maybe gcloud..?

requirements:
	pip install -r requirements.txt

dev-requirements:
	pip install -r requirements.dev.txt

docker-dependencies:
	# docker-compose

project-dependencies:
	# postgresql
	# redis
