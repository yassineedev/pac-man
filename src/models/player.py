"""Pac-Man player model."""
from dataclasses import dataclass

from src.core.constants import Direction, Position
from src.models.maze import Maze


@dataclass
class Player:
    """Player location, remaining lives and movement."""

    position: Position
    spawn: Position
    lives: int = 3

    def move(self, direction: Direction, maze: Maze) -> None:
        """Move one cell if the destination is walkable."""
        pass

    def lose_life(self) -> None:
        """Remove one life and respawn."""
        pass

    def respawn(self) -> None:
        """Restore the player to the starting cell."""
        pass

    def is_alive(self) -> bool:
        """Return whether the player has lives remaining."""
        pass
