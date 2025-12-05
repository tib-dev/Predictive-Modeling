# ============================================================
# Insurance Risk Analytics — Makefile
# ============================================================

# Python executable
PYTHON := python3

# Virtual environment directory
VENV := .venv

# Convenience wrapper to run commands inside venv
VENV_PY := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
VENV_PYTEST := $(VENV)/bin/pytest

# ============================================================
# Setup
# ============================================================

.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created."

.PHONY: install
install: venv
	@echo "Installing dependencies..."
	$(VENV_PIP) install -r requirements.txt
	@echo "Dependencies installed."

.PHONY: install-dev
install-dev: venv
	@echo "Installing development dependencies..."
	$(VENV_PIP) install -r requirements-dev.txt
	@echo "Dev dependencies installed."

# ============================================================
# Testing
# ============================================================

.PHONY: test
test:
	@echo "Running unit tests..."
	$(VENV_PYTEST) -q
	@echo "All tests completed."

.PHONY: test-verbose
test-verbose:
	@echo "Running tests with verbose output..."
	$(VENV_PYTEST) -vv

.PHONY: coverage
coverage:
	@echo "Running coverage..."
	$(VENV_PYTEST) --cov=insurance_analytics --cov-report=term-missing

.PHONY: coverage-html
coverage-html:
	@echo "Creating HTML coverage report..."
	$(VENV_PYTEST) --cov=insurance_analytics --cov-report=html
	@echo "Open htmlcov/index.html to view the report."

# ============================================================
# Code Quality (Optional)
# ============================================================

.PHONY: format
format:
	@echo "Formatting codebase with Black..."
	$(VENV_PY) -m black src/ tests/

.PHONY: lint
lint:
	@echo "Running lint checks with flake8..."
	$(VENV_PY) -m flake8 src/ tests/

# ============================================================
# Cleanup
# ============================================================

.PHONY: clean
clean:
	@echo "Removing caches and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	rm -rf htmlcov
	rm -rf dist build
	@echo "Cleanup done."

.PHONY: reset
reset: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Fresh project reset complete."
