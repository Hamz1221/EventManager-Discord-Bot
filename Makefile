# Define the image and container names
IMAGE_NAME=my-event-manager-discord-bot
CONTAINER_NAME=event-manager-bot

# Target to build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Target to run the Docker container
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env $(IMAGE_NAME)

# Target to stop and remove the running container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Target to rebuild the image and restart the container
restart: stop build run

# Target to view logs from the running container
logs:
	docker logs -f $(CONTAINER_NAME)

# Target to clean up the Docker image and container
clean: stop
	docker rmi $(IMAGE_NAME) || true
