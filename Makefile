all: black isort flake8 mypy test

black:
	black openslides_backend/ tests/

isort:
	isort --recursive openslides_backend/ tests/

flake8:
	flake8 openslides_backend/ tests/

mypy:
	mypy openslides_backend/ tests/

test:
	pytest

test_all:
	OPENSLIDES_BACKEND_RUN_ALL_TESTS=1 pytest

pip_check:
	pip-check

run-debug:
	OPENSLIDES_BACKEND_DEBUG=1 python -m openslides_backend

docker-build-dev:
	docker build -f Dockerfile-dev . -t openslides_backend_dev

docker-build-prod:
	docker build -f Dockerfile . -t openslides_backend

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))

docker-run-dev-interactive:
	docker run -it -v $(dir $(mkfile_path))openslides_backend:/srv/code/openslides_backend -p 8000:8000 -p 8001:8001 -p 8002:8002 --rm openslides_backend_dev

docker-run-prod:
	docker-compose up -d

docker-stop-prod:
	docker-compose down

docker-run-dev:
	docker-compose -f docker-compose-dev.yml up -d

docker-stop-dev:
	docker-compose down --volumes