first_run:
	#Команда для первого запуска
	cp .env.example fastapi-solution/src/core/.env
	cp fastapi-solution/src/etl/postgres_to_es/.env
	docker-compose up --build -d

run:
	#Команда для сборки и запуска контейнеров
	docker-compose up --build -d

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
