#!/bin/bash

export FLASK_APP=src/app
export FLASK_ENV=development

echo "Setting up virtual environment..."
poetry install

echo "Running database migrations..."
poetry run flask db upgrade

echo "Starting Flask development server..."
poetry run flask run
