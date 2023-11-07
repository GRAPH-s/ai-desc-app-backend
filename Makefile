.PHONY: run
run:
	cd ./django_core && gunicorn django_core.wsgi:application --bind 0.0.0.0:8000 --reload
