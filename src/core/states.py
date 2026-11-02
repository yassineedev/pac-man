"""Available application states."""
from enum import Enum, auto


class GameState(Enum):
    """Screens and phases managed by the game."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    NAME_ENTRY = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
