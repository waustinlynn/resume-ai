# Makefile

.PHONY: test integration-tests

# Default target to run unit tests
test:
	@echo "Running unit tests..."
	pytest -m "not integration"

# Target to run integration tests
test-integration:
	@echo "Starting Docker containers and running integration tests..."
	docker-compose up -d  # Start the services in the background
	pytest -m integration  # Run integration tests
	docker-compose down  # Tear down the containers after tests
