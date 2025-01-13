# Makefile for Docker Compose commands

# Default compose file
COMPOSE_FILE = docker-compose.yml

# Start the Docker Compose services (non-detached mode)
up:
	docker-compose -f $(COMPOSE_FILE) up

# Start the Docker Compose services (detached mode)
up_detached:
	docker-compose -f $(COMPOSE_FILE) up -d

# Stop the Docker Compose services
down:
	docker-compose down

# Restart the Docker Compose services
restart: down up

# Follow logs of Docker Compose services
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Build and restart the Docker Compose services
build:
	docker-compose down -v
	docker-compose -f $(COMPOSE_FILE) up --build -d
