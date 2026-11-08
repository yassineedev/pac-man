from abc import ABC, abstractmethod

from src.shared.game_data import Direction, Position


class Character(ABC):
    """Base class for all moving characters."""

    def __init__(self, start: Position, direction: Direction) -> None:
        self.position = start
        self.start_position = start
        self.direction = direction

    @abstractmethod
    def choose_move(self, maze, player_position: Position) -> Direction:
        """Choose the next direction."""
        pass

    def move(self, direction: Direction, maze) -> None:
        """Move one cell if there is no wall."""
        x, y = self.position.x, self.position.y

        if not maze.can_move(x, y, direction.value):
            return

        offsets = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }

        dx, dy = offsets[direction]

        self.position = Position(x + dx, y + dy)
        self.direction = direction

    def return_to_start(self) -> None:
        """Reset character position."""
        self.position = self.start_position
