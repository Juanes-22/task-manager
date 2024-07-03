# Task Management System
![task-manager-dashboard](https://github.com/Juanes-22/task-manager/assets/91810892/5ff0ee23-3059-462e-a3ee-4e4fd0ca9cd3)

## Overview

This project is a simple web application for a task management system. The application allows users to create, view, and delete tasks. The frontend is built using Flask and Bootstrap, while the backend uses Flask and PostgreSQL. The entire application is containerized using Docker.

## Installation

### Prerequisites

- Python and pip installed on your machine (for running locally).
- Docker and Docker Compose installed on your machine (for running with Docker).

### Setup

#### Running with Docker Compose

1. **Clone the repository**

   ```bash
   git clone https://juanesgarciamar@dev.azure.com/juanesgarciamar/task-manager/_git/task-manager
   cd task-manager
   ```

2. **Set up environment variables**

   Create a `.env` file in the root directory and add the following variables:

   ```env
    DB_NAME=task_manager_db
    DB_USER=postgres
    DB_PASSWORD=1234
    SECRET_KEY=my-super-secret-key
    JWT_SECRET_KEY=my-super-secret-key
   ```

3. **Build and run the Docker containers**

   ```bash
   docker compose up --build
   ```

   This will build the Docker images and start the containers for the web application and the PostgreSQL database.

4. **Access the application**

   Open your web browser and navigate to `http://localhost:8000`.

#### Running Locally

1. **Clone the repository**

   ```bash
   git clone https://juanesgarciamar@dev.azure.com/juanesgarciamar/task-manager/_git/task-manager
   cd task-manager/web_app
   ```

2. **Set up a PostgreSQL instance**

   You can either install PostgreSQL locally or run a PostgreSQL container using Docker.

3. **Set up environment variables**

   Create a `.env` file in the root directory and add the following variables:

   ```env
    DATABASE_URL=postgresql://postgres:1234@localhost:5432/task_manager_db
    SECRET_KEY=my-super-secret-key
    JWT_SECRET_KEY=my-super-secret-key
   ```

4. **Install dependencies**

   You can install dependencies using `pip` or `poetry`.

   **Using pip:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Using Poetry:**

   ```bash
   poetry install
   ```

5. **Run the Flask application**

   ```bash
   flask run
   ```

6. **Access the application**

   Open your web browser and navigate to `http://localhost:5000`.

## Directory Structure

### Root Project Structure

```
task-manager/
│
├── README.md
├── azure-pipelines.yml
├── build.sh
├── docker-compose.yml
└── web_app/...
```

### Flask Web App Structure

```
web_app/
│
├── Dockerfile
├── migrations/...
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── run-local.sh
├── run-prod.sh
└── src/
    ├── app/
    │   ├── __init__.py
    │   ├── auth/
    │   │   ├── constants.py
    │   │   ├── decorators.py
    │   │   ├── forms.py
    │   │   ├── helpers.py
    │   │   ├── models.py
    │   │   ├── routes.py
    │   │   ├── schemas.py
    │   │   ├── services.py
    │   │   └── views.py
    │   ├── commands.py
    │   ├── common/
    │   │   ├── error_handlers.py
    │   │   ├── exceptions.py
    │   │   └── helpers.py
    │   ├── config.py
    │   ├── constants/
    │   │   └── http_status_codes.py
    │   ├── extensions.py
    │   ├── static/...
    │   ├── tasks/
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── routes.py
    │   │   ├── schemas.py
    │   │   ├── services.py
    │   │   └── views.py
    │   └── templates/...
    └── wsgi.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
