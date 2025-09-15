.PHONY: help install run test build docker-build docker-run clean deploy-spcs

help: ## Show this help message
	@echo 'Usage: make [target] ...'
	@echo ''
	@echo 'Targets:'
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

setup-db: ## Initialize database with sample data
	python populate_sample_data.py

run: ## Run the application in development mode
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run the test suite
	pytest tests/ -v

test-coverage: ## Run tests with coverage report
	pytest tests/ --cov=app --cov-report=html --cov-report=term

build: ## Build Docker image
	docker build -t coding-interview-platform .

docker-run: build ## Build and run Docker container
	docker run -p 8000:8000 coding-interview-platform

docker-compose-up: ## Start with Docker Compose (includes PostgreSQL)
	docker-compose up -d

docker-compose-down: ## Stop Docker Compose services
	docker-compose down

clean: ## Clean up temporary files and caches
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

deploy-spcs: ## Deploy to Snowflake Park Container Services
	@echo "Make sure to set required environment variables first:"
	@echo "export SNOWFLAKE_ACCOUNT=your_account"
	@echo "export SNOWFLAKE_USER=your_user"
	@echo "export SNOWFLAKE_PASSWORD=your_password"
	@echo "export SNOWFLAKE_DATABASE=your_database"
	@echo "export SNOWFLAKE_SCHEMA=your_schema"
	@echo ""
	./deploy-spcs.sh

lint: ## Run code linting
	flake8 app/ --max-line-length=120 --ignore=E203,W503

format: ## Format code with black
	black app/ tests/

dev: install setup-db ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the application"
	@echo "Visit http://localhost:8000 to access the platform"
	@echo "Test credentials:"
	@echo "  Candidate: username=candidate, password=candidate123"
	@echo "  Interviewer: username=admin, password=admin123"