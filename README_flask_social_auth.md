# Flask Social Login with GitHub, Google OAuth, and Private User Registration/Login

## Overview of Project Structure

This project is a Flask-based web application that enables social login via GitHub and Google OAuth, as well as private user registration and login. The project is organized into several files and directories, each playing a specific role in the functionality.

### 1. Project Structure
- **flask_social_auth (main directory)**
  - **app (directory)**
    - **templates (directory)**
      - `_base.html`
      - `index.html`
    - **forms.py** (Flask-WTF form definitions for user registration and login)
    - **auth.py** (handles private user authentication, registration, and OAuth login routes)
    - `__init__.py`
    - `models.py`
    - `oauth.py`
  - `.env` (environment variables file)
  - `main.py`
  - `requirements.txt` (list of dependencies)

## File-by-File Explanation

### 1. `main.py`
- **Purpose**: This is the main entry point of your application.
- **Key Points**:
  - **Load Environment Variables**: Using `dotenv`, it loads sensitive data like `SECRET_KEY`, `GITHUB_ID`, `GOOGLE_CLIENT_ID`, and database URI from the `.env` file.
  - **Create Flask App**: It calls `create_app()` from `app/__init__.py` to create a Flask application.
  - **Register Blueprints**: The GitHub OAuth blueprint (`github_blueprint`), Google OAuth blueprint, and private user authentication blueprint (`auth`) are registered.
  - **Define Routes**: Routes such as `/ping`, `/`, `/github`, `/google`, `/register`, `/login`, and `/logout` handle different parts of the web application.

### 2. `app/__init__.py`
- **Purpose**: This file initializes the Flask application, sets up configurations, and integrates extensions like SQLAlchemy (for database) and Flask-Login (for managing user sessions).
- **Key Points**:
  - **Create Flask App**: The `create_app()` function initializes the Flask app and configures it with a secret key and database URI.
  - **Initialize Extensions**: `db` (SQLAlchemy), `login_manager` (Flask-Login), and OAuth are initialized with the app.
  - **User Loader**: The `load_user` function is defined to load a user from the database by their ID, which Flask-Login uses to manage logged-in users.

### 3. `app/models.py`
- **Purpose**: This file defines the database models (tables) used in your application.
- **Key Points**:
  - **User Model**: The `User` class represents a user in your database with attributes such as `id`, `username`, `email`, `password_hash`, and OAuth information (for GitHub and Google).
  - **OAuth Model**: The `OAuth` class represents the OAuth token associated with a `User`. This is used to store and retrieve OAuth tokens.
  - **Registration and Authentication**: It includes password hashing and verification methods for private user login.

### 4. `app/oauth.py`
- **Purpose**: This file handles the OAuth setup and login logic using GitHub and Google.
- **Key Points**:
  - **GitHub Blueprint**: The `make_github_blueprint` function creates a blueprint for handling GitHub OAuth.
  - **Google Blueprint**: Similar to GitHub, a blueprint for Google OAuth is created.
  - **Token Storage**: It uses `SQLAlchemyStorage` to store OAuth tokens in the database.
  - **Login Handling**: The `oauth_logged_in` function checks if the user exists in the database; if not, it creates a new user and logs them in.

### 5. `app/auth.py`
- **Purpose**: This file handles private user registration and login.
- **Key Points**:
  - **Registration Route**: Handles user registration, including form validation and saving user data in the database.
  - **Login Route**: Validates user credentials, authenticates, and logs in the user using Flask-Login.

### 6. `app/forms.py`
- **Purpose**: This file defines the Flask-WTF forms used for user registration and login.
- **Key Points**:
  - **Registration Form**: Captures `username`, `email`, and `password` for new users.
  - **Login Form**: Captures `email` and `password` for returning users.

### 7. `app/templates/_base.html`
- **Purpose**: This is the base HTML template that other templates will extend.
- **Key Points**:
  - **Bootstrap & Font Awesome**: It includes links to Bootstrap and Font Awesome for styling.
  - **Content Block**: The `{% block content %}{% endblock content %}` allows other templates to insert their content into this base structure.

### 8. `app/templates/index.html`
- **Purpose**: This is the main page template that users will see when they visit your site.
- **Key Points**:
  - **Extends `_base.html`**: It extends the base template and fills in the content block.
  - **Conditional Display**: It shows different content based on whether the user is logged in (`current_user.is_authenticated`). If logged in, it shows a logout button; otherwise, it shows options for "Login with GitHub", "Login with Google", and private login options.

## How the Application Works

### 1. Application Initialization
- When you run `main.py`, it calls `create_app()` from `app/__init__.py` to initialize the Flask application.
- The app is configured with necessary extensions like SQLAlchemy for database interactions and Flask-Login for managing user sessions.

### 2. OAuth Setup
- `oauth.py` sets up the GitHub and Google OAuth using the `make_github_blueprint` and `make_google_blueprint` functions.
- OAuth tokens are stored in the database using `SQLAlchemyStorage`.

### 3. User Authentication (OAuth and Private)
- OAuth: When a user clicks the "Login with GitHub" or "Login with Google" buttons, they are redirected to the respective OAuth provider for authentication. After a successful login, the user is either loaded from the database or a new user is created, then logged in.
- Private: Users can register with a username, email, and password. After registration, they can log in with their credentials, and sessions are managed via Flask-Login.

### 4. Routing
- `/`: Renders the `index.html` template.
- `/github`: Handles GitHub login logic.
- `/google`: Handles Google login logic.
- `/register`: Renders the registration form and processes registration.
- `/login`: Renders the login form and handles login.
- `/logout`: Logs the user out and redirects to the homepage.

## How to Run the Application

### 1. Set Up Environment
- Create a `.env` file with the necessary environment variables like:
  ```bash
  SECRET_KEY=your_secret_key
  SQLALCHEMY_DATABASE_URI=your_database_uri
  GITHUB_ID=your_github_client_id
  GITHUB_SECRET=your_github_client_secret
  GOOGLE_CLIENT_ID=your_google_client_id
  GOOGLE_CLIENT_SECRET=your_google_client_secret

# Flask Application Setup and Usage Guide

## 1. Install Dependencies

Install dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt

```
# Run application
```bash
venv\Scripts\activate
python main.py

```

# Database migrations
```bash
flask db init
flask db migrate -m "Add new fields for OAuth and user registration"
flask db upgrade
```




