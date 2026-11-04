#!/usr/bin/env bash
set -euo pipefail

# Create a clean Pac-Man project with empty Python methods.
# Run this script inside your project folder.

if [[ ! -d .git ]]; then
    echo "Error: Run this script inside your Git project folder."
    exit 1
fi

write_new() {
    local path="$1"
    mkdir -p "$(dirname "$path")"
    if [[ -e "$path" ]]; then
        echo "Keep existing file: $path"
        cat >/dev/null
        return
    fi
    cat > "$path"
    echo "Create: $path"
}

mkdir -p src/{core,models,services,views,shared} tests assets/images assets/sounds data project_management .github/workflows
for path in src/__init__.py src/core/__init__.py src/models/__init__.py src/services/__init__.py src/views/__init__.py src/shared/__init__.py tests/__init__.py; do
    touch "$path"
done

write_new pac-man.py <<'PY'
"""Start the Pac-Man game."""

from src.core.game import Game


def main() -> None:
    """Start the app."""
    pass


if __name__ == "__main__":
    main()
PY

write_new src/shared/game_data.py <<'PY'
"""Simple data shared by the game engine and the UI."""

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Position:
    """One place in the maze."""

    x: int
    y: int


class Direction(Enum):
    """Four ways to move."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class GameStatus(Enum):
    """The current game screen or state."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WIN = "win"


@dataclass
class GhostData:
    """Data the UI needs to draw one ghost."""

    position: Position
    color: str
    can_be_eaten: bool = False


@dataclass
class GameData:
    """Data the UI needs to draw the game."""

    player: Position = Position(0, 0)
    ghosts: list[GhostData] = field(default_factory=list)
    walls: list[Position] = field(default_factory=list)
    pacgums: list[Position] = field(default_factory=list)
    big_pacgums: list[Position] = field(default_factory=list)
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: float = 0.0
    status: GameStatus = GameStatus.MENU
PY

write_new src/core/game.py <<'PY'
"""Control the game rules."""

from src.shared.game_data import Direction, GameData


class Game:
    """Keep all game objects and game rules together."""

    def __init__(self) -> None:
        pass

    def start_game(self) -> None:
        """Start a new game."""
        pass

    def update(self, time_passed: float) -> None:
        """Update the game after some time."""
        pass

    def move_player(self, direction: Direction) -> None:
        """Ask the player to move."""
        pass

    def pause_game(self) -> None:
        """Pause the game."""
        pass

    def continue_game(self) -> None:
        """Continue a paused game."""
        pass

    def get_game_data(self) -> GameData:
        """Give the UI the data it needs."""
        pass

    def use_cheat(self, cheat_name: str) -> None:
        """Use a cheat for testing."""
        pass
PY

write_new src/core/level.py <<'PY'
"""Manage game levels."""


class LevelManager:
    """Start levels and check when they end."""

    def __init__(self) -> None:
        pass

    def start_level(self, level_number: int) -> None:
        """Start one level."""
        pass

    def next_level(self) -> None:
        """Go to the next level."""
        pass

    def is_level_done(self) -> bool:
        """Check if the player finished this level."""
        pass
PY

write_new src/core/score.py <<'PY'
"""Manage points and lives."""


class ScoreManager:
    """Keep the player's points and lives."""

    def __init__(self) -> None:
        pass

    def add_points(self, points: int) -> None:
        """Add points to the score."""
        pass

    def lose_life(self) -> None:
        """Remove one life."""
        pass

    def reset_score(self) -> None:
        """Set the score back to zero."""
        pass
PY

write_new src/models/player.py <<'PY'
"""The Pac-Man player."""

from src.shared.game_data import Direction, Position


class Player:
    """Keep the player's place and movement."""

    def __init__(self, start: Position) -> None:
        pass

    def move(self, direction: Direction) -> None:
        """Move the player in one direction."""
        pass

    def return_to_start(self) -> None:
        """Move the player back to the start."""
        pass
PY

write_new src/models/ghost.py <<'PY'
"""Ghost classes with simple polymorphism."""

from abc import ABC, abstractmethod

from src.shared.game_data import Direction, Position


class Ghost(ABC):
    """A base class for every ghost."""

    def __init__(self, start: Position, color: str) -> None:
        pass

    @abstractmethod
    def choose_direction(self, player: Position) -> Direction:
        """Choose where to move next."""
        pass

    def move(self, direction: Direction) -> None:
        """Move the ghost."""
        pass

    def return_to_start(self) -> None:
        """Move the ghost back to the start."""
        pass


class FollowGhost(Ghost):
    """A ghost that follows the player."""

    def choose_direction(self, player: Position) -> Direction:
        """Choose a path toward the player."""
        pass


class RandomGhost(Ghost):
    """A ghost that can pick different paths."""

    def choose_direction(self, player: Position) -> Direction:
        """Choose a path."""
        pass
PY

write_new src/models/maze.py <<'PY'
"""Keep the maze walls and pacgums."""

from src.shared.game_data import Position


class Maze:
    """Keep maze data and check open paths."""

    def __init__(self) -> None:
        pass

    def can_move_to(self, place: Position) -> bool:
        """Check if a place is open."""
        pass

    def get_nearby_paths(self, place: Position) -> list[Position]:
        """Get open places next to this place."""
        pass

    def eat_pacgum(self, place: Position) -> str | None:
        """Remove a pacgum and return its type."""
        pass

    def is_finished(self) -> bool:
        """Check if all pacgums are gone."""
        pass
PY

write_new src/services/config.py <<'PY'
"""Read the game settings from a JSON file."""

from dataclasses import dataclass


@dataclass
class GameConfig:
    """Settings used by the game."""

    width: int = 0
    height: int = 0
    seed: int = 0


class ConfigService:
    """Read and check the game settings."""

    def load_config(self, file_path: str) -> GameConfig:
        """Read settings from a file."""
        pass

    def check_config(self, config: GameConfig) -> bool:
        """Check that settings are valid."""
        pass
PY

write_new src/services/maze_generator.py <<'PY'
"""Connect our game to the required maze generator."""

from src.models.maze import Maze


class MazeGenerator:
    """Use the external maze tool without changing it."""

    def make_maze(self, level: int, seed: int | None = None) -> Maze:
        """Ask the external tool for a maze."""
        pass
PY

write_new src/services/highscore.py <<'PY'
"""Read and save the best scores."""

from dataclasses import dataclass


@dataclass
class HighScore:
    """One player name and score."""

    name: str
    score: int


class HighScoreService:
    """Keep the ten best scores in a JSON file."""

    def load_scores(self) -> list[HighScore]:
        """Read saved scores."""
        pass

    def save_score(self, name: str, score: int) -> None:
        """Save a player's score."""
        pass

    def get_top_scores(self) -> list[HighScore]:
        """Get the ten best scores."""
        pass
PY

write_new src/views/game_view.py <<'PY'
"""Draw the game with Pygame."""

from src.shared.game_data import GameData


class GameView:
    """Draw the maze, player, ghosts, and score."""

    def __init__(self) -> None:
        pass

    def draw_game(self, game_data: GameData) -> None:
        """Draw the current game."""
        pass

    def draw_maze(self, game_data: GameData) -> None:
        """Draw walls and pacgums."""
        pass

    def draw_player(self, game_data: GameData) -> None:
        """Draw Pac-Man."""
        pass

    def draw_ghosts(self, game_data: GameData) -> None:
        """Draw all ghosts."""
        pass

    def draw_score(self, game_data: GameData) -> None:
        """Draw score, lives, level, and time."""
        pass
PY

write_new src/views/menu.py <<'PY'
"""Draw the main menu."""


class MainMenu:
    """Show choices before the game starts."""

    def draw(self) -> None:
        """Draw the menu."""
        pass

    def handle_input(self, key: str) -> None:
        """Read a menu key."""
        pass
PY

write_new src/views/screens.py <<'PY'
"""Other game screens."""

from abc import ABC, abstractmethod


class Screen(ABC):
    """A base class for game screens."""

    @abstractmethod
    def draw(self) -> None:
        """Draw this screen."""
        pass


class PauseScreen(Screen):
    """Show the pause screen."""

    def draw(self) -> None:
        """Draw the pause screen."""
        pass


class EndScreen(Screen):
    """Show the win or game-over screen."""

    def draw(self) -> None:
        """Draw the end screen."""
        pass


class HelpScreen(Screen):
    """Show how to play."""

    def draw(self) -> None:
        """Draw the help screen."""
        pass


class HighScoreScreen(Screen):
    """Show the best scores."""

    def draw(self) -> None:
        """Draw the highscore screen."""
        pass
PY

write_new src/views/input_handler.py <<'PY'
"""Read keys from the player."""

from src.shared.game_data import Direction


class InputHandler:
    """Turn keyboard keys into game commands."""

    def get_direction(self, key: str) -> Direction | None:
        """Get a direction from a key."""
        pass
PY

write_new tests/test_game.py <<'PY'
"""Tests for game rules. Add tests as features are built."""
PY

write_new requirements.txt <<'TXT'
pygame>=2.5,<3
flake8>=7,<8
mypy>=1.10,<2
pytest>=8,<10
pyinstaller>=6,<7
TXT

write_new Makefile <<'MAKE'
PYTHON = python3

.PHONY: install run debug clean lint test

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) pac-man.py config.json

debug:
	$(PYTHON) -m pdb pac-man.py config.json

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	$(PYTHON) -m flake8 src pac-man.py
	$(PYTHON) -m mypy src pac-man.py --check-untyped-defs

test:
	$(PYTHON) -m pytest tests
MAKE

write_new config.json <<'JSON'
{
  "width": 21,
  "height": 21,
  "seed": 42
}
JSON

write_new data/highscores.json <<'JSON'
[]
JSON

write_new .gitignore <<'TXT'
__pycache__/
*.py[cod]
.venv/
.mypy_cache/
.pytest_cache/
.ruff_cache/
dist/
build/
*.spec.bak
.DS_Store
TXT

write_new README.md <<'MD'
*This project is part of the 42 school curriculum.*

# Pac-Man

A Pac-Man game made with Python and Pygame.

## Status

This is only the project skeleton. Game logic is not ready.

## Team

- Developer 1: game engine, maze, player, ghosts, levels, config.
- Developer 2: game screens, drawing, keys, highscores.
- Both: tests, code review, and documentation.

## Run

1. Run `make install`.
2. Run `make run` after the game logic is added.

## Folders

- `src/core`: game rules.
- `src/models`: game objects.
- `src/services`: files and maze tool.
- `src/views`: Pygame screens.
- `src/shared`: data used by both developers.

## To finish

Add the full subject requirements, game rules, tests, and packaging steps.
MD

write_new project_management/team_plan.md <<'MD'
# Team Plan

## Roles

Developer 1 (lead): engine, maze, player, ghosts, levels, config, Git merges.
Developer 2: UI, menus, screens, keys, highscores.
Both: review, test, and write docs.

## Git rules

1. Do not code on `main`.
2. Make a new branch for each task.
3. Open a pull request (PR) when a task is ready.
4. The other developer reviews the PR.
5. Test before merging.
6. Merge into `main`.
7. Delete the finished branch.
8. Start the next branch from the new `main`.

## First tasks

1. Agree on shared data in `src/shared/game_data.py`.
2. Lead: connect the external maze generator.
3. UI developer: draw a test maze with fake data.
4. Merge small tasks every day.

## Daily check

- What did we finish?
- What is blocked?
- What do we do next?
- Are there PRs to review?
MD

write_new project_management/progress.md <<'MD'
# Daily Progress

| Day | Plan | Done | Problems |
| --- | --- | --- | --- |
| 1 | Setup and shared data | | |
| 2 | Maze and player | | |
| 3 | Ghosts and HUD | | |
| 4 | Score and lives | | |
| 5 | Levels and screens | | |
| 6 | Config and highscores | | |
| 7 | Tests and package | | |
| 8 | Final check and submit | | |
MD

write_new project_management/risks.md <<'MD'
# Risks

| Risk | What we will do |
| --- | --- |
| Maze tool does not work | Test it on Day 1. |
| UI and engine do not match | Agree on shared data first. |
| Merge conflicts | Make small PRs and merge often. |
| We are late | Finish required work before extras. |
| Game package does not run | Test packaging before the last day. |
MD

write_new .github/pull_request_template.md <<'MD'
## What did you change?

## Related issue

Closes #

## Checks

- [ ] My code uses simple names.
- [ ] I added type hints and short docstrings.
- [ ] I tested my changes.
- [ ] I ran `make lint`.
- [ ] I did not break shared data.
MD

write_new .github/workflows/check.yml <<'YAML'
name: Check Python

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install tools
        run: python -m pip install -r requirements.txt
      - name: Check Python files
        run: python -m compileall -q pac-man.py src
YAML

write_new .github/ISSUE_TEMPLATE.md <<'MD'
## Task

## Owner

## Done when

- [ ] The code works.
- [ ] The code is tested.
- [ ] The PR is reviewed.
MD

write_new setup_ssh.sh <<'BASH2'
#!/usr/bin/env bash
set -euo pipefail

# Change this Git repository from HTTPS to SSH.
# This script does not make SSH keys or push code.

git remote set-url origin git@github.com:yassineedev/pac-man.git
echo "Remote URL:"
git remote -v
echo "Testing SSH with GitHub..."
ssh -T git@github.com || true
echo "If GitHub said 'successfully authenticated', SSH is ready."
BASH2
chmod +x setup_ssh.sh

printf '\nProject skeleton is ready.\n'
printf 'Next: check files with git status, then commit on a feature branch.\n'
printf 'Note: Methods are empty. The game cannot run yet.\n'
