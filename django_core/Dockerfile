FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./ ./

RUN pip install -r requirements.txt

CMD ["gunicorn", "django_core.wsgi:application", "--bind 0.0.0.0:8000", "--reload"]