start-dev:
	docker-compose -f docker-compose.local.yaml up --build
prod:
	docker-compose -f docker-compose.test.yaml up --build
drop_db:
	docker-compose down
	# if you already renamed the project, sub dj_starter_pack_ with the name of the root directory
	docker volume rm dj_starter_pack_pgdata
venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt