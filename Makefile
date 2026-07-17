.PHONY: help install install-backend install-frontend test test-backend test-frontend test-evals lint format docker-build docker-up docker-down clean

help:
	@echo "AI Assistance Platform - Available Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install              Install all dependencies"
	@echo "  make install-backend      Install backend dependencies"
	@echo "  make install-frontend     Install frontend dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev                  Run backend and frontend with hot-reload"
	@echo "  make dev-backend          Run backend with hot-reload"
	@echo "  make dev-frontend         Run frontend with hot-reload"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests"
	@echo "  make test-backend         Run backend tests"
	@echo "  make test-frontend        Run frontend tests"
	@echo "  make test-evals           Run evaluation tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint                 Run linting checks"
	@echo "  make format               Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build         Build Docker images"
	@echo "  make docker-up            Start services with Docker Compose"
	@echo "  make docker-down          Stop services"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean                Clean build artifacts and cache"

install: install-backend install-frontend pre-commit-install

install-backend:
	cd backend && uv venv && uv pip install -e ".[dev]"

install-frontend:
	cd frontend && npm install

pre-commit-install:
	pre-commit install

dev:
	@echo "Starting backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	docker-compose -f docker/compose.yml up

dev-backend:
	cd backend && uvicorn main:app --reload

dev-frontend:
	cd frontend && npm start

test: test-backend test-frontend test-evals

test-backend:
	cd backend && pytest

test-backend-verbose:
	cd backend && pytest -v --cov

test-frontend:
	cd frontend && npm test -- --watchAll=false

test-evals:
	cd evals && pip install -r requirements.txt && pytest

lint:
	cd backend && ruff check . && mypy .
	cd frontend && npm run lint || true

format:
	cd backend && ruff format . && ruff check . --fix
	cd frontend && npm run format || true

docker-build:
	docker-compose -f docker/compose.yml build

docker-up:
	docker-compose -f docker/compose.yml up

docker-down:
	docker-compose -f docker/compose.yml down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/build frontend/build .terraform tfplan *.log
