"""Maze representation independent from the assigned generator."""
from dataclasses import dataclass, field

from src.core.constants import Position


@dataclass
class Maze:
    """Grid, collectible positions and spawn points."""

    grid: list[list[int]] = field(default_factory=list)
    pacgums: set[Position] = field(default_factory=set)
    super_pacgums: set[Position] = field(default_factory=set)
    player_spawn: Position = (0, 0)
    ghost_spawns: list[Position] = field(default_factory=list)

    def is_walkable(self, position: Position) -> bool:
        """Return whether the position is inside a corridor."""
        pass

    def neighbors(self, position: Position) -> list[Position]:
        """Return walkable cardinal neighbors."""
        pass

    def consume(self, position: Position) -> str | None:
        """Consume a pellet and return its kind, if any."""
        pass

    def is_complete(self) -> bool:
        """Check whether all required pellets have been collected."""
        pass
