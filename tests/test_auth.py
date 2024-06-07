import pytest
from flask import g, session, current_app, g
from flaskr.db import get_db
from tests.conftest import logger as test_logger
from flask import url_for

###The register view should render successfully on GET. On POST with valid form data, it should redirect to the login URL and the user’s data should be in the database. Invalid data should display error messages.
def test_register(client, app):
    test_logger.info("Testing registration process")
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    # Check if user is inserted into MySQL
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE username = 'a'")
        cursor_response = cursor.fetchall()
        print (cursor_response)
        assert cursor_response is not None and len(cursor_response) > 0
    test_logger.info("Registration process completed successfully")

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

## The tests for the login view are very similar to those for register. Rather than testing the data in the database, session should have user_id set after logging in.

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    test_logger.info(f"Response data for username '{username}' and password '{password}': {response.data}")
    print(f"Response data for username '{username}' and password '{password}': {response.data}")
    assert message in response.data, "Expected message {message} not found in response data"


## Testing logout is the opposite of login. session should not contain user_id after logging out###
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
