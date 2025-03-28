start-docker:
	docker-compose up

clean-docker:
	docker-compose down --volumes --remove-orphans
	docker-compose build --no-cache
	docker-compose up