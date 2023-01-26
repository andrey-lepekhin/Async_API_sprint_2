first_run:
	#Команда для первого запуска
	cp .env.example .env
	cp .docker.env.example .docker.env
	cp .env.example tests/.env
	cp .docker.env.example tests/.docker.env
	docker-compose -f docker-compose.yml -f docker-compose.etl.yml up --build -d

run:
	#Команда для запуска контейнеров в фоне
	docker-compose -f docker-compose.yml -f docker-compose.etl.yml up -d

generate_data:
	#Generate fake data and push to ES
	docker-compose exec etl python etl/postgres_to_es/generate_fake_data.py

postgresql:
	#Запуск консоли для управления postgresql-контейнером.
	docker-compose exec postgres bash

elasticsearch:
	#Запуск консоли для управления elasticsearch-контейнером.
	docker-compose exec elasticsearch bash

etl:
	#Запуск консоли для управления etl-контейнером.
	docker-compose exec etl bash

redis:
	#Запуск консоли для управления redis-контейнером.
	docker-compose exec redis bash

shows_async:
	#Запуск консоли для управления async-контейнером.
	docker-compose exec async_api bash

stop:
	#Остановка и удаление контейнеров, запущенных docker-compose up.
	docker-compose down

run_docker_tests_interactive:
	# Build and spin up main services, and run all tests interactively
	unzip -o ./tests/functional/testdata/indexes_snapshot.zip -d ./tests/functional/testdata/
	docker-compose -f docker-compose.yml -f tests/docker-compose.yml -f tests/docker-compose.tests.yml up --build

run_docker_test_containers:
	# Build and spin up main services with open external ports.
	# Use when you want to run tests locally of debug services directly
	unzip -o ./tests/functional/testdata/indexes_snapshot.zip -d ./tests/functional/testdata/
	docker-compose -f docker-compose.yml -f tests/docker-compose.yml up --build -d