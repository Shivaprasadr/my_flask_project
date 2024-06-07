import os

class Config:
    DEBUG = True

    # MySQL database configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'flask_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'user123')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'my_database')

class TestConfig(Config):
    TESTING = True
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'flask_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'user123')
    MYSQL_DB = os.environ.get('MYSQL_TEST_DB', 'my_test_database')
