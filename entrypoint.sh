#!/bin/sh

# Function to check if the MySQL port is ready
wait_for_mysql() {
    echo "Waiting for MySQL..."
    while ! nmap -p 3306 db | grep 3306 | grep "open" >/dev/null 2>&1; do
        sleep 1
    done
    echo "MySQL is up and running."
}

# Wait for MySQL
wait_for_mysql

# Function to check if the database is already initialized
check_db_initialized() {
  mysql -h db -u${MYSQL_USER} -p${MYSQL_PASSWORD} -e "USE ${MYSQL_DB}; SHOW TABLES;" | grep -q "user"
}

# Initialize the database if not already initialized
if ! check_db_initialized; then
  echo "Initializing the database..."
  flask --app flaskr init-db
  if [ $? -ne 0 ]; then
    echo "Database initialization failed."
    exit 1
  fi
else
  echo "Database is already initialized."
fi

# Start the Flask app
echo "Starting the Flask app..."
exec flask --app flaskr run --host=0.0.0.0
