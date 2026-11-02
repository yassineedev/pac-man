"""Ghost entity and basic chase/flee behavior."""
from dataclasses import dataclass

from src.core.constants import Position
from src.models.maze import Maze


@dataclass
class Ghost:
    """A ghost with its own spawn and frightened timer."""

    position: Position
    spawn: Position
    frightened_until: float = 0.0
    respawn_until: float = 0.0

    def update(self, maze: Maze, player: Position, now: float) -> None:
        """Choose and perform a movement step."""
        pass

    def chase(self, maze: Maze, target: Position) -> Position:
        """Choose a walkable step toward the player."""
        pass

    def flee(self, maze: Maze, target: Position) -> Position:
        """Choose a walkable step away from the player."""
        pass

    def make_frightened(self, until: float) -> None:
        """Enable frightened mode until the supplied time."""
        pass

    def is_edible(self, now: float) -> bool:
        """Check whether the ghost can be eaten."""
        pass

    def respawn(self, now: float) -> None:
        """Schedule the ghost to return to its corner."""
        pass
