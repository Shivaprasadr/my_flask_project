# config.py

class Config:
    # Your other configuration variables
    # For example:
    DEBUG = True

    # MySQL database configuration
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306  # Default MySQL port
    MYSQL_USER = 'flask_user'
    MYSQL_PASSWORD = 'user123'
    MYSQL_DB = 'my_database'

class TestConfig(Config):
    # MySQL database configuration for testing
    TESTING = True
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = 'flask_user'
    MYSQL_PASSWORD = 'user123'
    MYSQL_DB = 'my_test_database'
