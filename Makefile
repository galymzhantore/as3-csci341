.PHONY: help install db-local db-docker part1 part2 part3 clean docker-start docker-stop

help:
	@echo "Caregivers Platform - Available Commands:"
	@echo ""
	@echo "  make install      - Install Python dependencies"
	@echo "  make db-local     - Create database (local PostgreSQL)"
	@echo "  make db-docker    - Create database (Docker PostgreSQL)"
	@echo "  make part1        - Import database schema and data"
	@echo "  make part2        - Run SQLAlchemy queries"
	@echo "  make part3        - Run Flask web application"
	@echo "  make docker-start - Start Docker PostgreSQL container"
	@echo "  make docker-stop  - Stop Docker PostgreSQL container"
	@echo "  make clean        - Remove Python cache files"
	@echo ""

install:
	pip install -r requirements.txt

db-local:
	createdb caregivers_platform
	psql caregivers_platform < caregivers_platform_part1.sql

db-docker:
	docker exec -it postgres-csci341 createdb -U postgres caregivers_platform
	docker exec -i postgres-csci341 psql -U postgres caregivers_platform < caregivers_platform_part1.sql

part1:
	psql caregivers_platform < caregivers_platform_part1.sql

part2:
	python3 caregivers_platform_part2.py

part3:
	python3 app.py

docker-start:
	docker run --name postgres-csci341 \
		-e POSTGRES_PASSWORD=postgres \
		-e POSTGRES_USER=postgres \
		-p 5432:5432 \
		-d postgres:latest

docker-stop:
	docker stop postgres-csci341
	docker rm postgres-csci341

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
