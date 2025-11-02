.PHONY: lint format check type-check help install run test clean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	./my-env/bin/pip install -r requirements.txt

run:  ## Run the AI agent
	./my-env/bin/python run.py

test:  ## Run tests
	./my-env/bin/python -m pytest tests/ -v

lint:  ## Run ruff linter (check for issues)
	@echo "🔍 Running ruff linter..."
	./my-env/bin/ruff check .

format:  ## Run ruff formatter (auto-fix issues)
	@echo "✨ Formatting code with ruff..."
	./my-env/bin/ruff check --fix .
	./my-env/bin/ruff format .

type-check:  ## Run mypy type checker
	@echo "🔎 Running mypy type checker..."
	./my-env/bin/mypy src/main_agent.py src/agent_tools.py src/model_switcher.py src/config.py

check: lint type-check  ## Run all checks (lint + type-check)
	@echo "✅ All checks complete!"

fix: format  ## Auto-fix linting issues
	@echo "✅ Code formatted!"

clean:  ## Clean up cache files
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"

