.PHONY: help ensure-poetry autoformat lint-python lint clean install

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ensure-poetry: ## Check if poetry is available
	@if ! [ -x $(command -v poetry) ]; then \
		echo "Please install poetry (e.g. pip install poetry)"; \
		exit 1; \
	fi

autoformat: ensure-poetry ## Autoformat files using isort and black
	poetry run isort confluence2md/
	poetry run black confluence2md/

lint: autoformat ## Lint and auto-format project with isort, black, and flake8

clean: ## Clean up compiled files and coverage reports
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf pip-wheel-metadata
	rm -rf .coverage dist build htmlcov *.egg-info

install: ensure-poetry clean ## Install all dependencies, pre-commit hooks and models
	poetry install
	poetry run pre-commit install
