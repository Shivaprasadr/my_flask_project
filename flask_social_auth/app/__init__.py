from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://flask_user:user123@localhost/my_social_auth_database"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirects to login if user isn't authenticated

    # Register OAuth blueprints
    from .oauth import github_blueprint, google_blueprint
    app.register_blueprint(github_blueprint, url_prefix='/github_login')
    app.register_blueprint(google_blueprint, url_prefix='/google_login')

    from .models import User  # Import your models
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Adjusted to ensure user_id is cast to int

    with app.app_context():
        db.create_all()

    return app
