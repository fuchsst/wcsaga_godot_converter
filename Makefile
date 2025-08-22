# Makefile for WCSAGA Godot Converter

# Variables
PYTHON := python
UV := uv
PROJECT_DIR := .
CONVERTER_DIR := converter

# Default target
.PHONY: help
help:
	@echo "WCSAGA Godot Converter - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install           Install dependencies using uv"
	@echo "  make install-dev       Install development dependencies using uv"
	@echo "  make test              Run all tests using uv"
	@echo "  make test-coverage     Run tests with coverage using uv"
	@echo "  make format            Format code with black and isort using uv"
	@echo "  make lint              Lint code with flake8 using uv"
	@echo "  make typecheck         Run type checking with mypy using uv"
	@echo "  make quality           Run all quality checks using uv"
	@echo "  make clean             Clean build artifacts"
	@echo "  make setup-env         Run environment setup using uv"
	@echo "  make analyze           Run codebase analysis using uv"
	@echo "  make migrate           Run migration using uv"
	@echo "  make init-env          Initialize virtual environment with uv"
	@echo "  make list-tests        List available test modules"

# Install dependencies
.PHONY: install
install:
	$(UV) pip install -e .

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(UV) pip install -e ".[dev]"

# Run tests
.PHONY: test
test:
	$(UV) run pytest $(CONVERTER_DIR)/tests/ -v

# Run tests with coverage
.PHONY: test-coverage
test-coverage:
	$(UV) run pytest $(CONVERTER_DIR)/tests/ --cov=$(CONVERTER_DIR) --cov-report=html --cov-report=term

# Format code
.PHONY: format
format:
	$(UV) run black converter
	$(UV) run isort converter

# Lint code
.PHONY: lint
lint:
	$(UV) run flake8 converter

# Type check
.PHONY: typecheck
typecheck:
	$(UV) run mypy converter

# Run all quality checks
.PHONY: quality
quality: format lint typecheck

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run environment setup
.PHONY: setup-env
setup-env:
	cd $(CONVERTER_DIR)/scripts && $(UV) run python setup_environment.py --full

# Run codebase analysis
.PHONY: analyze
analyze:
	cd $(CONVERTER_DIR)/scripts && $(UV) run python analyze_source_codebase.py --source ./source --output ./analysis.json

# Run migration
.PHONY: migrate
migrate:
	cd $(CONVERTER_DIR) && $(UV) run python orchestrator/main.py --source ./source --target ./target

# Initialize virtual environment with uv
.PHONY: init-env
init-env:
	$(UV) venv
	$(UV) pip install -r requirements.txt
	@echo "Virtual environment setup complete!"
	@echo "To activate the environment, run: source .venv/bin/activate"

# List available test modules
.PHONY: list-tests
list-tests:
	@echo "Available test modules:"
	@cd $(CONVERTER_DIR)/tests && ls test_*.py | sed 's/test_//' | sed 's/\.py$//' | sort