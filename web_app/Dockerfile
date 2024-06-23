FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src

EXPOSE 5000

ENV FLASK_APP=src/app
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT [ "run-prod.sh" ]
