from flask import Flask, jsonify, redirect, render_template, url_for, flash, request
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google
from flask_login import logout_user, login_required, current_user, login_user
from app import create_app, db
from app.models import User  # Import User model
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os
import logging
from flask_wtf.csrf import CSRFProtect
from app.forms import RegistrationForm # Import the RegistrationForm class

# Load environment variables from .env file
load_dotenv()

# Configure SQLAlchemy database URI (before create_app)
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

# Create Flask application instance
app = create_app()

# Set app configuration (if not handled in create_app())
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.secret_key = SECRET_KEY  # Set secret key for sessions

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)
# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG to see all logs
logger = logging.getLogger(__name__)

# Add registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Use the Flask-WTF form
    if current_user.is_authenticated:
        logger.info("User is already authenticated, redirecting to homepage.")
        return redirect(url_for('homepage'))  # Redirect if already logged in

    if form.validate_on_submit():  # Flask-WTF automatically handles CSRF
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        logger.debug(f"Registering user: {username}, email: {email}")  # Debug log

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        try:
            db.session.commit()
            logger.debug(f"User count after registration: {User.query.count()}")
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('register'))
        # Log the successful registration
        logger.info(f"New user registered: {email}")
        
        flash('Registration successful! Please log in.', 'success')
        logger.debug("Redirecting to login page after successful registration.")
        return redirect(url_for('login'))
    else:
        logger.debug(f"Form errors: {form.errors}")  # Log any form validation errors

    return render_template('register.html', form=form)


# Add login route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        logger.info("User is already authenticated, redirecting to homepage.")
        return redirect(url_for('homepage'))  # Redirect if already logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        logger.debug(f"Attempting to log in with Email: {email}")
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            logger.info(f"User logged in: {email}")
            return redirect(url_for('homepage'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
            logger.warning(f"Login failed for Email: {email}")

    return render_template('login.html')

# Add logout route
@app.route('/logout')
@login_required
def logout():
    logger.info(f"User logged out: {current_user.email}")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('homepage'))

# Ping route for testing purposes
@app.route("/ping")
def ping():
    return jsonify(ping="pong")

# Homepage route to render index.html
@app.route("/")
def homepage():
    return render_template("index.html")

# GitHub login route
@app.route("/github")
def github_login():
    if not github.authorized:
        logger.info("GitHub login required, redirecting to GitHub.")
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]
    logger.info(f"User logged in via GitHub: @{username}")
    return f"You are @{username} on GitHub"

# Google login route
@app.route("/google")
def google_login():
    if not google.authorized:
        logger.info("Google login required, redirecting to Google.")
        return redirect(url_for("google.login"))
    res = google.get("/plus/v1/people/me")  # Change API if needed
    username = res.json()["displayName"]
    logger.info(f"User logged in via Google: {username}")
    return f"You are {username} on Google"

if __name__ == "__main__":
    app.run(debug=True)
