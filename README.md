# Planetarium API

A Django REST Framework API for an online planetarium ticket booking system.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Running with Docker](#running-with-docker)
  - [Manual Setup (Optional)](#manual-setup-optional)
- [API Endpoints](#api-endpoints)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)

## Features

- User registration and JWT-based authentication.
- Management of:
  - Astronomy Shows and Show Themes
  - Planetarium Domes
  - Show Sessions
  - Reservations (Bookings)
  - Tickets
  - Users
- API documentation using Swagger and ReDoc.
- Dockerized for easy deployment and development.
- Initial data loading for quick setup.

## Technologies Used

- **Backend:** Python 3.12, Django 4.2, Django REST Framework
- **Database:** PostgreSQL (configured for Docker), SQLite (for local development if not using Docker)
- **Authentication:** JSON Web Tokens (JWT) via `djangorestframework-simplejwt`
- **API Documentation:** `drf-yasg` (Swagger/OpenAPI, ReDoc)
- **Containerization:** Docker, Docker Compose
- **Linters & Formatters:** `black`, `flake8`, `isort`
- **Testing:** `pytest`, `pytest-django`
- **Other Key Libraries:** `django-filter`, `psycopg2-binary`

## Project Structure

The project follows a standard Django app structure:

```
Planetarium-api/
├── bookings/           # Handles reservations/bookings
├── config/             # Project-wide settings and main URL configuration
├── domes/              # Manages planetarium domes
├── show_sessions/      # Manages show sessions
├── shows/              # Manages astronomy shows and themes
├── templates/          # HTML templates (e.g., for the home page)
├── tests/              # Contains automated tests
├── tickets/            # Manages tickets
├── users/              # Custom user model and user-related endpoints
├── venv/               # Virtual environment (if used locally)
├── .dockerignore
├── .env                # Environment variables (local, gitignored)
├── .env.example        # Example environment variables
├── .gitignore
├── db.sqlite3          # Default SQLite database (if not using PostgreSQL)
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker image build instructions
├── initial_data.json   # Initial data for the database
├── manage.py           # Django's command-line utility
├── README.md
└── requirements.txt    # Python dependencies
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed.
- Git (for cloning the repository).

### Running with Docker (Recommended)

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Planetarium-api
    ```

2.  **Create environment file:**
    Copy the example environment file and customize it if needed (e.g., for `SECRET_KEY` in production). For development, the defaults in `.env.example` and `docker-compose.yml` should work.

    ```bash
    cp .env.example .env
    ```

3.  **Build and run the services:**

    ```bash
    docker-compose up --build
    ```

    This command will:

    - Build the Docker image for the `web` service (Django application).
    - Start the `web` service and the `db` service (PostgreSQL).
    - Apply database migrations.
    - Load initial data from `initial_data.json`.
    - Start the Django development server on `http://localhost:8000`.

4.  **Access the application:**

    - API: `http://localhost:8000/api/`
    - Admin Panel: `http://localhost:8000/admin/` (you'll need to create a superuser first, see below)
    - API Docs (Swagger): `http://localhost:8000/api/docs/`
    - API Docs (ReDoc): `http://localhost:8000/api/redoc/`

5.  **Create a superuser (optional, for admin panel access):**
    Open another terminal and run:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

    Follow the prompts to create an admin user.

6.  **Stopping the application:**
    Press `Ctrl+C` in the terminal where `docker-compose up` is running, then:
    ```bash
    docker-compose down
    ```
    To remove volumes (and lose PostgreSQL data):
    ```bash
    docker-compose down -v
    ```

### Manual Setup (Optional)

This setup is for development without Docker.

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Planetarium-api
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create environment file:**
    Copy `.env.example` to `.env` and configure it. You might need to adjust `DATABASES` settings in `config/settings.py` if you are not using the default PostgreSQL connection from `docker-compose.yml` (e.g., to use `db.sqlite3`).

5.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Load initial data (optional):**

    ```bash
    python manage.py loaddata initial_data.json
    ```

7.  **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The API provides endpoints for managing various resources of the planetarium system. Key base URLs for registered ViewSets:

- `/api/astronomy-shows/`
- `/api/show-themes/`
- `/api/planetarium-domes/`
- `/api/show-sessions/`
- `/api/reservations/`
- `/api/tickets/`
- `/api/users/`

Authentication endpoints:

- `/api/token/` (POST): Obtain JWT access and refresh tokens.
- `/api/token/refresh/` (POST): Refresh JWT access token.

For detailed information on all available endpoints, request/response formats, and parameters, please refer to the API documentation.

## API Documentation

Interactive API documentation is available through:

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`

These interfaces allow you to explore and interact with the API endpoints in real-time.

## Running Tests

To run the test suite:

1.  **If using Docker:**
    Ensure your containers are running (`docker-compose up`). Then, in a new terminal:

    ```bash
    docker-compose exec web pytest
    ```

2.  **If running manually (with virtual environment activated):**
    ```bash
    pytest
    ```

This will execute all tests defined in the `tests/` directory and within individual app directories.

Diagrams
https://prnt.sc/KKHEcBDiPVLO
