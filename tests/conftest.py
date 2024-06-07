import os
import sys
import logging
import pytest

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set log level to INFO
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger('test_logger')
logger.addHandler(file_handler)

# Add the parent directory of 'flaskr' to the Python path
# Assuming the structure is my_flask_project/tests/conftest.py and my_flask_project/flaskr/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskr import create_app
from flaskr.db import get_db, init_db
from flaskr.config import TestConfig

# Load the SQL script
data_sql_path = os.path.join(os.path.dirname(__file__), 'data.sql')
with open(data_sql_path, 'r') as f:
    _data_sql = f.read()

@pytest.fixture
def app():
    app = create_app(TestConfig, testing=True)

    with app.app_context():
        init_db()

        db = get_db()
        cursor = db.cursor()

        try:
            # Log and execute the SQL script for initial setup
            for line in _data_sql.splitlines():
                if line.strip():  # Ignore empty lines
                    logging.info(f"Executing SQL: {line}")
                    cursor.execute(line)
                    result = cursor.fetchall()
                    logging.info(f"Result: {result}")
                    db.commit()

            # Verify data in the `user` table
            cursor.execute('SELECT * FROM `user`')
            users = cursor.fetchall()
            logging.info(f"Users before tests: {users}")

        except Exception as e:
            db.rollback()  # Rollback the transaction if an error occurs
            logging.error("Error executing SQL script: %s", e)
        finally:
            cursor.close()

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
        print(username, password)
        response = self._client.post('/auth/login', data={'username': username, 'password': password})
        print(f"Login response status: {response.status_code}")
        print(f"Login response headers: {response.headers}")
        print(f"Login response data: {response.data}")
        return response

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
