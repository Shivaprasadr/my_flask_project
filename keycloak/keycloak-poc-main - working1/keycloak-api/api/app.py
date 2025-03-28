import os
import logging
from logging.handlers import RotatingFileHandler

from authlib.integrations.flask_oauth2 import current_token
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from api.auth import require_auth
from api.dtos import ItemDTO
from api.models import db

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@db:5432/mydatabase")

# Initialize the database
db.init_app(app)

with app.app_context():
    db.create_all()

# Configure logging
def configure_logging():
    # Set the logging level
    app.logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the console handler to the app's logger
    app.logger.addHandler(console_handler)

# Call the logging configuration function
configure_logging()

# Dummy data for demonstration
user_items = {
    "676afc8d-af2f-4ed2-8c39-9f9a82d18556": [
        ItemDTO("123", "car"),
        ItemDTO("4312", "cellphone"),
        ItemDTO("151", "coffee"),
    ],
    "53535353-b670-4527-a34c-66523687b128": [
        ItemDTO("512", "car"),
        ItemDTO("21255", "cellphone"),
        ItemDTO("142", "coffee"),
        ItemDTO("22112", "tea"),
    ],
}

@app.route("/", methods=["GET"])
def index():
    app.logger.info("Index route accessed")
    return render_template("index.html")

@app.route("/api/users/<string:user_id>/items", methods=["GET"])
@require_auth(None)
def get_user_items(user_id):
    app.logger.info(f"Getting items for user: {user_id}")
    return jsonify({"items": user_items["53535353-b670-4527-a34c-66523687b128"]})

@app.route("/api/public", methods=["GET"])
def public():
    app.logger.info("Public route accessed")
    response = "No Authorization need it"
    return jsonify(response)

@app.route("/api/private", methods=["GET"])
@require_auth(None)
def private():
    app.logger.info("Private route accessed")
    return jsonify(current_token)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)