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
