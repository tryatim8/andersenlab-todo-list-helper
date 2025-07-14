# ✅ Task Manager API with Django REST Framework

<em>Secure and test-covered REST API for managing personal task lists, with JWT authentication and PostgreSQL backend.</em><br>
<em>Final technical assignment developed using Django and DRF.</em>

<p align="center">
  <img width="220" src="https://static.andersenlab.com/andersenlab/new-andersensite/logos/andersen-preview-image.png" alt="Andersen Logo">
</p>

[![Python Version](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.2.3-green)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/DRF-3.16.0-teal)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![JWT Auth](https://img.shields.io/badge/Auth-JWT-orange)](https://github.com/jazzband/djangorestframework-simplejwt)
[![Testing](https://img.shields.io/badge/Pytest-8.4.1-green)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen.svg)](#)
[![Linting](https://img.shields.io/badge/Linters-flake8%20%7C%20mypy%20%7C%20isort-black)](https://flake8.pycqa.org/)
[![Docs](https://img.shields.io/badge/API--Docs-Swagger%20%7C%20Redoc-blue)](https://swagger.io/)

---

## ✨ Features

- ✅ JWT-based user authentication and registration
- 📋 Full CRUD operations on tasks
- 🔐 Task ownership control (only owners can modify/delete)
- 🔎 Filtering tasks by status (`New`, `In Progress`, `Completed`)
- ✅ Mark tasks as completed via a special endpoint
- 📄 Pagination support for task lists
- 🧪 Extensive API testing with Pytest
- ⚙️ Admin panel with superuser access
- 📦 Dockerized project setup
- 📚 Fully documented OpenAPI schema via Swagger & Redoc

---

## 🚀 Quickstart

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/andersenlab-todo-list-helper.git
cd andersenlab-todo-list-helper
```

### 2. Configure environment

Copy and edit the environment template:

```bash
cp .env.template .env
# Then manually update secrets and passwords in .env
```

### 3. Build and run with Docker Compose:

```bash
docker compose up --build
```
> All dependencies will be installed inside the containers.
> The application runs with Gunicorn as the WSGI HTTP server inside the container automatically.
> The database migrations will be applied inside the container at startup.

### Available endpoints after startup:

- 🏠 API root: [http://localhost:8000/api/](http://localhost:8000/api/)
- 🔐 Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)  
  (default credentials: `admin` / `admin`)
- 📘 Swagger UI: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)
- 📕 Redoc UI: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## 👤 Authentication

Authentication is handled via **JWT tokens**.

### Register a new user (authentication is not required)

```http
POST /api/users/register/
```

### Login (obtain token pair)

```http
POST /api/token/
```

### Refresh access token

```http
POST /api/token/refresh/
```

Include `Authorization: Bearer <access_token>` in all protected requests.

---

## 🔁 Task API Overview

| Method | Endpoint                          | Description                 |
|--------|-----------------------------------|-----------------------------|
| GET    | `/api/tasks/all/`                 | List all tasks (staff only) |
| GET    | `/api/tasks/`                     | List current user’s tasks   |
| GET    | `/api/tasks/{id}/`                | Retrieve specific task      |
| POST   | `/api/tasks/`                     | Create new task             |
| PUT    | `/api/tasks/{id}/`                | Change task (only by owner) |
| PATCH  | `/api/tasks/{id}/`                | Update task (only by owner) |
| DELETE | `/api/tasks/{id}/`                | Delete task (only by owner) |
| POST   | `/api/tasks/{id}/mark_completed/` | Mark task as completed      |

#### Pagination and Filtering example:

```http
GET /api/tasks/?page=2&status=in_progress
```

---

## 🧪 Testing

Run the test suite with:

```bash
pytest myproject/
```

Test coverage includes:

- ✅ User registration and auth
- ✅ Task CRUD operations
- ✅ Permissions (owner-only)
- ✅ Filtering and pagination
- ✅ Token access

---

> Optionally, you can generate HTML coverage reports using `coverage`:

```bash
coverage run -m pytest
coverage html
```

---

## 🧰 Tech Stack

- `Django 5.2.3` — Web framework
- `Django REST Framework 3.16.0` — REST API toolkit
- `PostgreSQL 16` — Relational DBMS
- `Docker + Docker Compose` — Containerization
- `JWT` — Authentication via SimpleJWT
- `drf-spectacular` — OpenAPI schema generation
- `Pytest` + `pytest-django` — Unit testing
- `flake8`, `isort`, `mypy` — Linting and static typing
- `Faker` — Generating test data

---

## 📁 Project Structure

```bash
andersenlab-todo-list-helper/
├── myproject/
│   ├── users/             # Custom user model and auth
│   ├── tasks/             # Task models, views, serializers
│   ├── tests/             # Test suite
│   ├── mysite/            # Project settings
│   ├── fixtures/          # Predefined test data
│   └── manage.py
├── fixtures.json          # Example data for local dev
├── Dockerfile             # Backend Dockerfile
├── docker-compose.yaml    # Compose configuration
├── .env.template          # Example env config
├── pyproject.toml         # Poetry dependencies
├── README.md
```

---

## 🎯 Project Goals

This API project was developed as a technical task for a Junior Python Developer position at Andersen Lab.

Covered objectives:

- ✅ REST API with secure authentication
- ✅ PostgreSQL integration
- ✅ Full test coverage and linters
- ✅ Docker-ready deployment
- ✅ Clear README and Swagger/OpenAPI documentation

---

## 👤 Author

**Timofey Prokofyev**  
📧 [tryatim8@mail.ru](mailto:tryatim8@mail.ru)  
💼 [GitHub](https://github.com/tryatim8)