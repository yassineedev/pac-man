#!/bin/bash

set -e

echo "🟡 Setting up Pac-Man project..."

# Check repository
if [ ! -d ".git" ]; then
    echo "⚠️ Warning: No Git repository found in current directory."
fi

# Create directories
mkdir -p \
    src/core \
    src/models \
    src/services \
    src/views \
    assets \
    data \
    tests \
    project_management

# Create Python package files
touch \
    src/__init__.py \
    src/core/__init__.py \
    src/models/__init__.py \
    src/services/__init__.py \
    src/views/__init__.py

# Create source files
touch \
    src/core/game.py \
    src/core/states.py \
    src/core/constants.py \
    src/models/player.py \
    src/models/ghost.py \
    src/models/maze.py \
    src/services/config.py \
    src/services/maze_generator.py \
    src/services/highscore.py \
    src/views/menu.py \
    src/views/game_view.py \
    src/views/screens.py

# Create tests
touch \
    tests/test_config.py \
    tests/test_player.py \
    tests/test_highscore.py \
    tests/test_maze.py

# Create project management documents
touch \
    project_management/planning.md \
    project_management/tasks.md \
    project_management/architecture.md \
    project_management/risks.md \
    project_management/progress.md \
    project_management/acceptance_tests.md

# Create main entry point
if [ ! -f pac-man.py ]; then
cat > pac-man.py <<'EOF'
"""Pac-Man application entry point."""

import sys


def main() -> None:
    """Start the Pac-Man application."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)

    print("Pac-Man project initialized!")
    print(f"Configuration: {sys.argv[1]}")


if __name__ == "__main__":
    main()
EOF
fi

# Create requirements
if [ ! -f requirements.txt ]; then
cat > requirements.txt <<'EOF'
pygame
flake8
mypy
pytest
pyinstaller
EOF
fi

# Create configuration
if [ ! -f config.json ]; then
cat > config.json <<'EOF'
{
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "highscore_filename": "data/highscores.json",
    "levels": [
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15},
        {"width": 15, "height": 15}
    ]
}
EOF
fi

# Create highscores
if [ ! -f data/highscores.json ]; then
    echo "[]" > data/highscores.json
fi

# Create Makefile
if [ ! -f Makefile ]; then
cat > Makefile <<'EOF'
PYTHON = python3
PIP = $(PYTHON) -m pip

.PHONY: install run debug clean lint lint-strict test

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) pac-man.py config.json

debug:
	$(PYTHON) -m pdb pac-man.py config.json

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .flake8_cache
	rm -rf build dist

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

test:
	$(PYTHON) -m pytest tests/
EOF
fi

# Create .gitignore
if [ ! -f .gitignore ]; then
cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/

# Virtual environment
.venv/
venv/
env/

# Testing and linting
.pytest_cache/
.mypy_cache/
.flake8_cache/
.coverage
htmlcov/

# Build
build/
dist/
*.spec.bak

# Editor
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
EOF
fi

# Create README
if [ ! -f README.md ]; then
cat > README.md <<'EOF'
*This project has been created as part of the 42 curriculum by <login1>, <login2>.*

# Pac-Man

## Description

A Pac-Man game developed in Python using Pygame.

## Instructions

### Installation

```bash
make install
