from flask import Flask, jsonify, redirect, render_template, url_for
from flask_dance.contrib.github import github
from flask_login import logout_user, login_required, current_user
from app import create_app, db
from app.models import User, OAuth
from app.oauth import github_blueprint
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask application instance
app = create_app()
app.secret_key = os.getenv("SECRET_KEY")  # Set secret key for sessions

# Configure SQLAlchemy database URI
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Register GitHub blueprint
app.register_blueprint(github_blueprint, url_prefix="/login")

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
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]
    return f"You are @{username} on GitHub"

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

if __name__ == "__main__":
    app.run(debug=True)
