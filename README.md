# Planetarium API 
 
A Django REST Framework API for an online planetarium ticket booking system. 
 
 ## Table of Contents
 
- [Features](#features) 
- [Technologies Used](#technologies-used)  
- [Project Structure](#project-structure) 
- [Setup and Installation](#setup-and-installation) 
  - [Prerequisites](#prerequisites) 
  - [Running with Docker](#running-with-docker) 
  - [Manual Setup](#manual-setup) 
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
- **Database:** PostgreSQL (for Docker), SQLite (for local development)
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
├── templates/          # HTML templates 
├── tests/              # Automated tests 
├── tickets/            # Manages tickets 
├── users/              # Custom user model and user-related endpoints 
├── venv/               # Virtual environment (if used locally) 
├── .dockerignore 
├── .env                # Environment variables (local, gitignored) 
├── .env.example        # Example environment variables 
├── .gitignore 
├── db.sqlite3          # SQLite database (if not using PostgreSQL)
├── docker-compose.yml  # Docker Compose configuration 
├── Dockerfile          # Docker image build instructions 
├── initial_data.json   # Initial data for the database 
├── manage.py           # Django's command-line utility 
├── README.md 
└── requirements.txt    # Python dependencies 
``` 
 
## Setup and Installation 
 
### Prerequisites 
 
- Docker and Docker Compose installed .
- Git (for cloning the repository). 
 
### Running with Docker
 
1. **Clone the repository:**
 
   ```bash
   git clone <repository_url>
   cd Planetarium-api
   ```
 
2. **Create environment file:**
   Copy the example environment file and customize it if needed.
 
   ```bash
   cp .env.example .env
   ```
 
3. **Build and run the services:**
 
   ```bash
   docker-compose up --build
   ```
 
   This command:
 
   - Builds the Docker image for the `web` service (Django application).
   - Starts the `web` and `db` (PostgreSQL) services.
   - Applies database migrations.
   - Loads initial data from `initial_data.json`.
   - Starts the Django development server on `http://localhost:8000`.
 
4. **Access the application:**
 
   - API: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`
   - API Docs (Swagger): `http://localhost:8000/api/docs/`
   - API Docs (ReDoc): `http://localhost:8000/api/redoc/`
 
5. **Create a superuser (optional):**
   Open a new terminal and run:
 
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
 
6. **Stopping the application:**
   Press `Ctrl+C` in the terminal where `docker-compose up` is running, then:
   ```bash
   docker-compose down
   ```
   To remove volumes (and lose PostgreSQL data):
   ```bash
   docker-compose down -v
   ```
 
### Manual Setup
 
This setup is for development without Docker. 
 
1. **Clone the repository:**
 
   ```bash
   git clone <repository_url>
   cd Planetarium-api
   ```
 
2. **Create and activate a virtual environment:**
 
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
 
3. **Install dependencies:**
 
   ```bash
   pip install -r requirements.txt
   ```
 
4. **Create environment file:**
   Copy `.env.example` to `.env` and configure it.
 
5. **Apply migrations:**
 
   ```bash
   python manage.py migrate
   ``` 
 
6. **Load initial data (optional):**
 
   ```bash
   python manage.py loaddata initial_data.json
   ``` 
 
7. **Create a superuser (optional):**
 
   ```bash
   python manage.py createsuperuser
   ```
 
8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/`.
 
## API Endpoints 
 
The API provides endpoints for managing various resources of the planetarium system:
 
- `/api/astronomy-shows/` - Astronomy Shows
- `/api/show-themes/` - Show Themes
- `/api/planetarium-domes/` - Planetarium Domes
- `/api/show-sessions/` - Show Sessions
- `/api/reservations/` - Reservations
- `/api/tickets/` - Tickets
- `/api/users/` - Users
 
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
 
1. **If using Docker:**
   Ensure your containers are running (`docker-compose up`). Then, in a new terminal: 
 
   ```bash
   docker-compose exec web pytest
   ```
 
2. **If running manually (with virtual environment activated):**
   ```bash
   pytest
   ```
 
This will execute all tests defined in the `tests/` directory and within individual app directories. 
 