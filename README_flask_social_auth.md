mysql run is in creds file

venv\Scripts\activate



# Flask Social Login with GitHub

## Overview of Project Structure

This project is a Flask-based web application that enables social login via GitHub. The project is organized into several files and directories, each playing a specific role in the functionality. Here's a breakdown of what each file does and how they work together:

### 1. Project Structure
- **flask_social_auth (main directory)**
  - **app (directory)**
    - **templates (directory)**
      - `_base.html`
      - `index.html`
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
  - **Load Environment Variables**: Using `dotenv`, it loads sensitive data like `SECRET_KEY` and database URI from the `.env` file.
  - **Create Flask App**: It calls `create_app()` from `app/__init__.py` to create a Flask application.
  - **Register GitHub Blueprint**: The GitHub OAuth blueprint (`github_blueprint`) from `oauth.py` is registered to handle GitHub login.
  - **Define Routes**: Several routes are defined (`/ping`, `/`, `/github`, and `/logout`) to handle different parts of your web application.

### 2. `app/__init__.py`
- **Purpose**: This file initializes the Flask application, sets up configurations, and integrates extensions like SQLAlchemy (for database) and Flask-Login (for managing user sessions).
- **Key Points**:
  - **Create Flask App**: The `create_app()` function initializes the Flask app and configures it with a secret key and database URI.
  - **Initialize Extensions**: `db` (SQLAlchemy) and `login_manager` (Flask-Login) are initialized with the app.
  - **User Loader**: The `load_user` function is defined to load a user from the database by their ID, which Flask-Login uses to manage logged-in users.

### 3. `app/models.py`
- **Purpose**: This file defines the database models (tables) used in your application.
- **Key Points**:
  - **User Model**: The `User` class represents a user in your database with an `id` and `username`.
  - **OAuth Model**: The `OAuth` class represents the OAuth token and is associated with a `User`. This is used to store and retrieve OAuth tokens.

### 4. `app/oauth.py`
- **Purpose**: This file handles the OAuth setup and login logic using GitHub.
- **Key Points**:
  - **GitHub Blueprint**: The `make_github_blueprint` function creates a blueprint for handling GitHub OAuth. This blueprint is registered in `main.py`.
  - **Token Storage**: It uses `SQLAlchemyStorage` to store OAuth tokens in the database.
  - **Login Handling**: The `github_logged_in` function is connected to the OAuth event that occurs when a user logs in via GitHub. It checks if the user exists in the database; if not, it creates a new user and logs them in.

### 5. `app/templates/_base.html`
- **Purpose**: This is the base HTML template that other templates will extend.
- **Key Points**:
  - **Bootstrap & Font Awesome**: It includes links to Bootstrap and Font Awesome for styling.
  - **Content Block**: The `{% block content %}{% endblock content %}` allows other templates to insert their content into this base structure.

### 6. `app/templates/index.html`
- **Purpose**: This is the main page template that users will see when they visit your site.
- **Key Points**:
  - **Extends `_base.html`**: It extends the base template and fills in the


  content block.
  - **Conditional Display**: It shows different content based on whether the user is logged in (`current_user.is_authenticated`). If they are logged in, it shows a logout button; otherwise, it shows a "Login with GitHub" button.

## How the Application Works

### 1. Application Initialization
- When you run `main.py`, it calls `create_app()` from `app/__init__.py` to initialize the Flask application.
- The app is configured with necessary extensions like SQLAlchemy for database interactions and Flask-Login for managing user sessions.

### 2. OAuth Setup
- `oauth.py` sets up the GitHub OAuth using the `make_github_blueprint` function, allowing users to log in with their GitHub accounts.
- The OAuth tokens are stored in the database using `SQLAlchemyStorage`.

### 3. User Authentication
- When a user clicks the "Login with GitHub" button on `index.html`, they are redirected to GitHub for authentication.
- After a successful login, the `github_logged_in` function in `oauth.py` checks if the user exists in the database. If not, a new user is created.
- The user is then logged in, and their session is managed by Flask-Login.

### 4. Routing
- `/`: Renders the `index.html` template.
- `/github`: Handles GitHub login logic.
- `/logout`: Logs the user out and redirects to the homepage.

## How to Run the Application

### 1. Set Up Environment
- Create a `.env` file with the necessary environment variables like `SECRET_KEY`, `GITHUB_ID`, and `GITHUB_SECRET`.
- Install dependencies from `requirements.txt`.

### 2. Run the Application
- In the terminal, navigate to your project directory and run `python main.py`.
- Visit `http://127.0.0.1:5000/` in your browser to see the application in action.

This explanation should help you get back on track with your project!

if any db changes needed , we need to update the modules and run the below migrsate comand
flask db init
flask db migrate -m "update the nullable value as false for both google and github"
flask db upgrade

