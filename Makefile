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
	@echo "  make install           Install dependencies"
	@echo "  make install-dev        Install development dependencies"
	@echo "  make test               Run all tests"
	@echo "  make test-coverage      Run tests with coverage"
	@echo "  make format             Format code with black and isort"
	@echo "  make lint               Lint code with flake8"
	@echo "  make typecheck          Run type checking with mypy"
	@echo "  make quality            Run all quality checks"
	@echo "  make clean              Clean build artifacts"
	@echo "  make setup-env          Run environment setup"
	@echo "  make analyze            Run codebase analysis"

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
	$(PYTHON) -m pytest $(CONVERTER_DIR)/tests/ -v

# Run tests with coverage
.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m pytest $(CONVERTER_DIR)/tests/ --cov=$(CONVERTER_DIR) --cov-report=html --cov-report=term

# Format code
.PHONY: format
format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

# Lint code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

# Type check
.PHONY: typecheck
typecheck:
	$(PYTHON) -m mypy .

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
	$(PYTHON) setup_environment.py --full

# Run codebase analysis
.PHONY: analyze
analyze:
	$(PYTHON) analyze_source_codebase.py --source source --output analysis.json

# Run migration
.PHONY: migrate
migrate:
	cd $(CONVERTER_DIR) && $(PYTHON) orchestrator/main.py --source ../source --target ../target