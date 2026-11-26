from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GhostStatu(Enum):
    WEAK = "WEAK"
    EATEN = "EATEN"
    NORMAL = "NORMAL"


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class PlayerData:
    position: Position
    direction: Direction


@dataclass(frozen=True)
class GhostData:
    name: str
    position: Position
    direction: Direction
    state: str


@dataclass(frozen=True)
class GameData:
    maze: tuple[tuple[int, ...], ...]
    player: PlayerData
    ghosts: tuple[GhostData, ...]
    pacgums: tuple[Position, ...]
    power_pacgums: tuple[Position, ...]
    score: int
    lives: int
    level: int
    time_left: float
    state: str
    cheat_mode: bool
    player_move_time: float = 0.2
    ghost_move_time: float = 0.5
    power_mode: bool = False
    power_mode_time_left: float = 0.0
    invincible: bool = False
    ghosts_frozen: bool = False
    fast_player: bool = False
    highscores: tuple[tuple[str, int], ...] = ()
