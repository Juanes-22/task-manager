FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install dos2unix libpq-dev gcc

RUN pip install poetry==1.8.2

COPY . .

EXPOSE 5000

COPY run-prod.sh .
RUN dos2unix run-prod.sh && chmod +x run-prod.sh

ENTRYPOINT ["./run-prod.sh"]
