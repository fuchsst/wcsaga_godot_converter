# Makefile for WCSAGA Godot Converter

# Variables
PYTHON := python
UV := uv
PROJECT_DIR := .
CONVERTER_DIR := converter
DATA_CONVERTER_DIR := data_converter

# Default target
.PHONY: help
help:
	@echo "WCSAGA Godot Converter - Development Commands"
	@echo ""
	@echo "General Commands:"
	@echo "  make install              Install dependencies using uv"
	@echo "  make install-dev          Install development dependencies using uv"
	@echo "  make clean                Clean build artifacts"
	@echo "  make init-env             Initialize virtual environment with uv"
	@echo ""
	@echo "Converter Module Commands:"
	@echo "  make converter-test              Run converter tests using uv"
	@echo "  make converter-test-coverage     Run converter tests with coverage using uv"
	@echo "  make converter-format            Format converter code with black and isort using uv"
	@echo "  make converter-lint              Lint converter code with flake8 using uv"
	@echo "  make converter-typecheck         Run converter type checking with mypy using uv"
	@echo "  make converter-quality           Run all converter quality checks using uv"
	@echo "  make converter-setup-env         Run converter environment setup using uv"
	@echo "  make converter-analyze           Run converter codebase analysis using uv"
	@echo "  make converter-migrate           Run converter migration using uv"
	@echo "  make converter-list-tests        List available converter test modules"
	@echo ""
	@echo "Data Converter Module Commands:"
	@echo "  make data-test              Run data_converter tests using uv"
	@echo "  make data-test-coverage     Run data_converter tests with coverage using uv"
	@echo "  make data-format            Format data_converter code with black and isort using uv"
	@echo "  make data-lint              Lint data_converter code with flake8 using uv"
	@echo "  make data-typecheck         Run data_converter type checking with mypy using uv"
	@echo "  make data-quality           Run all data_converter quality checks using uv"
	@echo "  make data-run-tests         Run data_converter tests using run_tests.sh script"
	@echo ""
	@echo "All Modules Commands:"
	@echo "  make all-test               Run tests for both modules using uv"
	@echo "  make all-format             Format code for both modules using uv"
	@echo "  make all-lint               Lint code for both modules using uv"
	@echo "  make all-typecheck          Run type checking for both modules using uv"
	@echo "  make all-quality            Run all quality checks for both modules using uv"

# Install dependencies
.PHONY: install
install:
	$(UV) pip install -e .

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(UV) pip install -e ".[dev]"

# Run tests for converter module
.PHONY: converter-test
converter-test:
	$(UV) run pytest $(CONVERTER_DIR)/tests/ -v

# Run tests with coverage for converter module
.PHONY: converter-test-coverage
converter-test-coverage:
	$(UV) run pytest $(CONVERTER_DIR)/tests/ --cov=$(CONVERTER_DIR) --cov-report=html --cov-report=term

# Format converter code
.PHONY: converter-format
converter-format:
	$(UV) run black $(CONVERTER_DIR)
	$(UV) run isort $(CONVERTER_DIR)

# Lint converter code
.PHONY: converter-lint
converter-lint:
	$(UV) run flake8 $(CONVERTER_DIR)

# Type check converter code
.PHONY: converter-typecheck
converter-typecheck:
	$(UV) run mypy $(CONVERTER_DIR)

# Run tests for data_converter module
.PHONY: data-test
data-test:
	$(UV) run pytest $(DATA_CONVERTER_DIR)/tests/ -v

# Run tests with coverage for data_converter module
.PHONY: data-test-coverage
data-test-coverage:
	$(UV) run pytest $(DATA_CONVERTER_DIR)/tests/ --cov=$(DATA_CONVERTER_DIR) --cov-report=html --cov-report=term

# Format data_converter code
.PHONY: data-format
data-format:
	$(UV) run black $(DATA_CONVERTER_DIR)
	$(UV) run isort $(DATA_CONVERTER_DIR)

# Lint data_converter code
.PHONY: data-lint
data-lint:
	$(UV) run flake8 $(DATA_CONVERTER_DIR)

# Type check data_converter code
.PHONY: data-typecheck
data-typecheck:
	$(UV) run mypy $(DATA_CONVERTER_DIR)

# Run data_converter tests using the run_tests.sh script
.PHONY: data-run-tests
data-run-tests:
	cd $(DATA_CONVERTER_DIR) && ./run_tests.sh

# Run all quality checks for converter module
.PHONY: converter-quality
converter-quality: converter-format converter-lint converter-typecheck

# Run all quality checks for data_converter module
.PHONY: data-quality
data-quality: data-format data-lint data-typecheck

# Run all quality checks for both modules
.PHONY: all-quality
all-quality: all-format all-lint all-typecheck

# Run format for both modules
.PHONY: all-format
all-format: converter-format data-format

# Run lint for both modules
.PHONY: all-lint
all-lint: converter-lint data-lint

# Run typecheck for both modules
.PHONY: all-typecheck
all-typecheck: converter-typecheck data-typecheck

# Run tests for both modules
.PHONY: all-test
all-test: converter-test data-test

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run environment setup for converter module
.PHONY: converter-setup-env
converter-setup-env:
	cd $(CONVERTER_DIR)/scripts && $(UV) run python setup_environment.py --full

# Run codebase analysis for converter module
.PHONY: converter-analyze
converter-analyze:
	cd $(CONVERTER_DIR)/scripts && $(UV) run python analyze_source_codebase.py --source $(abspath source/code) --graph-file $(abspath dependency_graph.json) --output ./analysis.json

# Run migration for converter module
.PHONY: converter-migrate
converter-migrate:
	cd $(CONVERTER_DIR) && $(UV) run python orchestrator/main.py --source $(abspath source/code) --target $(abspath target) --graph-file $(abspath dependency_graph.json)

# Initialize virtual environment with uv
.PHONY: init-env
init-env:
	$(UV) venv
	$(UV) pip install -r requirements.txt
	@echo "Virtual environment setup complete!"
	@echo "To activate the environment, run: source .venv/bin/activate"

# List available test modules for converter
.PHONY: converter-list-tests
converter-list-tests:
	@echo "Available converter test modules:"
	@cd $(CONVERTER_DIR)/tests && ls test_*.py 2>/dev/null | sed 's/test_//' | sed 's/\.py$//' 2>/dev/null | sort || echo "No test files found"

# List available test modules for data_converter
.PHONY: data-list-tests
data-list-tests:
	@echo "Available data_converter test modules:"
	@cd $(DATA_CONVERTER_DIR)/tests && ls test_*.py 2>/dev/null | sed 's/test_//' | sed 's/\.py$//' 2>/dev/null | sort || echo "No test files found"

# List available test modules for both modules
.PHONY: list-tests
list-tests: converter-list-tests data-list-tests

# List available test modules for both modules
.PHONY: list-tests
list-tests: converter-list-tests data-list-tests
