import os
import tempfile
import sys
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)  # Set log level to INFO
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger('test_logger')
logger.addHandler(file_handler)

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from flaskr.config import TestConfig  # Import TestConfig

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'r') as f:
    _data_sql = f.read()

@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        init_db()
        # Execute SQL script line by line
        db = get_db()
        db.reconnect()
        cursor = db.cursor()
        try:
            cursor.execute(_data_sql)  # Execute the SQL script
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Exception as e:
            db.rollback()  # Rollback the transaction if an error occurs
            print("Error executing SQL script:", e)
            logger.error("Error executing SQL script: %s", e)
        finally:
            pass
        #cursor.close()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)