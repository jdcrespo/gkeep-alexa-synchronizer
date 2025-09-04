# Define variables
DOCKER_IMAGE = gkeep-sync
CONTAINER_NAME = gkeep-sync-container

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE) .

# Run the sync process
sync: build
	docker run --rm --name $(CONTAINER_NAME) \
		--env-file .env \
		-v $(PWD):/app \
		$(DOCKER_IMAGE)
