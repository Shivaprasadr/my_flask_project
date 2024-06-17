import os
import logging
from flask import Flask
from flask_session import Session
from flaskr.config import Config
from cachelib.file import FileSystemCache

def create_app(config_class=Config, testing=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Configure logging
    if not testing:
        # Set log level to INFO
        logging.basicConfig(level=logging.INFO)
        # Customize log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Create a file handler and set the formatter
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        # Add the file handler to the logger
        app.logger.addHandler(file_handler)
        # Example usage of logging
        app.logger.info('Flask app initialized')

    app.config.from_object(config_class)
    # Ensure a secret key is set for sessions
    app.config['SECRET_KEY'] = os.urandom(24)

    # Configure the session to use CacheLib
    app.config['SESSION_TYPE'] = 'cachelib'
    cache_dir = 'flask_session'
    app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir=cache_dir, threshold=500, default_timeout=app.permanent_session_lifetime.total_seconds())

    # Initialize the session
    Session(app)

    # Initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
