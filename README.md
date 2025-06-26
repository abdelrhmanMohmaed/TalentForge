# TalentForge

This repository contains the backend API for the TalentForge project, built with Django and Django REST Framework. It provides user management functionalities, including user creation, authentication (JWT), and the ability to assign roles and projects during user registration.

---

## Features

- **Custom User Model**: Supports a custom user model with fields like `EED`, `email`, `name`, `department`, `job_title`, and `location`.
- **Role and Project Management**: Defines `Role` and `Project` models, allowing for flexible assignment of roles (e.g., admin, mentor, mentee) and associating users with specific projects.
- **User Registration**: Allows new user creation via API, with integrated role and project assignment.
- **JWT Authentication**: Secure user authentication using JSON Web Tokens (JWT) through `djangorestframework-simplejwt` and `Djoser`.

---

## API Endpoints

| Function                         | Endpoint                        | Method     |
|----------------------------------|----------------------------------|------------|
| Home Endpoint                    | `/`                              | GET        |
| User Registration                | `/auth/users/`                   | POST       |
| User Login (JWT)                | `/auth/jwt/create/`             | POST       |
| List/Create Roles (Admin only)  | `/api/roles/`                    | GET/POST   |
| List/Create Projects (Admin only) | `/api/projects/`              | GET/POST   |

---

## Setup and Installation

### 1. Prerequisites

- Python 3.8+ (preferably 3.10+)
- PostgreSQL database server
- `pipenv` for dependency management

---

### 2. Clone the Repository

```bash
git clone https://github.com/abdelrhmanMohmaed/TalentForge
cd TalentForge
``` 

---

### 3. Install Dependencies

```bash
pipenv install
``` 

---

### 4. Database Configuration

- Create a PostgreSQL database (e.g., mento_hub) and user
- Edit config/settings.py:

```bash
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mento_hub",
        "USER": "postgres",
        "PASSWORD": "your_db_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
``` 
- ✅ Make sure PostgreSQL is running on port 5432.

### 5. Run Migrations

```bash
pipenv run python manage.py migrate
``` 

### 6. Create a Superuser

```bash
pipenv run python manage.py createsuperuser
``` 
- Follow the prompts to enter email & password.

### 7. Populate Initial Data

#### Option A: Using Django Admin

Add this to `users/admin.py`:

```python
admin.site.register(Role)
admin.site.register(Project)
```

Run the development server:
```python
pipenv run python manage.py runserver
```
http://127.0.0.1:8000/admin/




