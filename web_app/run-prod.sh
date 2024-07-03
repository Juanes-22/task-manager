#!/bin/bash

export FLASK_ENV=production

echo "Setting up virtual environment..."
poetry install --without dev

echo "Running database migrations..."
poetry run flask db upgrade

echo "Starting Gunicorn server..."
poetry run gunicorn src.wsgi:app --bind 0.0.0.0:5000 --workers 4
