.PHONY: run
run:
	cd ./django_core && gunicorn django_core.wsgi:application --bind 0.0.0.0:8000 --reload


.PHONY: run_docker_backend
run_docker_backend:
	pip freeze >> ./django_core/requirements.txt && docker-compose up backend

