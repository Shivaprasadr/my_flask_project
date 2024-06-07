# Set environment variables for Flask application

# Set MySQL database configuration for development
Set-Item -Path Env:MYSQL_HOST -Value "localhost"
Set-Item -Path Env:MYSQL_PORT -Value "3306"
Set-Item -Path Env:MYSQL_USER -Value "flask_user"
Set-Item -Path Env:MYSQL_PASSWORD -Value "user123"
Set-Item -Path Env:MYSQL_DB -Value "my_database"

# Set MySQL database configuration for testing
Set-Item -Path Env:MYSQL_TEST_HOST -Value "localhost"
Set-Item -Path Env:MYSQL_TEST_PORT -Value "3306"
Set-Item -Path Env:MYSQL_TEST_USER -Value "flask_user"
Set-Item -Path Env:MYSQL_TEST_PASSWORD -Value "user123"
Set-Item -Path Env:MYSQL_TEST_DB -Value "my_test_database"

Write-Host "Environment variables set for Flask application."
