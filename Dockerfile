FROM python:3.10
ENV PYTHONUNBUFFERED=1
ENV TZ="Europe/Moscow"
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./src .

CMD wait-for-it -s "${REDIS_HOST}:${REDIS_PORT}" -s "${DB_HOST}:${DB_PORT}" --timeout 10 && gunicorn wsgi_app:app --workers=1 --bind=0.0.0.0:8000 --timeout 600
