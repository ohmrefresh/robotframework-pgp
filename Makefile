.PHONY: help install install-dev test test-all lint format docs clean build upload upload-test

help:
	@echo "Available targets:"
	@echo "  install       Install package in development mode"
	@echo "  install-dev   Install development dependencies"
	@echo "  test          Run unit tests"
	@echo "  test-all      Run all tests including Robot Framework"
	@echo "  lint          Run code linting"
	@echo "  format        Format code with black"
	@echo "  docs          Build documentation"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build package"
	@echo "  upload        Upload to PyPI"
	@echo "  upload-test   Upload to TestPyPI"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest --cov=RobotFrameworkPGP

test-all:
	pytest --cov=RobotFrameworkPGP
	robot --outputdir results tests/acceptance/

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

docs:
	cd docs && make html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	cd docs && make clean

build: clean
	python -m build

upload: build
	twine upload dist/*

upload-test: build
	twine upload --repository testpypi dist/*

# Development shortcuts
dev-setup: install-dev
	@echo "Development environment setup complete!"

dev-test: lint test test-all
	@echo "All tests passed!"